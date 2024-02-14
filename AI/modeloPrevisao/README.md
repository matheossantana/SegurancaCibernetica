# Previsão de Ataques Cibernéticos

## Introdução
O modelo de previsão de ataques cibernéticos foi construído utilizando um pipeline de aprendizado de máquina que integra um pré-processador MaxAbsScaler e um classificador ExtraTreesClassifier. O ExtraTreesClassifier é uma modificação do algoritmo Random Forest que seleciona divisões de nós aleatórios. É útil em modelos que precisam ser robustos a variações nos dados e é conhecido por sua capacidade de atuar bem em grandes conjuntos de dados com muitas variáveis de entrada.

### Parâmetros do Modelo:
* Algoritmo: ExtraTreesClassifier
* Pré-processamento: MaxAbsScaler
* Critério: Gini
* Número de Estimadores: 10
* Bootstrap: False (não usa amostragem com reposição)
* Peso das Classes: None (pesos iguais para todas as classes)
* Máximo de Features: 0.7 (usa 70% das features para cada árvore)
* Mínimo de Amostras por Folha: Aprox. 0.036 (3.6% das amostras totais)
* Mínimo de Amostras para Dividir um Nó: 0.01 (1% das amostras totais)
### Desempenho do Modelo:
O desempenho do modelo foi avaliado com base na métrica AUC Ponderada (Área sob a Curva ROC), onde o modelo alcançou uma pontuação de aproximadamente 0.98775. Esta métrica é particularmente importante pois leva em consideração tanto a taxa de verdadeiros positivos quanto a taxa de falsos positivos, sendo um bom indicador de desempenho para problemas de classificação desbalanceados.

### Utilização do Modelo:
O modelo foi integrado a um serviço de ponto de extremidade que permite a realização de previsões em tempo real. Este serviço aceita dados de entrada em um formato específico e retorna uma previsão de probabilidade de cada classe, que neste contexto, representa a probabilidade de um determinado comportamento na rede ser um ataque cibernético.

Para mais detalhes sobre como utilizar o ponto de extremidade para fazer previsões com o modelo, consulte a seção "Uso do Modelo" deste documento.


## Configuração do Ponto de Extremidade

O modelo de previsão de ataques cibernéticos está configurado para ser servido por meio de um ponto de extremidade de API, permitindo a realização de previsões em tempo real. A API foi implementada usando o Azure Machine Learning, mas os conceitos são aplicáveis a qualquer serviço de hospedagem de modelo.

### Deploy do Modelo
O modelo foi registrado e implantado em um serviço de inferência do Azure Machine Learning, o qual expõe uma API REST para realizar previsões. O serviço está configurado para escalar conforme a demanda e é protegido para garantir que apenas clientes autorizados possam acessá-lo.

### Entrada de Dados
A API espera receber dados no formato JSON, onde cada chave do objeto JSON representa um recurso utilizado pelo modelo durante o treinamento. Um exemplo de carga útil de entrada pode ser encontrado no arquivo `scoring_file_v_2_0_0.py`.

### Realizando Previsões
Para realizar uma previsão, faça uma solicitação POST para o ponto de extremidade da API com a carga útil de entrada apropriada. O modelo retornará a previsão em um formato JSON com a probabilidade associada a cada classe de saída.

### Monitoramento e Logs
Logs de operações e telemetria estão habilitados para o serviço de ponto de extremidade, o que permite monitorar a saúde do serviço, o uso da API e as previsões realizadas. Isso é essencial para manter a qualidade e a confiabilidade do serviço de previsão.

### Segurança
As práticas recomendadas de segurança foram seguidas para proteger o ponto de extremidade. Isso inclui a autenticação baseada em tokens, criptografia de dados em trânsito e armazenamento seguro de chaves e credenciais.

### Documentação da API
A documentação detalhada da API, incluindo o contrato de entrada/saída e exemplos de solicitações/respostas, está disponível junto com o serviço de ponto de extremidade.

Para informações mais detalhadas sobre como interagir com o ponto de extremidade e realizar previsões, consulte o arquivo `scoring_file_v_2_0_0.py`.

## Uso do Modelo

O modelo de previsão de ataques cibernéticos pode ser utilizado através de uma API REST que aceita dados de entrada em formato JSON e retorna a previsão do modelo.

### Preparação dos Dados
Os dados enviados para o ponto de extremidade devem estar no mesmo formato que o modelo espera. Eles devem ser pré-processados adequadamente, de acordo com o que foi feito durante o treinamento do modelo. Um exemplo de como os dados de entrada devem ser formatados pode ser encontrado no arquivo `scoring_file_v_2_0_0.py`.

### Solicitação de Previsão
Para fazer uma previsão, você deve enviar uma solicitação POST para o ponto de extremidade da API com os dados de entrada formatados corretamente. A solicitação deve ser enviada para a URL do ponto de extremidade que foi configurada durante a etapa de implantação.

Exemplo de solicitação POST usando `curl`:

```bash
curl -X POST "https://ai-900-dio-wvdlt.eastus2.inference.ml.azure.com/score" -H "Content-Type:application/json" -d "{\"data\": <dados_de_entrada>}"
```
Substitua `<dados_de_entrada>` pelo JSON dos dados de entrada.

### Resposta do Modelo
A resposta da API será um JSON contendo as previsões do modelo. Se o método de previsão for predict_proba, a resposta incluirá as probabilidades associadas a cada classe. Se o método for predict, a resposta incluirá a classe prevista.

### Tratamento de Erros
Qualquer erro no processamento da solicitação ou na execução do modelo será retornado como uma resposta da API com detalhes do erro. É importante tratar essas respostas adequadamente no cliente que está fazendo a solicitação.

Para mais detalhes sobre a implementação específica e exemplos de código, consulte o arquivo `scoring_file_v_2_0_0.py`.




