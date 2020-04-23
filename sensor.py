import argparse
import random
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Send and receive messages through an MQTT connection.")
    parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                          "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
    parser.add_argument('--cert', help="File path to your client certificate, in PEM format.")
    parser.add_argument('--key', help="File path to your private key, in PEM format.")
    parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                          "Necessary if MQTT server uses a certificate that's not already in " +
                                          "your trust store.")
    parser.add_argument('--client-id', default='samples-client-id', help="Client ID for MQTT connection.")
    parser.add_argument('--topic', default="samples/test", help="Topic to publish messages to.")

    return parser.parse_args()

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