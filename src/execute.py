from requests_html import HTMLSession
from lxml import html
from lxml.etree import tostring
from datetime import datetime
from pathlib import Path
import re
import random

from links import store
from models import Job, Link
from store import insert_job, insert_link
from telegram import send_message


CACHE_FOLDER = "__html__"
BASE_URL = "https://uk.indeed.com"

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
	"Accept-Encoding": "",
	"referer": "https://uk.indeed.com/"
}

def main():
	s = HTMLSession()
	s.headers.update(headers)

	query = "elixir"

	scraping = True
	first_job = None
	page = 0

	while scraping:
		url = f"{BASE_URL}/jobs?q={query}&l=London&start={page * 10}"

		raw_html = fetch_html_cache(s, url)
		tree = html.fromstring(raw_html)
		container = tree.xpath('//*[@id="mosaic-provider-jobcards"]')[0]

		jobs = []

		children = container.getchildren()
		counter = 0
		for c in children:
			if c.tag != "a":
				continue

			job = html_to_job(s, c)

			if first_job is not None and job.url == first_job.url:
				scraping = False
				break

			if counter == 0:
				first_job = job

			jobs.append(job)

			insert_job(job)

			counter += 1

		send_message(f"Scraped page {page + 1}")
		print(f"Scraped page {page + 1}")
		page += 1

	send_message("Job completed! Scaped all pages")


def fetch_html_cache(s, url):
	wait = random.uniform(2, 10)

	Path(f"./{CACHE_FOLDER}").mkdir(parents=True, exist_ok=True)

	link = insert_link(Link(None, url, 0, None))
	short_key = link.short_key
	
	date = datetime.today().strftime("%b_%d_%Y")

	file_name = f"{short_key}_{date}.html"

	cache_file = Path(f"./{CACHE_FOLDER}/{file_name}")
	if cache_file.is_file():
		f = open(f"./{CACHE_FOLDER}/{file_name}", "r")

		return f.read()

	with open(f"./{CACHE_FOLDER}/{file_name}", "w") as outfile:
		r = s.get(url)

		r.html.render(sleep=wait, timeout=200)

		outfile.write(r.html.html)
		outfile.close()

	return r.html.html


def html_to_job(s, raw_html) -> Job:
	href = raw_html.get("href")
	title = fetch_title(raw_html)
	address = fetch_address(raw_html)

	salary_low = 0
	salary_high = 0
	(salary_raw, salary_low, salary_high) = fetch_salary(raw_html)

	company_name = fetch_company_name(raw_html)

	job_url = f"{BASE_URL}{href}"

	raw_html = fetch_html_cache(s, job_url)
	tree = html.fromstring(raw_html)
	content = tree.xpath('//*[@id="viewJobSSRRoot"]/div/div[3]/div/div/div[1]/div[1]/div[4]')[0]
	
	pattern = re.compile('<.*?>')
	content_html = tostring(content, encoding='unicode')
	content_text = re.sub(pattern, '', content_html)

	return Job(
		"", 
		title, 
		job_url, 
		content_text, 
		content_html, 
		company_name, 
		salary_raw, 
		salary_low, 
		salary_high, 
		address
	)


def fetch_title(raw_html):
	return raw_html.xpath('./div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/span')[0].text


def fetch_address(raw_html):
	el = raw_html.xpath('./div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/pre/div')[0]
	return ''.join(el.itertext())


def fetch_salary(raw_html) -> tuple:
	el = raw_html.xpath('./div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[3]/div/div/span')
	salary_raw = None
	if len(el) > 0:
		salary_raw = el[0].text

	if salary_raw is not None:
		return fetch_low_high_salary(salary_raw)
			
	return (salary_raw, 0, 0)


def fetch_low_high_salary(raw: str) -> tuple:
	regex = r"(£[0-9]*,[0-9]*)"

	matches = re.finditer(regex, raw, re.MULTILINE)

	salaries = ()
	for _, match in enumerate(matches, start=1):
		salaries = salaries + (salary_from_string(match.group()),)

	if len(salaries) == 0:
		salaries = (0, 0)

	if len(salaries) == 1:
		salaries = salaries + salaries

	return (raw,) + salaries


def fetch_company_name(raw_html) -> str:
	el = raw_html.xpath('./div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/pre/span')
	if len(el) == 0:
		return None

	el = el[0]

	el_children = el.getchildren()
	if len(el_children) > 0:
		company_name = el_children[0].text
	else:
		company_name = el.text

	return company_name


def salary_from_string(salary: str) -> int:
	return int(salary.strip("£").replace(",", ""))

if __name__ == "__main__":
	main()