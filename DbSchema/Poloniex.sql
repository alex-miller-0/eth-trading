CREATE TABLE IF NOT EXISTS PoloCharts (
	id INTEGER NOT NULL auto_increment PRIMARY KEY,  
	date INTEGER UNIQUE,
	high FLOAT,
	low FLOAT,
	open FLOAT,
	close FLOAT,
	volume FLOAT,
	quoteVolume FLOAT,
	weightedAverage FLOAT
);