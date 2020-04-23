import ssl
import paho.mqtt.client as mqtt
import json
import sensor
import time

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.

# Using globals to simplify sample code
args = sensor.parse_args()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection result: ", str(rc))

def on_publish(mqttc, obj, mid):
    print("Message published: ", str(mid))
    pass

def ssl_alpn():
    try:
        #debug print opnessl version
        print("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ssl_context.load_verify_locations(cafile=args.root_ca)
        ssl_context.load_cert_chain(certfile=args.cert, keyfile=args.key)

        return  ssl_context

    except Exception as e:
        print("exception ssl_alpn()")
        raise e

if __name__ == '__main__':
    # Setup mqtt connection
    mqtt_connection = mqtt.Client()
    mqtt_connection.on_connect = on_connect
    mqtt_connection.on_publish = on_publish

    # setup TLS connection
    ssl_context = ssl_alpn()
    mqtt_connection.tls_set_context(context=ssl_context)

    print("Connecting to {} with client ID '{}'...".format(args.endpoint, args.client_id))
    mqtt_connection.connect(args.endpoint, 8883, 60)

    # Loop until connection achieved
    mqtt_connection.loop_start()

    while True:
        # generate message based on random values
        message = json.dumps(sensor.generate_data(args))

        print("Publishing message to topic '{}': {}".format(args.topic, message))
        result = mqtt_connection.publish(args.topic, message, qos=1)
        result.wait_for_publish()
        print("Published")

        time.sleep(10)


