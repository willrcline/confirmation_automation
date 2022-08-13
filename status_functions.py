import pandas as pd
from datetime import datetime

def yes(phone):
    apt = pd.read_csv('apt_confirmations')
    apt.loc[apt['phone'] == phone, 'client_response'] = 'y'
    
    now=datetime.today()
    timestamp_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    apt.loc[apt['phone'] == phone, 'client_response_ts'] = timestamp_str

    pd.to_csv('apt_confirmations', index=False)

def reschedule(phone): 
    apt = pd.read_csv('apt_confirmations')
    apt.loc[apt['phone'] == phone, 'client_response'] = 'y'

    now=datetime.today()
    timestamp_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    apt.loc[apt['phone'] == phone, 'client_response_ts'] = timestamp_str

    pd.to_csv('apt_confirmations', index=False)