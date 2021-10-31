import sqlite3

from models import Job, Link

conn = sqlite3.connect("store.db", check_same_thread=False)

def insert_job(job : Job, conn=conn) -> Job:
	cursor = conn.cursor()
	query = """INSERT OR IGNORE INTO jobs (
		job_id, 
		title, 
		url, 
		description_text, 
		description_html, 
		company, 
		salary_raw, 
		salary_low, 
		salary_high,
		address
	) VALUES (
		?, ?, ?, ?, ?, ?, ?, ?, ?, ?
	)"""
	
	records = [(
		job.job_id,
		job.title,
		job.url,
		job.description_text,
		job.description_html,
		job.company,
		job.salary_raw,
		job.salary_low,
		job.salary_high,
		job.address
	)]

	cursor.executemany(query, records)

	conn.commit()

	job.id = cursor.lastrowid

	cursor.close()

	return job


def get_all_jobs(conn=conn) -> list:
	cursor = conn.cursor()
	rows = cursor.execute("SELECT * FROM jobs").fetchall()

	return to_jobs(rows)


def to_jobs(rows) -> list:
	results = []
	for r in rows: 
		results.append(to_job(r))
	
	return results


def to_job(row) -> Job:
	f = Job(*row[1:])

	f.id = row[0]

	return f


def insert_link(link : Link, conn=conn) -> Link:
	found_link = get_link_by_url(link.url)
	if found_link is not None:
		return found_link

	cursor = conn.cursor()
	query = """INSERT OR IGNORE INTO links (
		short_key, 
		url, 
		clicks, 
		active
	) VALUES (
		?, ?, ?, ?
	)"""
	
	records = [(
		link.short_key,
		link.url,
		link.clicks,
		link.active,
	)]

	cursor.executemany(query, records)

	conn.commit()

	link.id = cursor.lastrowid

	cursor.close()

	return link


def get_all_links(conn=conn) -> list:
	cursor = conn.cursor()
	rows = cursor.execute("SELECT * FROM links").fetchmany()
	
	return to_links(rows)


def get_link_by_url(url: str, conn=conn) -> Link:
	cursor = conn.cursor()
	rows = cursor.execute("SELECT * FROM links WHERE url = ?", [url]).fetchmany()
	
	links = to_links(rows)
	if len(links) == 0:
		return None

	return links[0]


def get_link_by_short_key(short_key: str, conn=conn) -> Link:
	cursor = conn.cursor()
	rows = cursor.execute("SELECT * FROM links WHERE short_key = ?", [short_key]).fetchmany()
	
	links = to_links(rows)
	if len(links) == 0:
		return None

	return links[0]


def to_links(rows) -> list:
	results = []
	for r in rows: 
		results.append(to_link(r))
	
	return results


def to_link(row) -> Link:
	l = Link(*row[1:])

	l.id = row[0]

	return l