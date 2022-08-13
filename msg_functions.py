import os
from twilio.rest import Client as twilioClient
import schedule
import time
import pandas as pd
import numpy as np
from datetime import datetime

twilio_phone = '+12512548494'
account_sid = 'ACba71bf990ec62eb505278b9472bad67b'
auth_token = '788e421e3ab8c4e1fb9b652bcbbe8b75'
client = twilioClient(account_sid, auth_token)

now=datetime.today()
date_str = now.strftime("%m/%d/%y")

def confirmations():
    apt = pd.read_csv('apt_confirmations.csv')

    for id, row in apt.iterrows():
        msg = client.messages.create(
            body= ("Hello! This is Massage Envy confirming your appointment for tomorrow at " + row["time"] + " with " + row["employee_firstname"] + ". Type \"Y\" to confirm or \"R\" to reschedule. Appointment cancellation notices must be provided before store closing today to avoid same day cancellation fees."),
            from_=twilio_phone,
            to='2058079007'
        )

def test():
    msg = client.messages.create(
        body= "Scheduled Test",
        from_=twilio_phone,
        to='2058079007'
    )