import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

API_TOKEN = "A234tvgh0sdfgv"
OW_API_KEY = "3896a9d8346e84f00c3788c4d3321efd"

app = Flask(__name__)


def get_weather(location, date):
	url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&dt={date}&appid={OW_API_KEY}"
	resp = requests.request("GET", url)
	return json.loads(resp.text)


class InvalidUsage(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv["message"] = self.message
		return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


@app.route("/")
def home_page():
	return "<p><h2>Homework 1: SaaS by Mykhailo Halaida</h2></p>"


@app.route(
	"/weather",
	methods=["POST"],
)
def weather_endpoint():
	params = request.get_json()

	if params.get("token") is None:
		raise InvalidUsage("token is required", status_code=400)

	token = params.get("token")

	if token != API_TOKEN:
		raise InvalidUsage("wrong API token", status_code=403)

	location = params.get("location")
	date = params.get("date")
	requester_name = params.get("requester_name")

	weather = get_weather(location, date)

	result = {
		"requester_name": requester_name, 
		"timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		"location": location, 
		"date": date, 
		"weather": weather
	}

	return result