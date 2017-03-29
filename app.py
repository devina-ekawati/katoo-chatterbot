from flask import Flask, request, jsonify
from chatter_bot import ChatterBot
from similarity_finder import SimilarityFinder
import os

app = Flask(__name__)
cb = ChatterBot()
sf = SimilarityFinder()

mydir = os.path.dirname(__file__)
file = os.path.join(mydir, 'movies_list.txt')

@app.route('/get-reply', methods=['POST'])
def get_reply():
	json = request.json
	message = json["message"]
	reply = cb.get_reply(message)
	result = {'reply': str(reply)}
	return jsonify(result)

@app.route('/get-title', methods=['POST'])
def get_title():
	json = request.json
	message = json["message"]
	titles = sf.getTitleFromTitleList(file)
	title = sf.findMostSimilarTitle(message, titles)
	result = {'title': str(title)}
	return jsonify(result)

if __name__ == '__main__':
    app.run()