from scrapy import Request, Spider
from scrapy_splash import SplashRequest
import re


class IndeedSpider(Spider):

	name = "indeed"

	base_url = "https://uk.indeed.com"

	page = 0

	query = "python"

	def start_requests(self):
		yield SplashRequest(
			self.__get_url(), 
			callback=self.__parse_jobs_list_page,
			endpoint="render.html",
			args={"wait": 0.5}
		)

	def __parse_jobs_list_page(self, response):
		# container = response.xpath('//*[@id="sj_3e20138464b2a632"]/div[1]/div/div[1]/div').getall()
		container = response.css("div#mosaic-provider-jobcards")
		for job in container.xpath("./a"):
			yield {
				"page_url": response.url,
				"url": self.base_url + job.attrib["href"],
				"title": job.xpath("./div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/span/text()").get(),
				"company": self.__extract_company_name(job),
				"location": job.css("div.companyLocation::text").get(),
				"salary_range": self.__extract_salary_range(job)
			}

	def __get_url(self):
		return f"{self.base_url}/jobs?q={self.query}&l=London&start={self.page * 10}"

	def __extract_company_name(self, job):
		company_name = job.css("span.companyName::text").get()
		if company_name is not None:
			return company_name

		return job.css("span.companyName a::text").get()

	def __extract_salary_range(self, job):
		salary_range = job.css("div.salary-snippet span::text").get()
		if salary_range is not None:
			return self.__parse_salary_range(salary_range)

		return None

	def __parse_salary_range(self, raw_salary) -> dict:
		regex = r"(£[0-9]*,[0-9]*)"

		matches = re.finditer(regex, raw_salary, re.MULTILINE)

		salaries = ()
		for _, match in enumerate(matches, start=1):
			salaries = salaries + (self.__salary_from_string(match.group()),)

		if len(salaries) != 2:
			return None

		return {
			"salary_low": salaries[0],
			"salary_high": salaries[1]
		}

	def __salary_from_string(self, salary: str) -> int:
		return int(salary.strip("£").replace(",", ""))
	