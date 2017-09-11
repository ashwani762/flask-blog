CREATE TABLE users(id integer PRIMARY KEY AUTOINCREMENT NOT NULL ,name varchar(100),email varchar(100),username varchar(30),password varchar(100),register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

select * from users;

DROP TABLE users;