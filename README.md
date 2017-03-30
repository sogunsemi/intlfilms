# Foreign Movie Database
FMDB is an international film command-line interface that uses the TMDB REST APIto provide users with recommendations of popular foreign films to watch. Users
can retrieve movies based on various categories (e.g. genre, rating...etc).
## Installation
Download the source from [Github](https://github.com/sogunsemi/intlfilms).
The dependencies can be found in the requirements.txt file.
## Usage
You will need an API key from [TMDB](https://www.themoviedb.org/).

Next, create a `config.ini` file and include your API key so it can be read by `config.py`:
```python
[Keys]
api_key = <YOUR API KEY>
```
In the `constants.py` file change the `DATABASE_URL` based on what database you wish to use:
```python
DATABASE_URL = <YOUR URL>
```
The general format for the URL's is:
`dialect+driver://username:password@host:port/database`

Example URL's for other databases:
```python
#PostgreSQL
engine = create_engine('postgresql://username:password@localhost/mydatabase')

#MySQL
engine = create_engine('mysql+mysqldb://username:password@localhost/foo')
```
More information on how to build the database URL as well as other connection string examples can be found at [SQLAlchemy DB URL's](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls).

This application is CLI-based:

```python
python film_recomm.py 
Type "?" or "help" for available commands
(FMDB)
```
Tab-completion is included:
```python
(FMDB) genre 
Action          Comedy          Drama           History         Mystery         Thriller        Western        
Adventure       Crime           Family          Horror          Romance         TV Movie       
Animation       Documentary     Fantasy         Music           Science Fiction War
```
Example search result for movies with a genre list including "Drama":
```python
(FMDB) genre Drama
===================
Drama movies
===================
2009-06-01 [Greek(Modern)] "Dogtooth"
2011-11-02 [French] "The Intouchables"
1994-09-14 [French] "Leon: The Professional"
1976-03-04 [Norwegian] "The Summer I Turned 15"
1982-01-01 [Portuguese] "Love Strange Love"
2016-08-26 [Japanese] "Your Name."
1975-07-16 [French] "The Hot Nights of Linda"
```
