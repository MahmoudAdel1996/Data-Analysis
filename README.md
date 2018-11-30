# About the logs analysis project:
Through this project we can draw important data from the database such as how
many views of the article and famous authors and errors that occurred during
the day, the output will be a plain text file.


## Source of Database:
you can download it from [Here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

to import use this
```
$ psql -d [databaseName] -f newsdata.sql
``` 
## About Database:
connect to Database with this command
```
$ psql [databaseName]
```
To show all table on Database
```
[databaseName]=> \dt
```
To show details of certain table
```
[databaseName]=> \d [tableName]
```
To show all data table on Database
```SQL
[databaseName]=> SELECT * FROM [tableName]

```


## Install:
we use PostgreSQL to install it u can type in your terminal

```
$ pip install psycopg2
```


## How to use:
```python
import psycopg2
db = psycopg2.connect(database='databaseName')
c = db.cursor()
c.execute(query)
data = c.fetchall()
```
to write in file
```python
with open('output.txt', 'w') as out:
    out.write("Type some thing here")
```


## Example:
this function return list of tuple of all colums data from toparticles table.
```python
def most_popular_articles():
    query = "select * from toparticles limit 3;"
    c.execute(query)
    data = c.fetchall()
    return data
```


## Created Views:
```sql
CREATE OR REPLACE VIEW toparticles AS
SELECT articles.title,
       count(*) AS VIEW
FROM articles,
     log
WHERE PATH LIKE '%' || slug || '%'
  AND status = '200 OK'
GROUP BY articles.title
ORDER BY view DESC;
```
    
```sql
CREATE OR REPLACE VIEW popular AS
SELECT A.title,
       authors.name AS author,
       VIEW
FROM
  (SELECT toparticles.title,
          articles.author,
          VIEW
   FROM toparticles,
        articles
   WHERE toparticles.title = articles.title
   ORDER BY VIEW DESC) AS A,
     authors
WHERE A.author = authors.id;
```

```sql
CREATE OR REPLACE VIEW error AS
SELECT (cast(errorstate.error AS decimal)/
          allstate.error)*100 AS error,
          errorstate.date
FROM(SELECT TIME::date AS date, count(*) AS error
      FROM log
      WHERE status != '200 OK'
      GROUP BY date) AS errorstate,
    (SELECT TIME::date AS date, count(*) AS error
      FROM log
      GROUP BY date) AS allstate
WHERE errorstate.date = allstate.date;
```


## How to run the code:
```
$ python3 newsdb.py
```
