import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql:///postgres")
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("flights.csv")
    reader = csv.reader(f)
    for o, dest, dur in reader:
        db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
                   {"origin": o, "destination": dest, "duration": dur})
        print(
            f"Added flight from {o} to {dest} lasting {dur} minutes.")
    db.commit()


if __name__ == "__main__":
    main()
