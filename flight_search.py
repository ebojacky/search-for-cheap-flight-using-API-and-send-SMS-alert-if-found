from datetime import datetime as dt, timedelta
import requests
import os

APIKEY_QUERY = os.environ["tequila_apikey_query"]
APIKEY_SEARCH = os.environ["tequila_apikey_search"]


def extract_relevant_data(data):
    return {
        "flight_id": data["id"],
        "price": data["price"],
        "cityFrom": data["cityFrom"],
        "cityTo": data["cityTo"],
        "nightsInDest": data["nightsInDest"],

        "initial_journey": {
            "id": data["route"][0]["id"],
            "flyFrom": data["route"][0]["flyFrom"],
            "flyTo": data["route"][0]["flyTo"],
            "cityCodeFrom": data["route"][0]["cityCodeFrom"],
            "cityCodeTo": data["route"][0]["cityCodeTo"],
            "airline": data["route"][0]["airline"],
            "flight_no": data["route"][0]["flight_no"],
            "utc_arrival": data["route"][0]["utc_arrival"],
            "utc_departure": data["route"][0]["utc_departure"],
        },
        "return_journey": {
            "id": data["route"][1]["id"],
            "flyFrom": data["route"][1]["flyFrom"],
            "flyTo": data["route"][1]["flyTo"],
            "cityCodeFrom": data["route"][1]["cityCodeFrom"],
            "cityCodeTo": data["route"][1]["cityCodeTo"],
            "airline": data["route"][1]["airline"],
            "flight_no": data["route"][1]["flight_no"],
            "utc_arrival": data["route"][1]["utc_arrival"],
            "utc_departure": data["route"][1]["utc_departure"]
        }
    }


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.endpoint_query = "https://tequila-api.kiwi.com/locations/query"
        self.endpoint_search = "https://tequila-api.kiwi.com/v2/search"
        self.apikey_query = APIKEY_QUERY
        self.apikey_search = APIKEY_SEARCH

    def get_iata_code(self, city):
        head = {
            "apikey": self.apikey_query
        }
        par = {
            "term": city,
            "location_types": "city"
        }
        response = requests.get(url=self.endpoint_query, params=par, headers=head)
        response.raise_for_status()

        return response.json()["locations"][0]["code"]

    def get_flights(self, home, destination):
        head = {
            "apikey": self.apikey_search
        }
        dates = [(dt.now() + timedelta(days=i)).strftime("%d/%m/%Y") for i in [1, 180]]

        query = {
            "fly_from": home,
            "fly_to": destination,
            "date_from": dates[0],
            "date_to": dates[1],
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=self.endpoint_search,
                                params=query, headers=head)
        response.raise_for_status()
        flights = []
        for each_data in response.json()["data"]:
            flights.append(extract_relevant_data(each_data))

        return flights
