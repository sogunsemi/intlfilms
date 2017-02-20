from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('sqlite:///film.db')

DecBase = declarative_base()
DBSession = scoped_session(sessionmaker())

movie_genres = Table(
        "movie_genres",
        DecBase.metadata,
        Column("fk_movie_genre", Integer, ForeignKey("movie.id")),
        Column("fk_genre", Integer, ForeignKey("genre.id")),
        )
movie_cast = Table(
        "movie_cast",
        DecBase.metadata,
        Column("fk_movie_cast", Integer, ForeignKey("movie.id")),
        Column("fk_cast", Integer, ForeignKey("cast.id")),
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
        backref="movie",
        secondary=movie_genres)
    cast = relationship(
        "Cast",
        backref="movie",
        secondary=movie_cast)

    def addGenres(self, genres):
        for genre in genres:
            self.genres.extend(Genre(name="Action"))

class Genre(DecBase):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    m_id = Column(Integer, ForeignKey('movie.id'))

class Cast(DecBase):
    __tablename__ = 'cast'

    id = Column(Integer, primary_key=True)
    character = Column(String(255))
    name = Column(String(255))
    m_id = Column(Integer, ForeignKey('movie.id'))

def init_db():
    engine = create_engine('sqlite:///sqllite_film.db', echo=False)
    DBSession.configure(bind=engine)
    DecBase.metadata.create_all(engine)

# Main entry point of program
def main():
    #init_movie_list(mDict)
    #collect_data(mDict)
    init_db()

if __name__ == "__main__":
    main()
    #init_db()
    
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

    #dbsession.add(m1)
    #dbsession.add(m2)
    #dbsession.commit()
    
    '''
    m1.genres.append(Genre(name="Action"))
    m1.genres.append(Genre(name="Romance"))
    dbsession.add(m1)
    dbsession.commit()
    '''

    '''
    q = dbsession.query(Movie)
    for mov in q:
        print type(mov)
        for genre in mov.genres:
            print genre.name
    '''

    '''
    q = dbsession.query(Genre).count()
    print "number of genres %d" % (q)
    '''

    '''
    for genre in q:
        print type(genre)
        print genre.name
    '''

    # q = dbsession.query(Movie).delete()
    # print type(q)

    # for id, overview in dbsession.query(Movie.m_id, Movie.overview):
        # print "id: {} ovw: {}".format(id, overview)

    # deletes single Movie object "q"
    # q = dbsession.query(Movie).filter(Movie.m_id == 550).first()
    # dbsession.delete(q)
    # deletes all Movie objects with m_id == 550
    # dbsession.query(Movie).filter(Movie.m_id == 550).delete()
    
    #DecBase.metadata.create_all(engine)
    #session_factory = sessionmaker(bind=engine)
    #Session = scoped_session(session_factory)
