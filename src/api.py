from flask import Flask, jsonify, redirect
import os

from store import get_all_jobs, get_all_links, get_link_by_short_key

app = Flask(__name__)

@app.route('/')
@app.route('/jobs')
def jobs():
	jobs = get_all_jobs()

	result = []
	for j in jobs:
		result.append(vars(j))

	return jsonify(result)


@app.route('/links')
def links():
	links = get_all_links()

	result = []
	for l in links:
		result.append(vars(l))

	return jsonify(result)


@app.route('/job/<short_key>')
def job(short_key):
	link = get_link_by_short_key(short_key)

	return redirect(link.url, code=307)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("HTTP_PORT", 5000)))