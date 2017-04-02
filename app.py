from flask import Flask, request, jsonify
from chatter_bot import ChatterBot
from movie_name_finder import MovieNameFinder
from restaurant_name_finder import RestaurantNameFinder
import os, requests

app = Flask(__name__)
my_dir = os.path.dirname(__file__)

# cb = ChatterBot()
mf = MovieNameFinder()
rf = RestaurantNameFinder()

env = {}
file = os.path.join(my_dir, '.env')
with open(file, "r") as f:
	for line in f:
		line = line.rstrip()
		tokens = line.split("=")
		env[tokens[0]] = tokens[1]

@app.route('/get-reply', methods=['POST'])
def get_reply():
	json = request.json
	message = json["message"]
	reply = {}
	movie_name = mf.get_movie_name(message)
	if not movie_name:
		location = get_location(message)
		restaurant_name = rf.get_restaurant_name(message, location)

		if not restaurant_name:
			reply = {"code": 3, "name": cb.get_reply(message)}
		else:
			reply = {"code": 1, "name": restaurant_name, "location": location}	
	else:
		reply = {"code": 2, "name": movie_name}

	result = {'reply': reply}
	return jsonify(result)

def connect_to_kata_ai(text):
	text = "+".join(text.split())
	url = "https://api.kata.ai/v1/insights"
	headers = {"Authorization": env["API_KATA_AI"]}
	param = {'m': text}
	r = requests.get(url, params=param, headers=headers)
	return r.json()

def get_location(text):
	result = connect_to_kata_ai(text)
	location = ""
	if (result["code"] == 200):
		entities = result["entities"]
		for entity in entities:
			if entity["entity"] == "LOCATION":
				location = entity["fragment"]
	return location

if __name__ == '__main__':
    app.run()