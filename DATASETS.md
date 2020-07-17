# Dados
(english below)

Os dados disponibilizados dizem respeito a notícias e entidades recolhidas no âmbito deste projeto.

## MongoDB
Para usar estes datasets deve ter uma instância de [mongodb](https://www.mongodb.com/) a correr e para onde possa importar dados. Deverá extrair os ficheiros zipados e, de seguida, invocar o comando `mongorestore -d desarquivo <PASTA_COM_FICHEIROS>`

* [Dataset 01](https://drive.google.com/file/d/11b11LPIBqFUYE-ifyBjyIv1boC9P5iN2/view?usp=sharing) - Conjunto das notícias (depois de limpeza não trivial de duplicados) e entidades extraídas, este dataset foi posteriormente filtrado para gerar o 2o dataset com um número mais limitado de entidades de forma a garantir a sua relevância.
* [Dataset 02](https://drive.google.com/file/d/18_8RBlrzKO6cVShUZBZZMs930m1Ga3TG/view?usp=sharing) - Conjunto final de notícias e entidades diretamente apresentadas na versão atual do desarquivo


## Neo4J
Para usar estes dataset deve ter uma instância de [neo4j](https://neo4j.com/) vazia. Deve colocar os ficheiros disponibilizados na pasta `/import` dessa instância e correr o comando

### Dataset 03
Grafo de ligações entre entidades.

##### Versão 1: [Dataset 03 a](https://drive.google.com/file/d/1NUtgr7UyNtYMEU4Env9TqeVwFxIIe8rA/view?usp=sharing) (mais rápida)
 `neo4j-admin import --id-type=STRING --nodes=import/i_entities.csv --relationships=rel=import/i_connections.csv`

 ou

##### Versão 2: [Dataset 03 b](https://drive.google.com/file/d/12VrehvB6j0QVE6B_vAfTIPBAYZ1oytWl/view?usp=sharing) (mais lenta)

```sql
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (e:PER {_id: row._id, text: row.text});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///orgs.csv' AS row
MERGE (e:ORG {_id: row._id, text: row.text});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///locations.csv' AS row
MERGE (e:LOC {_id: row._id, text: row.text});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///misc.csv' AS row
MERGE (e:MISC {_id: row._id, text: row.text});



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///news.csv' AS row
MERGE (n:NEWS {_id: row._id, title: row.title});



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///connections_1.csv' AS row
MERGE (e1 {_id: row._id1})
MERGE (e2 {_id: row._id2})
WITH row, e1, e2
MERGE (e1)-[:rel{weight: toInteger(row.weight)}]-(e2);
```
Exemplo de visualização no neo4j-browser do dataset 3:
![](https://i.imgur.com/wNThGU0.png)

### Dataset 04
Grafo de ligações entre entidades e notícias (neste caso não foi preparado o comando com o `neo4j-import` mas aconselha-se esse face à opção `LOAD CSV` para datasets grandes) os dados são os mesmos do [dataset 03 b](https://drive.google.com/file/d/12VrehvB6j0QVE6B_vAfTIPBAYZ1oytWl/view?usp=sharing) mas, ao importar, são reorganizados de outra forma gerando um nó no grafo para cada notícia

```sql
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (e:PER {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///orgs.csv' AS row
MERGE (e:ORG {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///locations.csv' AS row
MERGE (e:LOC {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///misc.csv' AS row
MERGE (e:MISC {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///news.csv' AS row
MERGE (n:NEWS {_id: row._id, title: row.title});



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///connections_1.csv' AS row
MERGE (e1 {_id: row._id1})
MERGE (e2 {_id: row._id2})
WITH row, e1, e2
MERGE (e1)-[:rel{weight: toInteger(row.weight), news: split(row.news, ',')}]-(e2);
```

---
---
# Data
(english below)

The available data are related to news and entities collected in the scope of this project.

## MongoDB
To use these datasets, you should have a running instance of [mongodb](https://www.mongodb.com/) where you can import data. After download, you need to unzip the files and then invoke the command `mongorestore -d desarquivo <PATH_TO_FOLDER_WITH_FILES>`

* [Dataset 01](https://drive.google.com/file/d/11b11LPIBqFUYE-ifyBjyIv1boC9P5iN2/view?usp=sharing) - Set of news (after a non-trivial de-duplication process) and entities extracted, this dataset was later filtered to generate the 2nd dataset with a more limited number of entities in order to ensure relevance. 
* [Dataset 02](https://drive.google.com/file/d/18_8RBlrzKO6cVShUZBZZMs930m1Ga3TG/view?usp=sharing) - Final set of news and entities directly presented in the current version of Desarquivo. 

## Neo4J
To use these datasets, you need an empty running instance of [neo4j](https://neo4j.com/). You should place the provided files in the `/import` folder of that instance and then run the appropriate command. 

### Dataset 03
Entity relationships graph

##### Version 1: [Dataset 03 a](https://drive.google.com/file/d/1NUtgr7UyNtYMEU4Env9TqeVwFxIIe8rA/view?usp=sharing) (faster)
 `neo4j-admin import --id-type=STRING --nodes=import/i_entities.csv --relationships=rel=import/i_connections.csv`

 or

##### Version 2: [Dataset 03 b](https://drive.google.com/file/d/12VrehvB6j0QVE6B_vAfTIPBAYZ1oytWl/view?usp=sharing) (slower)

```sql
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (e:PER {_id: row._id, text: row.text});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///orgs.csv' AS row
MERGE (e:ORG {_id: row._id, text: row.text});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///locations.csv' AS row
MERGE (e:LOC {_id: row._id, text: row.text});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///misc.csv' AS row
MERGE (e:MISC {_id: row._id, text: row.text});



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///news.csv' AS row
MERGE (n:NEWS {_id: row._id, title: row.title});



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///connections_1.csv' AS row
MERGE (e1 {_id: row._id1})
MERGE (e2 {_id: row._id2})
WITH row, e1, e2
MERGE (e1)-[:rel{weight: toInteger(row.weight)}]-(e2);
```
Example of visualization of dataset 3 in neo4j-browser:

![](https://i.imgur.com/wNThGU0.png)

### Dataset 04
Graph of connection between entities and news (in this case prepared with the `neo4j-import` command, which is recommended over `LOAD CSV` for larger datasets). The data is the same as in [dataset 03 b](https://drive.google.com/file/d/12VrehvB6j0QVE6B_vAfTIPBAYZ1oytWl/view?usp=sharing) but, when you import them, they are re-organized differently, generating a node in the graph for each news article, leaving you with a much larger but potentially richer graph. 

```sql
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (e:PER {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///orgs.csv' AS row
MERGE (e:ORG {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///locations.csv' AS row
MERGE (e:LOC {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///misc.csv' AS row
MERGE (e:MISC {_id: row._id, text: row.text})
WITH row, e
UNWIND split(row.news, ',') AS news_piece
MERGE (n:NEWS {_id: news_piece})
MERGE (e)-[:liga]-(n);



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///news.csv' AS row
MERGE (n:NEWS {_id: row._id, title: row.title});



USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///connections_1.csv' AS row
MERGE (e1 {_id: row._id1})
MERGE (e2 {_id: row._id2})
WITH row, e1, e2
MERGE (e1)-[:rel{weight: toInteger(row.weight), news: split(row.news, ',')}]-(e2);
```