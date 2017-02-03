class Movie(object):
	"""
	Information we retrive from the TMDB server for each movie
	is stored here so it can be displayed later on.
	"""	
	def __init__(self):
		self.data = {}
		self.data["id"] = 0
		self.data["overview"] = ""
		self.data["release_date"] = ""
		self.data["genres"] = []
		self.data["title"] = ""
		self.data["original_title"] = ""
		self.data["original_language"] = ""
		self.data["vote_average"] = ""
		self.data["backdrop_path"] = ""
		self.data["poster_path"] = ""
		self.data["runtime"] = ""
		self.data["status"] = ""
		self.data["cast"] = []
