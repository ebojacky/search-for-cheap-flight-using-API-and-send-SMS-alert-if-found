import requests
import os

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_prices = "https://api.sheety.co/5610985b8f30ed6aa6908e5cea6fe8f1/flightdeals/prices"
        self.sheet_users = "https://api.sheety.co/5610985b8f30ed6aa6908e5cea6fe8f1/flightdeals/users"
        self.sheet_token = os.environ["flightdeals_key"]

    def get_cities_with_no_codes(self):
        bearer_headers = {
            "Authorization": f"Bearer {self.sheet_token}"
        }
        sheet_response = requests.get(
            url=self.sheet_prices,
            headers=bearer_headers
        )
        sheet_response.raise_for_status()
        data = sheet_response.json()
        cities = [(item["city"], item["id"]) for item in data["prices"] if item["iataCode"] == ""]
        return cities

    def update_city_codes(self, city_code, row_id):
        bearer_headers = {
            "Authorization": f"Bearer {self.sheet_token}"
        }
        json = {"price": {
            "iataCode": city_code
            }
        }
        sheet_response = requests.put(
            url=self.sheet_prices + f"/{row_id}",
            json=json,
            headers=bearer_headers
        )
        sheet_response.raise_for_status()

    def get_destinations_and_price(self):
        bearer_headers = {
            "Authorization": f"Bearer {self.sheet_token}"
        }
        sheet_response = requests.get(
            url=self.sheet_prices,
            headers=bearer_headers
        )
        sheet_response.raise_for_status()
        data = sheet_response.json()
        cities = [{"city": item["iataCode"], "lowest_price": item["lowestPrice"]}
                  for item in data["prices"] if
                  item["iataCode"] != ""]
        return cities
