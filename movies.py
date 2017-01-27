class Movie(object):
	"""
	Information we retrive from the TMDB server for each movie
	is stored here so it can be displayed later on.
	"""	
	def __init__(self):
		self.data = {}
		data["id"] = 0
		data["overview"] = ""
		data["release_date"] = ""
		data["genres"] = []
		data["title"] = ""
		data["original_title"] = ""
		data["original_language"] = ""
		data["vote_average"] = ""
		data["backdrop_path"] = ""
		data["poster_path"] = ""
		data["runtime"] = ""
		data["status"] = ""
		data["cast"] = []
