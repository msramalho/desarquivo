# Processo de Recolha de dados
(english below)

Instruções para recolha de dados:
* Configurar o processo de recolha no ficheiro [config.json](config.json), nomeadamente as entidades de início, o número de notícias de cada website em cada pedido à API, quais os websites de onde recolher informação, quais as datas entre as quais recolher informação, configurar o número de `rounds` de recolha (por experiência 6 a 10 funciona bem para ser abrangente mas não redundante)
* Instanciar mongodb e atualizar os respetivos dados no ficheiro [config.json](config.json)
* criar um virtual environment de python `py -m venv env`, ativá-lo `source env/bin/activate` (linux) ou `env/Scripts/activate` (windows), e instalar os requisitos `pip install -r requirements.txt`
* dowload do modelo para português da biblioteca spacy (reconhecimento de entidades): `python -m spacy download pt_core_news_sm` (ou treina um novo)
* executar o ficheiro de recolha, idealmente deixando a correr em paralelo (pode demorar várias horas conforme as configurações, mas não deverá ultrapassar as 24h para 8 rondas usando 50 notícias como o limite no pedido à API) `nohup py collect.py &`
* Depois da recolha estar pronta é aconselhável que se executem os seguintes notebooks de python (podem ser convertidos para scripts e executados):
  * [fix_news_text](fix_news_text.ipynb)
  * [fix_timestamps](fix_fix_timestamps.ipynb)
* Por fim, executar o notebook [process](process.ipynb) que vai gerar as coleções `final_entities` e `final_news` na mongodb e também vai gerar os ficheiros necessários para carregar o grafo para o neo4j (e inclui os comandos de importação)


A pasta [rnd](rnd/) não contém código essencial, mas sim alguns scripts que podem ajudar a testar e a diagnosticar o processo de recolha de dados. 

# Data Collection process

Instructions for data collection:
* Configure the collection process in the [config.json](config.json) file, namely the seed entities, the number of news of each website (in each API request), which websites to search, the number of rounds/iterations of the collection process (from experience, 6 to 10 is a good number for being large enough but not redundant)
* Instanciate mongodb and update the respective access credentials in [config.json](config.json)
* create a python virtual environment `py -m venv env`, activate it `source env/bin/activate` (linux) or `env/Scripts/activate` (windows), and install the requirements `pip install -r requirements.txt`
* download the portuguese spacy model (for entity recognition): `python -m spacy download pt_core_news_sm` (or train your own)
* execute the collection file, ideally leaving it running in parallel (as it can take several hours depending on the configurations, but typically it should stay within 24h for 8 rounds and 50 news per request) `nohup py collect.py &`
* After the collection is ready, it is advisable that the following Jupyter notebooks are executed (they can be converted to scripts and then executed):
  * [fix_news_text](fix_news_text.ipynb)
  * [fix_timestamps](fix_fix_timestamps.ipynb)
* Finally, execute the [process](process.ipynb) notebook which will generate the mongo collections `final_entities` and `final_news` and also generate the necessary files to load the graph into neo4j (including import commands and instructions)

The [rnd](rnd/) folder does not contain essential code, but rather some scripts that might help to test and diagnose the data collection process. 