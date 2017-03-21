import multiprocessing, sys, time
from config import API_KEY
from model import create_db_engine, Movie, Genre, Cast, movie_genres
from constants import MAX_ENTRIES, MAX_CAST, lang
import requests
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
import json
from ifilms import init_movie_list, collect_data
import readline
import cmd

engine = create_db_engine("sqlite:///sqllite_film.db")
session_factory = sessionmaker(engine)
Session = scoped_session(session_factory)

# Allows tab-completion to work using readline on OS X
readline.parse_and_bind("bind ^I rl_complete")

GENRES = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
        "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
        "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"]

class FMDB(cmd.Cmd):
    """Command processor for the Foreign Movie Database."""
    
    
    def __init__(self):
        cmd.Cmd.__init__(self)
    
    prompt = "(FMDB) "


    def do_popular(self, args):
        """
        Usage:
            popular
            
        Retrieve a list of popular foreign movies
        """
        params = args.split()

        if len(params) > 0:
            print "*** invalid number of arguments"
            return

        get_popular(args)
    
    def do_language(self, args):
        """
        Usage:
            language <lang>
            
        Retrieve a list of popular foreign movies with the specifid original language <lang>
        """
        params = args.split()
        
        if len(params) != 1:
            print "*** invalid number of arguments"
            return

        get_language(params)
    
    def complete_language(self, text, line, begidx, endidx):
        if text:
            completions = [ f for f in lang.values() if f.lower().startswith(text.lower()) ]
        else:
            lang_list = lang.values()
            completions = lang_list[:]
        return completions
    
    def do_rating(self, args):
        """
        Usage:
            rating
            
        Retrieve a list of popular foreign movies ordered by rating
        """
        params = args.split()
        
        if len(params) > 0:
            print "*** invalid number of arguments"
            return
        
        get_rating(params)
    
    def do_genre(self, args):
        """
        Usage:
            genre <genre>
            
        Retrieve a list of popular foreign movies that include the specified genre <genre>
        """
        params = []
        if args != "Science Fiction" and args != "TV Movie":
            params = args.split()
        else:
            params.append(args)
        
        if len(params) != 1:
            print "*** invalid number of arguments"
            return

        get_genre(params)
    
    def complete_genre(self, text, line, begidx, endidx):
        if text:
            completions = [ f for f in GENRES if f.lower().startswith(text.lower()) ]
        else:
            completions = GENRES[:]
        return completions

    def do_release(self, args):
        """
        Usage:
            release
            
        Retrieve a list of popular foreign movies ordered by release date
        """
        params = args.split()
        
        if len(params) > 0:
            print "*** invalid number of arguments"
            return
        get_release(params)

    def do_EOF(self, line):
        return True
    
    def emptyline(self):
        pass

def get_popular(args):
    """
    Get popular foreign movies

    Args:
        args - None

    Return:
        None
    """
    print "======================"
    print "Popular Foreign Movies"
    print "======================"
    
    session = Session()
    q = session.query(Movie)
    for movie in q:
        print u"{} [{}] \"{}\"".format(movie.release_date, lang[movie.original_language], movie.title)
    Session.remove()

def get_language(args):
    """
    Get foreign movie by language
    
    Args:
        args - None

    Return:
        None
    """
    try:
        key = next(key for key, value in lang.items() if value == args[0])
    except StopIteration:
        print "Invalid language: \"{}\"".format(args[0])
        return
    
    print "===================="
    print "{} movies".format(args[0])
    print "===================="

    session = Session()
    q = session.query(Movie).filter(Movie.original_language == key)
    for movie in q:
        print u"{} [{}] \"{}\"".format(movie.release_date, lang[movie.original_language], movie.title)
    Session.remove()
    
def get_rating(args):
    """
    Get foreign movies by rating
    
    Args:
        args - None

    Return:
        None
    """
    print "=================="
    print "Ordered by ratings"
    print "=================="
    
    session = Session()
    q = session.query(Movie).order_by(sqlalchemy.desc(Movie.vote_average))
    for movie in q:
        print u"{} {} [{}] \"{}\"".format(movie.vote_average, movie.release_date, lang[movie.original_language], movie.title)
    Session.remove()

def get_genre(args):
    """
    Get foreign movies by genre
    
    Args:
        args - One movie genre to sarch by

    Return:
        None
    """
    if args[0] not in GENRES:
        print "Invalid genre: \"{}\"".format(args[0])
        return
    
    print "==================="
    print "{} movies".format(args[0])
    print "==================="
    
    session = Session()
    q = session.query(Movie).filter(Movie.genres.any(Genre.name == args[0]))
    for movie in q:
            print u"{} [{}] \"{}\"".format(movie.release_date, lang[movie.original_language], movie.title)
    Session.remove()


def get_release(args):
    """
    Get foreign movies by release date
    
    Args:
        args - None

    Return:
        None
    """
    print "==================="
    print "Ordered by realease"
    print "==================="
    
    session = Session()
    q = session.query(Movie).order_by(sqlalchemy.desc(Movie.release_date))
    for movie in q:
        print u"{} [{}] \"{}\"".format(movie.release_date, lang[movie.original_language], movie.title)
    Session.remove()

def main():
    try:
        init_movie_list()
        mProcess = multiprocessing.Process(target=collect_data)
        mProcess.daemon = True
        mProcess.start()
        print "Collecting data..."
        time.sleep(200)
    except:
        print "Error: Main process exited."
        sys.exit(0)
if __name__ == "__main__":
    FMDB().cmdloop("Type \"?\" or \"help\" for available commands")
    #main()
