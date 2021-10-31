from pathlib import Path
import json
import random
import string

JSON_FILE = "./url_map.json"

def store(url: str) -> str:
	short_key = gen_short_url()

	json_file = Path(JSON_FILE)
	if json_file.is_file() == False:
		data = {}
		data[url] = short_key

		with open(JSON_FILE, "w") as json_file:
			json.dump(data, json_file)

	else:
		found_key = lookup_url(url)
		if found_key is not None:
			return found_key
			
		with open(JSON_FILE, "r") as json_file:
			data = json.load(json_file)
		
		data[url] = short_key

		with open(JSON_FILE, "w") as json_file:
			json.dump(data, json_file)

	return short_key


def lookup_key(short_key: str) -> str:
	with open(JSON_FILE, "r") as json_file:
		data = json.load(json_file)

	for (url, key) in data.items():
		if key == short_key:
			return url

	return None


def lookup_url(url: str) -> str:
	with open(JSON_FILE, "r") as json_file:
		data = json.load(json_file)

	if url in data:
		return data[url]

	return None


def gen_short_url() -> str:
	length = 6
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
