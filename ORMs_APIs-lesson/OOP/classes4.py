# Flight class with Passenger class (multiple classes)


class Flight:

    counter = 1

    def __init__(self, origin, destination, duration):
        self.id = Flight.counter
        Flight.counter += 1

        self.passengers = []

        self.origin = origin
        self.destination = destination
        self.duration = duration

    def print_info(self):
        print(f"Flight origin: {self.origin}")
        print(f"Flight destination: {self.destination}")
        print(f"Flight duration: {self.duration}")
        print(f"Flight id: {self.id}")

        print()
        print("Passengers:")
        for p in self.passengers:
            print(f"{p.name}")
            print(f"{p.flight_id}")

    def add_passenger(self, p):
        self.passengers.append(p)
        p.flight_id = self.id


class Passenger:

    def __init__(self, name):
        self.name = name


def main():
    f1 = Flight(origin="New York", destination="Paris", duration=540)
    f2 = Flight(origin="Kovd", destination="UB", duration=2160)

    alice = Passenger(name="Alice")
    bob = Passenger(name="Bob")
    saraa = Passenger(name="Saraa")

    f1.add_passenger(alice)
    f1.add_passenger(bob)

    f2.add_passenger(saraa)

    f1.print_info()
    f2.print_info()


if __name__ == "__main__":
    main()
