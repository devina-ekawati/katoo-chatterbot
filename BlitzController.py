from lxml import html
import requests
import urllib2

url = "https://www.cgv.id/en/movies/get_movie_json"

def getNowShowingMovies():
	movie_url = "https://www.cgv.id/en/movies/get_movie_json"
	response = urllib2.urlopen(movie_url)
	html = response.read()
	html = html.replace("[","")
	html = html.replace("]","")
	html = html.replace("\"","")
	html = html.lower()
	movieTitles = html.split(",")
	movieTitles = movieTitles[:-1]

	print movieTitles

def getMovieID():
	movie_url = "https://www.cgv.id/en/movies/now_playing"
	page = requests.get(movie_url)
	tree = html.fromstring(page.content)
	movieLinks = tree.xpath('//div[@class="movie-list-body"]/ul/li/img/@src')
	movieIDs = []
	for movieLink in movieLinks:
		movieID = movieLink[-11:-4]
		movieIDs.append(movieID)
	return movieIDs

def getMovies():
	movieIDs = getMovieID()
	template_movie_url = "https://www.cgv.id/en/movies/detail/"
	movieDetails = {}
	for movieID in movieIDs:
		movie_url = template_movie_url + movieID
		page = requests.get(movie_url)
		tree = html.fromstring(page.content)
		movie = {}
		title = tree.xpath('//div[@class="movie-info-title"]/text()')
		movietitle = title[0].strip()
		movie["id"] = movieID
		movie["poster"] = "https://www.cgv.id/" + tree.xpath('//div[@class="poster-section left"]/img/@src')[0]
		movie["trailer"] = tree.xpath('//div[@class="trailer-section"]/iframe/@src')[0]
		movie["synopsis"] = tree.xpath('//div[@class="movie-synopsis right"]/p/text()')[0]
		info = tree.xpath('//div[@class="movie-add-info left"]/ul/li/text()')
		if len(info) == 7:
			movie["director"] = info[0][11:]
			movie["actors"] = info[1][9:]
			movie["durations"] = info[2][12:]
			movie["censorrating"] = info[3][16:]
			movie["genre"] = info[4][8:]
			movie["language"] = info[5][11:]
			movie["subtitle"] = info[6][12:]
		elif len(info) == 7:
			movie["director"] = info[0][11:]
			movie["actors"] = info[1][9:]
			movie["durations"] = info[2][12:]
			movie["censorrating"] = info[3][16:]
			movie["genre"] = info[4][8:]
			movie["language"] = info[5][11:]
		
		cinemas = tree.xpath('//div[@class="schedule-title"]/text()')
		movie["cinema"] = cinemas
		cinematypes= tree.xpath('//li[@class="schedule-type"]/text()')
		for cinematype in cinematypes:
			movie["cinematype"] = cinematype.strip()
		showtimes = tree.xpath('//ul[@class="showtime-lists"]/li/a/text()')
		movie["showtime"] = showtimes
		prices = tree.xpath('//ul[@class="showtime-lists"]/li/a/@price')
		movie["price"] = prices
		
		# cinemainfos = {}
		# counter = 0
		# for cinema in cinemas:
		# 	time = showtimes[counter]
		# 	if showtimes[counter] < time:
		# 		time = showtimes[counter]
		# 		movieDetails[cinema] = cinemainfos
		# 		cinemainfos = {}
		# 	else:
		# 		cinemainfos["showtime"].append(showtimes[counter])
		# 		cinemainfos["price"].append(prices[counter])
		# 		counter++

		movieDetails[movietitle] = movie

	return movieDetails

# getNowShowingMovies()
print getMovies()
