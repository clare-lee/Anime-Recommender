# Anime Recommender System

<h2> Setup & Installation </h2>

> git clone <repo-url>

> python -m pip install scipy flask flask-sqlalchemy flask-login sqlalchemy werkzeug pandas PyMySql

<h2> Setup Database </h2>
  
Login MySQL 
```sql
mysql -u root -p;
```
  
Create Database
```sql
CREATE DATABASE Recommender;  
```  

Create Table
```sql
USE Recommender;
SOURCE CreateTables.sql;
```
  
Load Table
```sql
LOAD DATA LOCAL INFILE 'path to anime.csv' INTO TABLE anime FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'path to ratings.csv' INTO TABLE rating FIELDS TERMINATED BY ',' IGNORE 1 LINES;
```

<h2> Running the App </h2>
  
> python main.py

<h2> Viewing the App </h2>

> http://127.0.0.1:5000/
