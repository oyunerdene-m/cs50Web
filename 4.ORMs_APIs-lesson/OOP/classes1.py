# defining class
class Flight:

    def __init__(self, origin, destination, duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration


def main():
    # Create flight.
    # f is a variable of type Flight, just like a variable might be of type str or int.
    f = Flight(origin="New York", destination="Paris", duration=540)

    # Change the value of a propety.
    f.duration += 10

    # Print details about flight.
    print(f.origin)
    print(f.destination)
    print(f.duration)


# python read code top to bottom and to run program we need to call main
# if we running classes1.py, we should call main function, but when we import this file to other files not to call main
if __name__ == "__main__":
    main()
