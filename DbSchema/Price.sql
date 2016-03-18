CREATE TABLE IF NOT EXISTS EthBtcPrice (
	id INTEGER NOT NULL auto_increment PRIMARY KEY,  
	timestamp TIMESTAMP UNIQUE, 
	eth_btc_price FLOAT
)