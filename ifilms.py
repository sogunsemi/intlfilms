from config import API_KEY
import requests
import movies

def collect_data():
	"""
	Collects movie data from the TMDB REST API periodically
	and stores the information in a dictionary.
	"""
	params = {"api_key": API_KEY}
	
	try:
		response = requests.get("https://api.themoviedb.org/3/discover/movie", params=params)	
		print "Status code: {}".format(response.status_code)
		
		if not response.status_code // 100 == 2:
			print "Error: unexpected response of\n {}".format(response.json())
		else:
			print response.json()
	except requests.exceptions.RequestException as e:
		print "Error: {}".format(e)

def main():	
	collect_data()

if __name__ == "__main__":
	main()	
