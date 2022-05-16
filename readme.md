# Anime Recommender System

<h2> Setup & Installation </h2>

> git clone <repo-url>

> python3.9 -m pip install scipy flask flask-sqlalchemy flask-login sqlalchemy werkzeug pandas

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
> Using CreateTable.sql
  
Load Table
```sql
LOAD DATA LOCAL INFILE 'path to anime.csv' INTO TABLE anime FIELDS TERMINATED BY ',' IGNORE 1 LINES;
```

<h2> Running the App </h2>
  
> python3.9 main.py

<h2> Viewing the App </h2>
