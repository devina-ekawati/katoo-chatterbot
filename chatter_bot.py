import urllib2
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

chatterbot = ChatBot("Katoo", 
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.5,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],)

class ChatterBot:
	def __init__(self):
		chatterbot.set_trainer(ChatterBotCorpusTrainer)

		chatterbot.train(
		   "chatterbot.corpus.indonesia",
		   "./train.json"
		)

	def get_reply(self, message):
		response = chatterbot.get_response(message)
		print response.confidence 
		return response

if __name__ == '__main__':
	cb = ChatterBot()
	print cb.get_reply("apa kabar?")