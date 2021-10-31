import random
import string

from links import gen_short_url


class Job():

	def __init__(
		self, 
		job_id, 
		title,
		url,
		description_text,
		description_html,
		company,
		salary_raw,
		salary_low,
		salary_high,
		address,
		created = None):

		self.id = None
		self.job_id = str(job_id)
		self.title = title
		self.url = url
		self.description_text = description_text
		self.description_html = description_html
		self.company = company
		self.salary_raw = salary_raw
		self.salary_low = salary_low
		self.salary_high = salary_high
		self.address = address
		self.created = created


class Link():

	def __init__(
		self, 
		short_key, 
		url,
		clicks,
		active,
		created = None):

		self.id = None
		self.short_key = short_key
		self.url = url
		self.clicks = clicks
		self.created = created
		
		if active == 1:
			self.active = True
		else:
			self.active = False

		if short_key == None:
			self.short_key = self.gen_short_url()
		else:
			self.short_key = short_key

	def gen_short_url(self) -> str:
		length = 6
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))