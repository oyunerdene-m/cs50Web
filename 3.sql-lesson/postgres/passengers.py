from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql:///postgres")
db = scoped_session(sessionmaker(bind=engine))


def main():
    flights = db.execute(
        "SELECT id, origin, destination, duration FROM flights").fetchall()
    for flight in flights:
        print(
            f"Flight {flight.id}: {flight.origin} to {flight.destination}, {flight.duration} minutes.")

    flight_id = int(input("\nFlight ID: "))

    found_flight = db.execute("SELECT id, origin, destination, duration FROM flights WHERE id=:id", {
                              "id": flight_id}).fetchone()
    if(found_flight is None):
        print("Flight you are looking for is not found!")
        return
    print(
        f"Flight you are looking for is: {found_flight.origin} to {found_flight.destination}, {found_flight.duration} minutes.")

    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id", {
                            "flight_id": flight_id}).fetchall()
    print("\nPassengers:")
    for passenger in passengers:
        print(passenger.name)


if __name__ == "__main__":
    main()
