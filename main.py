import data_manager
import flight_search
import notification_manager
import pprint
import flight_data

dm = data_manager.DataManager()
fs = flight_search.FlightSearch()
for city_name, row_id in dm.get_cities_with_no_codes():
    iata_code = fs.get_iata_code(city=city_name)
    dm.update_city_codes(iata_code, row_id)

city_prices = dm.get_destinations_and_price()

for city_price in city_prices:
    flights = fs.get_flights("LON", city_price["city"])
    for flight in flights:
        if flight:
            if int(city_price["lowest_price"]) >= int(flight["price"]):
                print("YES!!, We got a cheap flight!!")
                pprint.pprint(flight)

                # send Notification
                data = flight_data.FlightData(flight)
                nm = notification_manager.NotificationManager()
                # nm.send_sms(data)
                nm.send_mail(data)

