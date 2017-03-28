# Foreign Movie Database
FMDB is an international film command-line interface that uses the TMDB REST APIto provide users with recommendations of popular foreign films to watch. Users
can retrieve movies based on various categories (e.g. genre, rating...etc).
# Installation
Download the source from [Github](https://github.com/sogunsemi/intlfilms).
The dependencies can be found in the requirements.txt file.
# Usage
You will need an API key from [TMDB](https://www.themoviedb.org/)
Create a config.ini file with your API key so it can be read by `config.py`:
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

Example URL's for other databases are:
```python
#PostgreSQL
engine = create_engine('postgresql://username:password@localhost/mydatabase')

#MySQL
engine = create_engine('mysql+mysqldb://username:password@localhost/foo')
```
More information on how to build the database URL as well as other examples
can be found at [SQLAlchemy DB URL's](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)

