CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
	job_id VARCHAR(255),
	title VARCHAR(255),
	url VARCHAR(255),
	description_text TEXT,
	description_html TEXT,
	company VARCHAR(255),
	salary_raw VARCHAR(255),
	salary_low INT,
	salary_high INT,
	address VARCHAR(255),
	created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY,
	short_key VARCHAR(255) UNIQUE,
	url VARCHAR(255) UNIQUE,
	clicks INT,
	active INT DEFAULT 1,
	created DATETIME DEFAULT CURRENT_TIMESTAMP
);


