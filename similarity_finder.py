from difflib import SequenceMatcher

class SimilarityFinder:
	"""docstring for SimilarityFinder"""
	def similar(self, a,b):
		return SequenceMatcher(None, a, b).ratio()

	def getTitleFromTitleList(self, filename):
		file = open(filename,'r')
		titles = file.readlines()
		return titles

	def findMostSimilarTitle(self, str, titles):
		max_idx = 0
		maximum = 0
		found = 0
		res = ""
		for title in titles:
			title = title.replace("\n","")
			if str.find(title) != -1:
				res = title
				found = 1
				break
			elif str.find(title.split(":")[0]) != -1:
				res = title
				found = 1
				break

		if found == 0:
			for i, title in enumerate(titles):
				if maximum < self.similar(str, title):
					maximum = self.similar(str, title)
					max_idx = i

				if title.find(":") != -1:
					firstWord = title.split(":")[0]
					if maximum < self.similar(str, firstWord):
						maximum = self.similar(str, firstWord)
						max_idx = i
			if maximum > 0.4:
				res = titles[max_idx]

		return res

if __name__ == '__main__':
	sf = SimilarityFinder()
	titles = sf.getTitleFromTitleList("movies_list.txt")
	print sf.findMostSimilarTitle("mau nonton Logan", titles)