/*Bitfinix data*/

CREATE TABLE IF NOT EXISTS BfxTicker (
	id INTEGER NOT NULL auto_increment PRIMARY KEY,  
	timestamp TIMESTAMP UNIQUE,
	mid FLOAT,
	bid FLOAT,
	ask FLOAT,
	last_price FLOAT,
	24_hr_low FLOAT,
	24_hr_high FLOAT,
	24_hr_volume FLOAT
);



/* bid=1 if type is 'bid', =0 if type is 'ask' */

CREATE TABLE IF NOT EXISTS BfxTrades (
	id INTEGER NOT NULL auto_increment PRIMARY KEY,  
	txn_id INT UNIQUE,
	timestamp TIMESTAMP,
	buy BOOL,
	price FLOAT,
	amount FLOAT,
	exchange VARCHAR(64)
);



/* bid=1 if type is 'bid', =0 if type is 'ask' */

CREATE TABLE IF NOT EXISTS BfxBook (
	id INTEGER NOT NULL auto_increment PRIMARY KEY,  
	timestamp TIMESTAMP,
	buy BOOL,
	price FLOAT,
	amount FLOAT
);


CREATE UNIQUE INDEX book_entry ON BfxBook (timestamp, price, amount);