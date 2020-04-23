# PhD Course on Smart Environmnets 2020

Code examples for the [PhD Course on Smart Environments](http://ichatz.me/Site/IoTPhD2020) 
carried out at the [Department of Computer, Control, and Management Engineering Antonio Ruberti (DIAG)](http://www.diag.uniroma1.it) 
of the [Sapienza University of Rome](http://www.uniroma1.it). 

The examples assume a virtual sensor that generates messages containing random values for
temperature, voltage consumption, a boolean door sensor and a timestamp.  

# MQTT client using AWS Python SDK

The first file implements a virtual sensor that connects using the native [AWS IoT SDK for Python](https://github.com/aws/aws-iot-device-sdk-python).
 
You can either install it using pip:
`pip install AWSIoTPythonSDK`

Another option is to compile it from sources:
`git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python
python setup.py install`

# MQTT client using Eclispe PAHO library

The second file implements a virtual sensor that connects to the AWS IoT broker using the [Paho MQTT Client](https://github.com/eclipse/paho.mqtt.python). 
Details on how to setup the TLS connection with the correct parameters so that the MQTT client can connect to
AWS IoT are available in this [AWS blog](https://aws.amazon.com/blogs/iot/how-to-implement-mqtt-with-tls-client-authentication-on-port-443-from-client-devices-python/).

The latest stable version is available in the Python Package Index (PyPi) and can be installed using
`pip install paho-mqtt`

To obtain the full code, including examples and tests, you can clone the git repository:
`git clone https://github.com/eclipse/paho.mqtt.python`

Once you have the code, it can be installed from your repository as well:
`cd paho.mqtt.python
python setup.py install`