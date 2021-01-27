<!-- <h1 align="center">Desarquivo</h1> -->

<p align="center">
<a href="https://msramalho.github.io/desarquivo/" >
<img height="100px" src="https://i.imgur.com/bbqpudq.gif" />
</a>
<br>
<br>
Um projeto que procura democratizar e complementar o <u>jornalismo de investigação</u> e a <u>verificação de factos</u>. 
<br>
Arquivo.pt para justiça, jornalismo e verdade.
<br>
<br>
<i>A project that seeks to democratize and complement <u>investigative journalism</u> and <u>fact-checking</u>.
<br>
Arquivo.pt for justice, journalism and truth.</i>
<br>
<h3 align="center"><a href="README_en.md">English Version</a></h3>
</p>

## Sobre o Projeto

O Desarquivo foi desenhado como um esforço reprodutível que tem por base um conjunto de configurações das quais se destacam

- As primeiras entidades a investigar e que dão origem à expansão da rede - nesta versão, foram `José Sócrates` e `Isabel dos Santos`
- O período de tempo a incluir - nesta versão, entre o ano `2000` e o ano `2020`
- Os jornais a procurar - nesta versão, foram [Público](https://www.publico.pt/), [Expresso](https://expresso.pt/), [Diário de Notícias](https://www.dn.pt/), [Correio da Manhã](https://www.cmjornal.pt/), [Sol](https://sol.sapo.pt/), [Visão](https://visao.sapo.pt/) e [Jornal de Notícias](https://www.jn.pt/)

As notícias recolhidas foram analisadas e de lá foram extraídas entidades (pessoas, organizações, lugares, entre outras) e respetivas relações. Estas relações formam uma rede imensa que é agora explorável nesta interface gráfica ou diretamente nos dados que são de [livre acesso](DATASETS.md).

O desarquivo assenta sobre duas bases de dados, nomeadamente [MongoDB](https://www.mongodb.com/) (NoSQL) e [neo4j](https://neo4j.com/) (Grafos).

<p align="center">
   <a href="https://youtu.be/tVlOUuRqIVU" >
      <img height="200px" src="https://i.imgur.com/0sHj6Fi.png"/>
   </a>
   <br>
   Vídeo de apresentação
</p>

### Cidadãos

Podem aceder ao [desarquivo](https://msramalho.github.io/desarquivo/) e explorar as suas diferentes funcionalidades e exemplos.

<p align="center"><img src="https://i.imgur.com/NRxBO0h.png"/></p>

### Investigadores e Programadores

Podem ainda aceder aos [datasets](DATASETS.md) disponibilizados e executar _queries_ mais complexas sobre os grafos gerados.

#### Instruções completas para usar o comando `neo4j-admin`
```bash
# clonar este repositório e entrar na pasta
git clone https://github.com/msramalho/desarquivo
cd desarquivo

# fazer uma cópia dos ficheiros deo configuração
cp .neo4j.env.example .neo4j.env
cp .mongo.env.example .mongo.env
cp ./api/.env.example .api/.env

# (editar os ficheiros com as passwords desejadas)
...

# criar as pastas correspondentes aos volumes necessários (se for o Docker a fazê-lo as permissões estaram erradas)
mkdir neo4j/import neo4j/data neo4j/conf neo4j/logs mongodb/

# colocar os datasets no formato igual ao dataset03a.zip (i_entities.csv e i_relationships.csv) na pasta /import
unzip dataset03a.zip -d <SOME DIR>
cp <SOME DIR>/i_*.csv ./neo4j/import/

# correr o seguinte comando para que importar o dataset neo4j
# (verificar que a pasta atual é $HOME/desarquivo) senão atualizar
docker run --interactive --tty --rm \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/desarquivo/neo4j/data:/data \
    --volume=$HOME/desarquivo/neo4j/import:/import \
    --user="$(id -u):$(id -g)" \
    neo4j:latest \
neo4j-admin import --id-type=STRING --nodes=/import/i_entities.csv --relationships=rel=/import/i_connections.csv

# iniciar o docker-compose
docker-compose up -d

# se aceder a IP:7474 verá o interface do neo4j, para o esconder do
# público editar as portas do serviço neo4j no docker-compose
...
# quando os 3 containers estiverem a correr
# instalar mongorestore no servidor (fora dos containers) -> pesquisar instruções mais recentes online
...
# importar os dados para o neo4j
# carregar o dataset02.zip para o servidor
unzip dataset02.zip -d dataset02
cd dataset02

# usar o mongorestore para importar para a isntância mongo
# -d é o nome da base de dados
# . é a pasta atual onde estarão os .bson e .json
mongorestore -u USER -p PASSWORD --authenticationDatabase admin --uri="mongodb://localhost:27017/" -d desarquivo . 

# feito.
# basta aceder a IP:80 para aceder à API que estará ligada a ambas as bases de dados, com os dados carregados
```


<p align="center"><img src="https://i.imgur.com/wNThGU0.png"/></p>

## Criação do Desarquivo

O Desarquivo é uma junção de diferentes peças que se encontram descritas abaixo.

### Recolha e Limpeza de Dados

Cujo código se encontra na pasta [collection](collection/) e que diz respeito à interação com as [APIs do Arquivo.pt](https://github.com/arquivo/pwa-technologies/wiki/APIs) e com a respetiva organização na base de dados MongoDB. Há a realçar que o processo tira partido de parallelismo o que, na prática, resulta numa redução de mais de uma ordem de grandeza no tempo total de recolha. Os demais pormenores estão explicados no ficheiro de instruções na dita [pasta](collection/).

### API

A API foi desenvolvida em [Flask](https://flask.palletsprojects.com/en/1.1.x/) e todo o respetivo código encontra-se na pasta [api](api/). Este diz respeito à interação com ambas as bases de dados (MongoDB e neo4j).

### A Interface

A Interface, desenvolvida em [Vue.js](https://vuejs.org/) com [Nuxt.js](https://nuxtjs.org/) e [Vuetify](https://vuetifyjs.com/en/) e com recurso à biblioteca [cytoscape.js](https://js.cytoscape.org/) para a visualização do grafo. Todo o código respetivo encontra-se na pasta [ui](ui/). A interface está preparada para ser automaticamente colocada em produção em [gh-pages](https://pages.github.com/).

## Docker

À exceção da interface e do processo de recolha de dados, as restantes partes do Desarquivo (API, MongoDB, neo4j) encontram-se em containers Docker o que significa que há uma maior flexibilidade e interoperabilidade quer no desenvolvimento quer em produção. Os comandos mais importantes para orquestrar estes serviços são

- `docker-compose up -d`
- `docker-compose down`

De realçar que se o projeto for executado em Windows, é necessário desativar o volume do serviço mongodb.

## Futuro do Desarquivo

O Desarquivo continuará a ser melhorado e procurará tornar-se uma ferramenta mais completa que se afirma como defensora de transparência, liberdade de expressão, e investigação jornalística. As possibilidades são inúmeras e as ideias também. Se te revês neste projeto e acreditas que faz sentido, considera contribuir com tempo, conselhos, ou ideais.

Para entrar em contacto comigo, utiliza o [LinkedIn](https://www.linkedin.com/in/msramalho/).

Agradecemos sugestões de melhoria e identificação de erros. Nesses casos, usem os [issues](https://github.com/msramalho/desarquivo/issues) do Github.
