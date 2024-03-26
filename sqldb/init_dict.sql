CREATE DATABASE IF NOT EXISTS Puflantu

CREATE TABLE dictionary (
    ID int NOT NULL, 
    Puflantu VARCHAR(64), 
    English VARCHAR(64),
    PRIMARY KEY (ID)
);

LOAD DATA LOCAL INFILE '/home/user/GitHub/Puflantu/dictionary.csv' 
INTO TABLE dictionary 
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\n';