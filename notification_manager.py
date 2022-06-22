import os
from twilio.rest import Client
import smtplib
from flight_data import FlightData

ACCOUNT_SID = os.environ['twilio_account_sid']
AUTH_TOKEN = os.environ['twilio_auth_token']
TWILIO_PHONE_NUMBER = os.environ['twilio_virtual_number']
MY_PHONE_NUMBER = os.environ['my_phone_msisdn']
MY_EMAIL = os.environ['gmail_account']
MY_PASS = os.environ['gmail_key']


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    @staticmethod
    def format_text(f: FlightData, long_text=False):
        text = f"Cheap flight alert!!\n" \
               f"{f.cityFrom} to {f.cityTo} and back at £{f.price} .\n" \
               f"Stay for {f.nightsInDest} nights starting from UTC {f.initial_journey['utc_arrival']}.\n" \
               f"Check Flight ID {f.flight_id} for details"

        if long_text:
            text += f"Details:\n" \
                    f"Initial Journey: {f.initial_journey}\n" \
                    f"Return Journey: {f.return_journey}"

        return text

    def send_sms(self, f: FlightData, to_number=MY_PHONE_NUMBER):
        text = self.format_text(f)

        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=text,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(message.status)

    def send_mail(self, f: FlightData, to_address=MY_EMAIL):
        text = self.format_text(f, long_text=True)

        with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
            connection.login(MY_EMAIL, MY_PASS)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=to_address,
                msg=f"Subject:Cheap Flight Alert!!\n\n{text}")
