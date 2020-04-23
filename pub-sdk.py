import argparse
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException
from awscrt import io, mqtt
import json
from sensor import generate_data

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

parser = argparse.ArgumentParser(description="Send and receive messages through an MQTT connection.")
parser.add_argument('--endpoint', required=True, help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
parser.add_argument('--cert', help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store.")
parser.add_argument('--client-id', default='samples-client-id', help="Client ID for MQTT connection.")
parser.add_argument('--topic', default="samples/test", help="Topic to subscribe to, and publish messages to.")

# Using globals to simplify sample code
args = parser.parse_args()

io.init_logging(io.LogLevel.Debug, 'stderr')

if __name__ == '__main__':
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    # Setup mqtt connection
    mqtt_connection = AWSIoTMQTTClient(args.client_id)
    mqtt_connection.configureEndpoint(args.endpoint, 8883)
    mqtt_connection.configureCredentials(args.root_ca, args.key, args.cert)

    # AWSIoTMQTTClient connection configuration
    mqtt_connection.configureAutoReconnectBackoffTime(1, 32, 20)
    mqtt_connection.configureOfflinePublishQueueing(-1)  # param: queue_size,if set to 0, the queue is disabled. If set to -1, the queue size is set to be infinite.
    mqtt_connection.configureDrainingFrequency(2)  # Draining: 2 Hz
    mqtt_connection.configureConnectDisconnectTimeout(10)  # 10 sec
    mqtt_connection.configureMQTTOperationTimeout(5)  # 5 sec

    print("Connecting to {} with client ID '{}'...".format(
        args.endpoint, args.client_id))

    connect_future = mqtt_connection.connect()
    print("Connected!")

    while True:
        # generate message based on random values
        message = json.dumps(generate_data(args))

        try:
            print("Publishing message to topic '{}': {}".format(args.topic, message))
            mqtt_connection.publish(
                topic=args.topic,
                payload=message,
                QoS=mqtt.QoS.AT_LEAST_ONCE)

        except publishTimeoutException:
            print("Failed to publish message")

        time.sleep(10)

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")