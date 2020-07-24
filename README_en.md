<!-- <h1 align="center">Desarquivo</h1> -->

<p align="center">
<a href="https://msramalho.github.io/desarquivo/" >
<img height="100px" src="https://i.imgur.com/bbqpudq.gif" />
</a>
<br>
<br>
<i>A project that seeks to democratize and complement <u>investigative journalism</u> and <u>fact-checking</u>.
<br>
Arquivo.pt for justice, journalism and truth.</i>
<br>
<br>
Um projeto que procura democratizar e complementar o <u>jornalismo de investigação</u> e a <u>verificação de factos</u>. 
<br>
Arquivo.pt para justiça, jornalismo e verdade.
<br>
<h3 align="center"><a href="README.md">Versão em Português</a></h3>
</p>

## About the Project
Desarquivo is designed as a reproducible effort based on a set of configurations from which we highlight:

* The first investigated entities, the ones that lead to the subsequent network expansion. In this version, these are `José Sócrates` (ex prime-minister of Portugal) and `Isabel dos Santos` (from Luanda Leaks)
* The period of time to include in the current version, which is between the year `2000` and `2020`
* The newspapers to search - in this version: [Público](https://www.publico.pt/), [Expresso](https://expresso.pt/), [Diário de Notícias](https://www.dn.pt/), [Correio da Manhã](https://www.cmjornal.pt/), [Sol](https://sol.sapo.pt/), [Visão](https://visao.sapo.pt/) and [Jornal de Notícias](https://www.jn.pt/)

The collected news were analysed and the entities they mentioned were identified <small>(people, organizations, places, and others)</small> along with their links. These links form an immense network which is now exploitable in this graphical interface, or directly in the [open sourced](DATASETS.md) raw data.

Desarquivo rests on two databases, namely [MongoDB](https://www.mongodb.com/) (NoSQL) and [neo4j](https://neo4j.com/) (Graphs).

<p align="center">
   <a href="https://youtu.be/tVlOUuRqIVU" >
      <img height="200px" src="https://i.imgur.com/0sHj6Fi.png"/>
   </a>
   <br>
   Presentation video (only in Portuguese)
</p>

### Citizens
Can access[desarquivo](https://msramalho.github.io/desarquivo/) and explore its different functionalities and examples. 

<p align="center"><img src="https://i.imgur.com/NRxBO0h.png"/></p>


### Researchers
Can access our available [datasets](DATASETS.md) and run more complex queries on the generated graphs.

<p align="center"><img src="https://i.imgur.com/wNThGU0.png"/></p>

## Building Desarquivo
Desarquivo is a puzzle with many pieces, as described below.

### Data Collection and Preparation
The code for this piece is available in the [collection](collection/) folder. It is related to the interaction with the [Arquivo.pt APIs](https://github.com/arquivo/pwa-technologies/wiki/APIs) and with the subsequent organization of data in the MongoDB database. It should be noted that this process runs many tasks in parallel, in practice, this means a reduction of over one order of magnitude to the total data collection time. Other details are explained in the mentioned [folder](collection/).

### API
The API is built on [Flask](https://flask.palletsprojects.com/en/1.1.x/) and all its code is available in the [api](api/) folder. This code interacts with both of our databases (MongoDB and neo4j). 

### The Interface
The Interface, developed in [Vue.js](https://vuejs.org/) with [Nuxt.js](https://nuxtjs.org/) and [Vuetify](https://vuetifyjs.com/en/), and also eith the [cytoscape.js](https://js.cytoscape.org/) library for the graph visualization. All the code for the interface is in the [ui](ui/) folder. The interface is also ready to be automatically deployed to production with [gh-pages](https://pages.github.com/).

## Docker
Excluding the collection process and the interface, all the remaining parts of Desarquivo (API, MongoDB, neo4j) can ve found in Docker containers, meaning there is a high flexibility in the development and production phases. The most important commands for the orchestration of these services are:
* `docker-compose up -d`
* `docker-compose down`

It should be noted that, at the moment, if the project is executed on Windows it is necessary to deactivate the volume in the mongodb service.

## Future of Desarquivo
Desarquivo will continue being improved and can grow into a more comprehensive tool that stands for transparency, freedom of speech, and journalistic investigation. The possibilities are many, and the ideas too. If you relate to these project and believe in it, we ask you to contribute with time, advice, or ideas. 

To get in touch with me, please use [LinkedIn](https://www.linkedin.com/in/msramalho/). 

We welcome all suggestions and bugs. For that, please use the [issues](https://github.com/msramalho/desarquivo/issues) page. 
