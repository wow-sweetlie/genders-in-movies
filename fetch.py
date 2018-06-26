import tmdbsimple as tmdb
import os

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import sys
import argparse

# automap base
Base = automap_base()

tmdb.API_KEY = os.environ['TMDB_API_KEY']

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)
logger.propagate = False


class MovieYearPage(Base):
    __tablename__ = "movie_year_page"
    Year = Column(Integer, primary_key=True)
    Page = Column(Integer)
    TotalPages = Column(Integer)

    def __init__(self, year):
        self.Year = year
        self.Page = 1

    def next_page(self):
        if self.TotalPages and self.Page >= self.TotalPages:
            raise Exception("already got all page for year: {}".format(
                self.Year))
        discover = tmdb.Discover()
        discovered = discover.movie(primary_release_year=self.Year,
                                    include_adult=False,
                                    page=self.Page)
        movies = discovered['results']
        self.TotalPages = discovered['total_pages']
        for movieinfo in movies:
            counter = GenderCounter(movieinfo)
            insert_stmt = insert(GenderCounter).\
                values(Id=counter.Id,
                       Title=counter.Title,
                       Popularity=counter.Popularity,
                       Valid=counter.Valid,
                       Year=counter.Year,
                       Fetched=counter.Fetched)
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=['Id']
            )
            conn.execute(do_nothing_stmt)

        self.Page += 1


class GenderCounter(Base):
    __tablename__ = "movie_gender"
    Id = Column(Integer, primary_key=True)
    Men = Column(Integer)
    Women = Column(Integer)
    Unset = Column(Integer)
    Title = Column(String)
    Popularity = Column(Float)
    Year = Column(Integer)
    Valid = Column(Boolean)
    Fetched = Column(Boolean)

    UNSET = 0
    WOMAN = 1
    MAN = 2

    def __init__(self, movie):
        self.Id = movie['id']
        self.Title = movie['title']
        self.Year = int(movie['release_date'][0:4])
        self.Popularity = movie['popularity']
        self.Valid = True
        self.Fetched = False

    def fetch_gender(self):
        movie = tmdb.Movies(self.Id)
        credits = movie.credits()
        head = credits['cast'][0:3]
        self.Fetched = True
        if len(head) != 3:
            self.Valid = False
            return

        self.Men = 0
        self.Women = 0
        self.Unset = 0
        for c in head:
            self.inc(c['gender'])

    def inc(self, genderTag):
        if genderTag == self.UNSET:
            self.Unset += 1
        elif genderTag == self.WOMAN:
            self.Women += 1
        elif genderTag == self.MAN:
            self.Men += 1
        else:
            raise("invalid gender value")

    def __str__(self):
        return ("Movie {}\n{} ({}) - Popularity: {:.2f}\n"
                "2fU: {}\nW: {}\nM: {}").format(
            self.Id,
            self.Title,
            self.Year,
            self.Popularity,
            self.Unset,
            self.Women,
            self.Men
        )


engine = create_engine(os.environ['DATABASE_URL'])
conn = engine.connect()
Base.prepare(engine, reflect=True)


def search_movies():
    session = Session(engine)
    yearPage = session.query(MovieYearPage).\
        filter((MovieYearPage.Page == 1) |
               (MovieYearPage.Page < MovieYearPage.TotalPages)).\
        order_by(MovieYearPage.Page).first()
    logger.warning("fetching movies for year {} / Page {}".format(
        yearPage.Year,
        yearPage.Page))
    yearPage.next_page()
    session.add(yearPage)
    session.commit()


def movie_fetcher():

    session = Session(engine)
    movie = session.query(GenderCounter).\
        filter(GenderCounter.Fetched == False).first()
    movie.fetch_gender()
    logger.warning("fetching genders for movie {} ({})".format(
        movie.Title, movie.Year))
    session.add(movie)
    session.commit()


def init():
    print("init")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    initYears()


def initYears():
    session = Session(engine)
    for year in range(1900, 2018):
        session.add(MovieYearPage(year))
    session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true")
    args = parser.parse_args()

    if args.init:
        init()
        sys.exit()

    logging.getLogger().addHandler(logging.StreamHandler())
    search_movies()

    scheduler = BlockingScheduler()
    scheduler.add_job(movie_fetcher, 'interval', seconds=2)
    scheduler.add_job(search_movies, 'interval', seconds=30)
    scheduler.start()
