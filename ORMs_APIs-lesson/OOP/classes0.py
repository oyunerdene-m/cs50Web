# defining python class, generic idea of what a flight is.
class Flight:
    # __init__ - special python method for first creating flight object
    # self - refers to object that we're working with
    def __init__(self, origin, destination, duration):
        self.origin = origin
        self.destination = destination
        self.duration = duration


f = Flight(origin="Khovd", destination="USA", duration="540")
print(f.origin)
print(f.destination)
print(f.duration)
