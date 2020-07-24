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

* As primeiras entidades a investigar e que dão origem à expansão da rede - nesta versão, foram `José Sócrates` e `Isabel dos Santos`
* O período de tempo a incluir - nesta versão, entre o ano `2000` e o ano `2020`
* Os jornais a procurar - nesta versão, foram [Público](https://www.publico.pt/), [Expresso](https://expresso.pt/), [Diário de Notícias](https://www.dn.pt/), [Correio da Manhã](https://www.cmjornal.pt/), [Sol](https://sol.sapo.pt/), [Visão](https://visao.sapo.pt/) e [Jornal de Notícias](https://www.jn.pt/)

As notícias recolhidas foram analisadas e de lá foram extraídas entidades (pessoas, organizações, lugares, entre outras) e respetivas relações. Estas relações formam uma rede imensa que é agora explorável nesta interface gráfica ou diretamente nos dados que são de [livre acesso]DATASETS.md).

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


### Investigadores
Podem ainda aceder aos [datasets](DATASETS.md) disponibilizados e executar _queries_ mais complexas sobre os grafos gerados.

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
* `docker-compose up -d`
* `docker-compose down`

De realçar que se o projeto for executado em Windows, é necessário desativar o volume do serviço mongodb.

## Futuro do Desarquivo
O Desarquivo continuará a ser melhorado e procurará tornar-se uma ferramenta mais completa que se afirma como defensora de transparência, liberdade de expressão, e investigação jornalística. As possibilidades são inúmeras e as ideias também. Se te revês neste projeto e acreditas que faz sentido, considera contribuir com tempo, conselhos, ou investimento financeiro. 

Para entrar em contacto comigo, utiliza o [LinkedIn](https://www.linkedin.com/in/msramalho/). 

Agradecemos sugestões de melhoria e identificação de erros. Nesses casos, usem os [issues](https://github.com/msramalho/desarquivo/issues) do Github. 
