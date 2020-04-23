import random
from datetime import datetime

def generate_data(args):
    ts = datetime.timestamp(datetime.now())

    # Create a dictionary with sample sensor values
    # freezer temperature, freezer operating voltage, the door (open/closed)
    # Include also a timestamp.
    data = {'sensor': args.client_id,
            'temperature': random.gauss(-7, 3),
            'voltage': random.gauss(24, 6),
            'door': random.randint(0, 1),
            'timestamp': datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S+00:00 (UTC)')
            }

    return data