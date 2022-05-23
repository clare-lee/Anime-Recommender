# Anime Recommender System

## Setup & Installation 

> git clone <repo-url>

> python -m pip install scipy flask flask-sqlalchemy flask-login sqlalchemy werkzeug pandas PyMySql scikit-learn

## Setup Database 
Install or have MySQL installed
  
Login MySQL 
```sql
mysql -u root -p;
```
  
Create Database
Create Table 
Load Data
```sql
SOURCE CreateTables.sql;
```

## Running the App 

> python main.py

## Viewing the App 

> http://127.0.0.1:5000/

## In the case of errors when loading data
On MySQL load with

LOAD DATA LOCAL INFILE 'anime.csv' INTO TABLE anime FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'ratings.csv' INTO TABLE rating FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;

OR 

On MySQL workbenchTable for anime and rating load anime.csv and rating.csv respectively using Table Data Import Wizard 
