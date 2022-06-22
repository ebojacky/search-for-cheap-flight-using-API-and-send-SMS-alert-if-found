class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, flight):
        self.flight_id = flight["flight_id"]
        self.price = flight["price"]
        self.cityFrom = flight["cityFrom"]
        self.cityTo = flight["cityTo"]
        self.nightsInDest = flight["nightsInDest"]
        self.initial_journey = flight["initial_journey"]
        self.return_journey = flight["return_journey"]

