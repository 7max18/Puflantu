CREATE DATABASE IF NOT EXISTS Puflantu;
USE Puflantu
DROP TABLE IF EXISTS dictionary;
CREATE TABLE dictionary(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    puflantu VARCHAR(64), 
    english VARCHAR(64)
);

LOAD DATA LOCAL INFILE '/home/user/GitHub/Puflantu/server/app/sql/dictionary.csv' 
INTO TABLE dictionary 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n';