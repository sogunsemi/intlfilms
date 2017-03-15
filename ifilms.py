# -*- coding: utf-8 -*-

import sys
from config import API_KEY
from model import create_db_engine, Movie, Genre, Cast, movie_genres
from constants import MAX_ENTRIES, MAX_CAST
import time
import requests
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
import json

# Initializes the dictionary we will use to store
# data from the TMDB API with an initial movie list
def init_movie_list():

    engine = create_db_engine("sqlite:///sqllite_film.db")
    session_factory = sessionmaker(engine)
    DBSession = scoped_session(session_factory)

    # If database is empty, initialize it,
    # if not, skip init.
    try:
        session = DBSession()
        q = session.query(Movie).first()
        
        # Check if the table has already been init'ed
        if q is not None:
            return
    except sqlalchemy.exc.SQLAlchemyError as e:
        print "DB error during initialization"
        print e
    finally:
        DBSession.remove()
    
    print "Initializing International Movie DB..."

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
            if m_count == MAX_ENTRIES:
                break

            # We only want non-english movies
            if result["original_language"] == "en":
                continue

            # Build the movie object we will
            # store in our dictionary of movies

            # Increase movie count
            m_count += 1
            
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

            m_genres = add_genres(DBSession, details)
            m_cast = add_cast(details)

            # Add created movie to DB
            try:
                session = DBSession()
                movie_entry.genres.extend(m_genres)
                movie_entry.cast.extend(m_cast)
                session.add(movie_entry)
                session.commit()
            except sqlalchemy.exc.SQLAlchemyError as e:
                print "DB error during movie collection initialization"
                print e
                session.rollback()
                m_count -= 1
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

def add_genres(Session, details):
    m_genres = []
    try:
        session = Session()
        for genre in details["genres"]:
            genre_name = genre["name"]

            genre_row = session.query(Genre).filter(Genre.name == genre_name).one_or_none()
            if genre_row is None:
                m_genres.append(Genre(name=genre_name))
            else:
                m_genres.append(genre_row)
    except sqlalchemy.orm.exc.MultipleResultsFound as e:
        print "Duplicate genre \"{}\" found".format(genre_name)
    finally:
        Session.remove()

    return m_genres

def add_cast(details):
    m_cast = []
    cast_num = 0
    for cast_member in details["credits"]["cast"]:
        if cast_num == MAX_CAST:
            break
        character = cast_member["character"] 
        name = cast_member["name"]
        m_cast.append(Cast(character=character, name=name))
        cast_num += 1
    return m_cast

def collect_data():
    """
    Collects movie data from the TMDB REST API periodically
    and stores the information in the DB.
    """
    engine = create_db_engine("sqlite:///sqllite_film.db")
    session_factory = sessionmaker(engine)
    Session = scoped_session(session_factory)

    m_count = 0
    top_movies = []
    
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

        # Add movie info to database 
        for result in m_list:
            if m_count == MAX_ENTRIES:
                break

            # We only want non-english movies
            if result["original_language"] == "en":
                continue

            # Build the movie object we will
            # store in our DB

            # Increase movie count
            m_count += 1
            
            m_id = result["id"]
            top_movies.append(m_id)
            
            m_exists = True
            
            try:
                session = Session()
                q = session.query(Movie).filter(Movie.m_id == m_id).first()
                
                # If the movie is already in the DB, check next movie
                # if it is not, proceed to add it to DB
                if q is not None:
                    m_exists = True
                else:
                    m_exists = False
            except sqlalchemy.exc.SQLAlchemyError as e:
                print "DB error while updating database"
                print e
                top_movies.pop()
                m_count -= 1
                continue
            finally:
                Session.remove()

            if m_exists:
                continue

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

            m_genres = add_genres(Session, details)
            m_cast = add_cast(details)

            # Add created movie to DB
            try:
                session = Session()
                movie_entry.genres.extend(m_genres)
                movie_entry.cast.extend(m_cast)
                session.add(movie_entry)
                session.commit()
            except sqlalchemy.exc.SQLAlchemyError as e:
                print "DB error during movie collection initialization"
                print e
                session.rollback()
                top_movies.pop()
                m_count -= 1
            finally:
                Session.remove()

        # Go get the next page of results
        i_page += 1
        params["page"] = i_page
    
    # Remove movies from DB not in top list we got from TMDB
    q = session.query(Movie).filter(~Movie.m_id.in_(top_movies))
    print "\nDeleted:"
    for movie in q:
        print u"{}".format(movie.title)
        del movie.cast[:]
        session.delete(movie)
    session.commit()
    Session.remove()

# Main entry point of program
def main():
    #init_db()
    init_movie_list()
    collect_data()
    
if __name__ == "__main__":
    main()

