CREATE TABLE IF NOT EXISTS BitMexPrice (
	id INTEGER NOT NULL auto_increment PRIMARY KEY,  
	timestamp TIMESTAMP UNIQUE, 
	price FLOAT,
	size INT
);


CREATE TABLE IF NOT EXISTS BitMexTrades (
	id INTEGER NOT NULL auto_increment PRIMARY KEY,
	timestamp TIMESTAMP UNIQUE,
	trades INT,
	volume INT,
	lastSize INT
);