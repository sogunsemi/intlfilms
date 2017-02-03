import sys
from config import API_KEY
import time
import requests
from movies import Movie
import json

MAX_ENTRIES = 10

# Initializes the dictionary we will use to store
# data from the TMDB API with an initial movie list
def init_movie_list(mDict):
   
    # Prepare the request url
    params = {"api_key": API_KEY, "page": 1}
    i_page = 1
    url = "https://api.themoviedb.org/3/discover/movie"

    # Loop until we recieve MAX_ENTRIES number of movies
    # or there are no more movies to check
    while True:
        if len(mDict) == MAX_ENTRIES:
            break
        try:
            response = send_request_with_retry(url, params)
        except requests.exceptions.RequestException as e:
            print "HTTP Error: {}".format(e)

        json_rsp = response.text
        parsed = json.loads(json_rsp)
        
        if i_page == parsed["total_pages"]:
            break

        m_list = parsed["results"]
        #print "total results on page: {}".format(len(m_list))

        # We build the 
        for result in m_list:
            #print "id: {}".format(result["id"])
            if len(mDict) == MAX_ENTRIES:
                break

            # We only want non-english movies
            if result["original_language"] == "en":
                continue

            # Build the movie object we will
            # store in our dictionary of movies
            m_object = Movie()
            m_dict = m_object.data

            m_dict["id"] = result["id"]
            m_dict["overview"] = result["overview"]
            m_dict["release_date"] = result["release_date"]
            m_dict["title"] = result["title"]
            m_dict["original_title"] = result["original_title"]
            m_dict["original_language"] = result["original_language"]
            m_dict["vote_average"] = result["vote_average"]
            m_dict["backdrop_path"] = result["backdrop_path"]
            m_dict["poster_path"] = result["poster_path"]

            details = get_movie_details(m_dict["id"], ["credits"])
            m_dict["runtime"] = details["runtime"]
            m_dict["status"] = details["status"]

            m_genres = [genre["name"] for genre in details["genres"]]
            m_dict["genres"] = m_genres

            cast_info = details["credits"]["cast"]
            cast_list = [(cast["character"], cast["name"]) for cast in cast_info]
            m_dict["cast"] = cast_list

            mDict[str(m_dict["id"])] = m_object
        
        # Go get the next page of results
        i_page += 1
        params["page"] = i_page
                        
# Retrieves extra details for a given movie
def get_movie_details(m_id, fields):

    # Build the url and add sub-requests that
    # will get appended to the JSON response
    s_fields = ",".join([str(f) for f in fields])
    params = {"api_key": API_KEY, "append_to_response": s_fields}
    url = "https://api.themoviedb.org/3/movie/{}".format(m_id)
    
    parsed = {}
    try:
        response = send_request_with_retry(url, params)
    except requests.exceptions.RequestException as e:
        print "HTTP Error: {}".format(e)
        sys.exit(1)
        
    json_rsp = response.text
    parsed = json.loads(json_rsp)
    #print json.dumps(parsed, indent=4, sort_keys=True)

    return parsed

# Makes all the API requests for the program
# and implements retry functionality if
# we hit the rate limit for the TMDB API
def send_request_with_retry(url, params):
    response = None
    while True:
        response = requests.get(url, params=params)

        # If status code is in 2xx range, leave loop
        if not response.status_code // 100 == 2:

            # If we hit the API rate limit, retry the request in
            # "Retry-After" seconds, if not, throw error
            if response.status_code == 429:
                retry = int(response.headers["Retry-After"])
                print "Sleep for {} seconds".format(retry)
                time.sleep(retry)
            else:
                raise requests.exceptions.RequestException("Bad status code, request unsuccessful!")
        else:
            break
    return response

# Collects movie data from the TMDB REST API and puts
# the information into a dictionary
def collect_data(mDict):
    """
    Collects movie data from the TMDB REST API periodically
    and stores the information in a dictionary.
    """
    for i in mDict:
        print json.dumps(mDict[i].data, indent=4, sort_keys=True)

# Main entry point of program
def main():
    mDict = {}
    init_movie_list(mDict)
    collect_data(mDict)
    
if __name__ == "__main__":
    main()	
