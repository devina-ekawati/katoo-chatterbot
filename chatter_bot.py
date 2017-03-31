import os
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

class ChatterBot:
	def __init__(self):
		my_dir = os.path.dirname(__file__)
		train_file = os.path.join(my_dir, 'train.json')

		self.chatterbot = ChatBot("Katoo", 
		    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
		    logic_adapters=[
		        {
		            'import_path': 'chatterbot.logic.BestMatch'
		        },
		        {
		            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
		            'threshold': 0.5,
		            'default_response': 'Maaf aku tidak mengerti :('
		        }
	    ],)
		self.chatterbot.set_trainer(ChatterBotCorpusTrainer)

		self.chatterbot.train(
		   "chatterbot.corpus.indonesia",
		   train_file
		)

	def get_reply(self, message):
		response = self.chatterbot.get_response(message)
		print response.confidence 
		return response

if __name__ == '__main__':
	cb = ChatterBot()
	while (True):
		response = raw_input("Message: ")
		print chatterbot.get_response(response)