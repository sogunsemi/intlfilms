import sys
from config import API_KEY
from model import init_db, DBSession, Movie, Genre, Cast, movie_genres
import time
import requests
import sqlalchemy
import json

# Set system default encoding to utf-8. This way,
# movie/cast names with special chars can be displayed
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

MAX_ENTRIES = 10

MAX_CAST = 5

# Initializes the dictionary we will use to store
# data from the TMDB API with an initial movie list
def init_movie_list():
    
    m_count = 0
    
    # Prepare the request url
    params = {"api_key": API_KEY, "page": 1}
    i_page = 1
    url = "https://api.themoviedb.org/3/discover/movie"

    # Loop until we recieve MAX_ENTRIES number of movies
    # or there are no more movies to check
    while True:
        if m_count == MAX_ENTRIES:
            break
        try:
            response = send_request_with_retry(url, params)
        except requests.exceptions.RequestException as e:
            print "HTTP Error: {}".format(e)
            continue

        json_rsp = response.text
        parsed = json.loads(json_rsp)
        
        if i_page == parsed["total_pages"]:
            break

        m_list = parsed["results"]
        #print "total results on page: {}".format(len(m_list))

        # Add movie info to database 
        for result in m_list:
            #print "id: {}".format(result["id"])
            if m_count == MAX_ENTRIES:
                break

            # We only want non-english movies
            if result["original_language"] == "en":
                continue

            # Build the movie object we will
            # store in our dictionary of movies

            m_id = result["id"]
            overview = result["overview"]
            release_date = result["release_date"]
            title = result["title"]
            original_title = result["original_title"]
            original_language = result["original_language"]
            popularity = result["popularity"]
            vote_average= result["vote_average"]
            backdrop_path = result["backdrop_path"]
            poster_path = result["poster_path"]

            details = get_movie_details(m_id, ["credits"])
            runtime = details["runtime"]
            status = details["status"]

            movie_entry = Movie(m_id=m_id, overview=overview, release_date=release_date,
                    title=title, original_title=original_title,
                    original_language=original_language, popularity=popularity,
                    vote_average=vote_average, backdrop_path=backdrop_path,
                    poster_path=poster_path, runtime=runtime, status=status)

            m_genres = []
            try:
                session = DBSession()
                for genre in details["genres"]:
                    genre_name = genre["name"]
                    
                    genre_row = session.query(Genre).filter(Genre.name == genre_name).one_or_none()
                    if genre_row is None:
                        #movie_entry.genres.append(Genre(name=genre_name))
                        m_genres.append(Genre(name=genre_name))
                    else:
                        #movie_entry.genres.append(genre_row)
                        m_genres.append(genre_row)
            except sqlalchemy.orm.exc.MultipleResultsFound as e:
                print "Duplicate genre \"{}\" found".format(genre_name)
            finally:
                DBSession.remove()

            m_cast = []
            cast_num = 0
            for cast_member in details["credits"]["cast"]:
                if cast_num == MAX_CAST:
                    break
                character = cast_member["character"] 
                name = cast_member["name"]
                #movie_entry.cast.append(Cast(character=character, name=name))
                m_cast.append(Cast(character=character, name=name))
                cast_num += 1

            # Add created movie to DB
            try:
                session = DBSession()
                movie_entry.genres.extend(m_genres)
                movie_entry.cast.extend(m_cast)
                session.add(movie_entry)
                session.commit()
                DBSession.remove()
            except sqlalchemy.exc.SQLAlchemyError as e:
                print "DB error during movie collection initialization"
                print e
                session.rollback()
            finally:
                DBSession.remove()

        # Get number of movies we have currently added to the database
        try:
            session = DBSession() 
            m_count = session.query(Movie).count()
        except sqlalchemy.exc.SQLAlchemyError:
            print "DB error during movie count operation"
            session.rollback()
        finally:
            DBSession.remove()

        
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

def deleteMovie(tmdb_id):
    
    session = DBSession()
    d_movie = delete_movie = session.query(Movie).filter(Movie.m_id == tmdb_id).one()
    del d_movie.cast[:]
    session.delete(d_movie)
    session.commit()
    DBSession.remove()

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
    init_db()
    #init_movie_list()

    session = DBSession()

    q = session.query(Movie)
    for movie in q:
        print movie.id, movie.m_id, movie.title
    
    print ""
    
    q = session.query(Genre)
    for g in q:
        print "{} - {}".format(g.id, g.name)

    print ""

    q = session.query(Cast)
    for cast in q:
        print "{} -{} - {} - {}".format(cast.id, cast.movie_id, cast.character, cast.name)

    DBSession.remove()

    #collect_data(mDict)
    
if __name__ == "__main__":
    main()

