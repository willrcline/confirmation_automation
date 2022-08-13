import schedule
import time
from msg_functions import *
from get_client_data import *

# schedule.every().day.at("08:00").do(get_client_data)
schedule.every().day.at("08:30").do(confirmations)