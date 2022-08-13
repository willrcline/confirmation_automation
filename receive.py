from email import message
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask import Flask, request, redirect
from datetime import datetime
from threading import Timer
import pandas as pd
import sys
from msg_functions import *
from status_functions import *
import random

twilio_phone = '+12512548494'
account_sid = 'ACba71bf990ec62eb505278b9472bad67b'
auth_token = '788e421e3ab8c4e1fb9b652bcbbe8b75'
client = Client(account_sid, auth_token)


app = Flask(__name__)

@app.route('/receive', methods=['GET', 'POST'])
def sms_reply():
    if request.method == 'POST':
        #get their msg info
        phone = int(request.form['From'][2:])
        message_body = request.form['Body']
        #get their data table info
        client_data = pd.read_csv('apt_confirmations.csv')
        row = client_data[client_data['phone']==phone].reset_index()
        
        #create response object
        resp = MessagingResponse()
        #check for flags
        #Demo sign up from my phone in certain format
        if (message_body == 'Y') or (message_body == 'y'):
            resp.message('Your appointment has been confirmed.')
            yes(phone)
        elif (message_body == 'R') or (message_body == 'r'):
            resp.message('Your appointment will be taken off the schedule.')
            reschedule(phone)
        else:
            resp.message('This is an automated system and does not understand your response.' + '\n' + 'Please respond with "Y" or "R" to confirm or reschedule your appointment. Alternatively, you can give us a call.')
        return str(resp)

if __name__ == '__main__':
    app.run(debug=True)