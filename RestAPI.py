from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import paho.mqtt.client as paho, os, urllib.parse
from time import sleep
from threading import Thread

app = Flask(__name__)
api = Api(app)

def slow_function(some_object):
    sleep(5)
    print(some_object)
    return some_object

@app.route('/')
def index():
    some_object = 'This is a test'
    thr = Thread(target=slow_function, args=[some_object])
    ret =  thr.start()
    return ret

#messageReceived=False
newWeather={'asd':123}
class WeatherInfo(Resource):
    def get(self):
        print("returning most resent data")
        mqttc.publish("ForceUpdate", "ForceUpdateReqFromAPI")
        mqttc.loop()
        while not messageReceived:
            mqttc.loop()

        print(newWeather)
        return {'asd':123}
        

api.add_resource(WeatherInfo, '/weatherinfo') # Route_1

def checkMessage():
    mqttc.loop()


# Define event callbacks
def on_connect(mqttc, obj, flags, rc):
    print("flags, rc: " + str(flags) + " " + str(rc))

def on_message(mqttc, obj, msg):
    print("Message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if str(msg.payload)==str(b'ForceUpdateReqFromAPI'):
        print("not right message")
        return
    else:
        print("that OK")
        newWeather = {'asd':345}
        messageReceived=True
        print(messageReceived)



def on_publish(mqttc, obj, msg_id):
    print("msg_id: " + str(msg_id))

def on_subscribe(mqttc, obj, msg_id, granted_qos):
    print("Subscribed: " + str(msg_id) + " " + str(granted_qos))

def on_log(mqttc, obj, level, log_string):
    print(log_string)



if __name__ == '__main__':
    mqttc = paho.Client()

    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'farmer.cloudmqtt.com')
    url = urllib.parse.urlparse(url_str)

    # Uncomment to enable debug messages
    #mqttc.on_log = on_log

    # Connect
    mqttc.username_pw_set("tizwftfs", "YdfYCynSzl23")
    mqttc.connect("farmer.cloudmqtt.com", 14138)

    # Start subscribe, with QoS level 0
    mqttc.subscribe("ForceUpdate", 0)

    # Continue the network loop, exit when an error occurs
    mqttc.loop()
    mqttc.loop()
    mqttc.loop()
    messageReceived=False
    app.run(port='5002')
     