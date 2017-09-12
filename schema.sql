CREATE TABLE users(id integer PRIMARY KEY AUTOINCREMENT NOT NULL ,name varchar(100),email varchar(100),username varchar(30),password varchar(100),register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

select * from users;

DROP TABLE users;

SELECT password from users where username = "ashwani";


create table articles(id integer PRIMARY KEY AUTOINCREMENT , title varchar(255), author varchar(100), body text, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

select * from articles;

SELECT * from sqlite_master WHERE type='table';