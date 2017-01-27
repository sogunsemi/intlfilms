"""
This file will serve to provide other modules access
to the API key.
"""
import ConfigParser

# API key we will use to access the TMDB REST API
API_KEY = None

# Read in API key from config file and store it
config = ConfigParser.SafeConfigParser()
config.read("config.ini")
API_KEY = config.get("Keys", "api_key")
