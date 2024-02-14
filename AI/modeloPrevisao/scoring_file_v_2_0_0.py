# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import pickle
import numpy as np
import pandas as pd
import joblib

import azureml.automl.core
from azureml.automl.core.shared import logging_utilities, log_server
from azureml.telemetry import INSTRUMENTATION_KEY

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType
from inference_schema.parameter_types.standard_py_parameter_type import StandardPythonParameterType

data_sample = PandasParameterType(pd.DataFrame({"0": pd.Series([0], dtype="int64"), "tcp": pd.Series(["example_value"], dtype="object"), "private": pd.Series(["example_value"], dtype="object"), "REJ": pd.Series(["example_value"], dtype="object"), "0_1": pd.Series([0], dtype="int64"), "0_2": pd.Series([0], dtype="int64"), "0_3": pd.Series([0], dtype="int64"), "0_4": pd.Series([0], dtype="int64"), "0_5": pd.Series([0], dtype="int64"), "0_6": pd.Series([0], dtype="int64"), "0_7": pd.Series([0], dtype="int64"), "0_8": pd.Series([0], dtype="int64"), "0_9": pd.Series([0], dtype="int64"), "0_10": pd.Series([0], dtype="int64"), "0_11": pd.Series([0], dtype="int64"), "0_12": pd.Series([0], dtype="int64"), "0_13": pd.Series([0], dtype="int64"), "0_14": pd.Series([0], dtype="int64"), "0_15": pd.Series([0], dtype="int64"), "0_16": pd.Series([0], dtype="int64"), "0_17": pd.Series([0], dtype="int64"), "0_18": pd.Series([0], dtype="int64"), "229": pd.Series([0], dtype="int64"), "10": pd.Series([0], dtype="int64"), "0_19": pd.Series([0.0], dtype="float64"), "0_20": pd.Series([0.0], dtype="float64"), "1": pd.Series([0.0], dtype="float64"), "1_21": pd.Series(["example_value"], dtype="object"), "0.04": pd.Series([0.0], dtype="float64"), "0.06": pd.Series([0.0], dtype="float64"), "0_22": pd.Series([0.0], dtype="float64"), "255": pd.Series([0], dtype="int64"), "10_23": pd.Series(["example_value"], dtype="object"), "0.04_24": pd.Series(["example_value"], dtype="object"), "0.06_25": pd.Series(["example_value"], dtype="object"), "0_26": pd.Series(["example_value"], dtype="object"), "0_27": pd.Series(["example_value"], dtype="object"), "0_28": pd.Series(["example_value"], dtype="object"), "0_29": pd.Series(["example_value"], dtype="object"), "1_30": pd.Series(["example_value"], dtype="object"), "1_31": pd.Series(["example_value"], dtype="object")}))
input_sample = StandardPythonParameterType({'data': data_sample})
method_sample = StandardPythonParameterType("predict")
sample_global_params = StandardPythonParameterType({"method": method_sample})

result_sample = NumpyParameterType(np.array(["example_value"]))
output_sample = StandardPythonParameterType({'Results':result_sample})

try:
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity('INFO')
    logger = logging.getLogger('azureml.automl.core.scoring_script_v2')
except:
    pass


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
    path = os.path.normpath(model_path)
    path_split = path.split(os.sep)
    log_server.update_custom_dimensions({'model_name': path_split[-3], 'model_version': path_split[-2]})
    try:
        logger.info("Loading model from path.")
        model = joblib.load(model_path)
        logger.info("Loading successful.")
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        raise

@input_schema('GlobalParameters', sample_global_params, convert_to_provided_type=False)
@input_schema('Inputs', input_sample)
@output_schema(output_sample)
def run(Inputs, GlobalParameters={"method": "predict"}):
    data = Inputs['data']
    if GlobalParameters.get("method", None) == "predict_proba":
        result = model.predict_proba(data)
    elif GlobalParameters.get("method", None) == "predict":
        result = model.predict(data)
    else:
        raise Exception(f"Invalid predict method argument received. GlobalParameters: {GlobalParameters}")
    if isinstance(result, pd.DataFrame):
        result = result.values
    return {'Results':result.tolist()}
