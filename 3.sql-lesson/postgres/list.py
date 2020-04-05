import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine("postgresql:///postgres")  # os.getenv("DATABASE_URL"))
# DATABASE_URL is an environment variable that indicates where the database lives

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))

# execute this SQL command and return all of the results


def main():
    flights = db.execute(
        "SELECT origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        # for ever
        print(f"{flight.origin} to {flight.destination}, {flight.duration} minutes.")


if __name__ == "__main__":
    main()
