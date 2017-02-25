from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///film.db')

DecBase = declarative_base()
DBSession = scoped_session(sessionmaker())

movie_genres = Table(
        "movie_genres",
        DecBase.metadata,
        Column("movie_id", Integer, ForeignKey("movie.id", ondelete="cascade")),
        Column("genre_id", Integer, ForeignKey("genre.id", ondelete="cascade"))
        )

class Movie(DecBase):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    m_id = Column(Integer)
    overview = Column(String(255))
    release_date = Column(String(255))
    title = Column(String(255))
    original_title = Column(String(255))
    original_language = Column(String(255))
    popularity = Column(Float)
    vote_average = Column(Float)
    backdrop_path = Column(String(255))
    poster_path = Column(String(255))
    runtime = Column(Integer)
    status = Column(String(255))
    genres = relationship(
        "Genre",
        backref="movies",
        secondary=movie_genres)
    cast = relationship(
        "Cast",
        backref="movie",
        cascade="all, delete-orphan")

class Genre(DecBase):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Cast(DecBase):
    __tablename__ = 'cast'

    id = Column(Integer, primary_key=True)
    character = Column(String(255))
    name = Column(String(255))
    movie_id = Column(Integer, ForeignKey("movie.id"))

def init_db():
    engine = create_engine('sqlite:///sqllite_film.db', echo=False)
    DBSession.configure(bind=engine)
    DecBase.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    
    dbsession = DBSession()
    m_id = 550
    overview = "overview"
    release_date = "release_date"
    title = "title"
    original_title = "original_title"
    original_language = "original_language"
    popularity = 80.6
    vote_average = 5.7
    backdrop_path = "backdrop_path"
    poster_path = "poster_path"
    runtime = "runtime"
    status = "status"

    m1 = Movie(m_id=m_id, overview=overview, release_date=release_date,
            title=title, original_title=original_title,
            original_language=original_language, popularity=popularity,
            vote_average=vote_average, backdrop_path=backdrop_path,
            poster_path=poster_path, runtime=runtime, status=status)
    m2 = Movie(m_id=1200, overview="overview2", release_date=release_date,
            title=title, original_title=original_title,
            original_language=original_language, popularity=popularity,
            vote_average=vote_average, backdrop_path=backdrop_path,
            poster_path=poster_path, runtime=runtime, status=status)

    #m1.genres.append(Genre(name="Thriller"))
    #dbsession.add(m1)
    #dbsession.add(m2)
    #dbsession.commit()
    #DBSession.remove()
