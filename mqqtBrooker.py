import paho.mqtt.client as paho, os, urllib.parse

import pyrebase
import json
import datetime

import random
import ast

from threading import Thread

config = {
"apiKey": "AIzaSyDhieSbPpQkRB9S7pDFNm0hZZI5ykS3jxI",
"authDomain": "weather-station-718eb.firebaseapp.com",
"databaseURL": "https://weather-station-718eb.firebaseio.com",
"storageBucket": "weather-station-718eb.appspot.com"
}
email="pi@asd.dk"
password = "123456"
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


user = auth.sign_in_with_email_and_password(email, password)
userInfo= auth.get_account_info(user['idToken'])
users=userInfo['users']
curUser = users[0]
localID=curUser['localId']
print(str(localID))
db = firebase.database()




# Define event callbacks
def on_connect(mqttc, obj, flags, rc):
    print("flags, rc: " + str(flags) + " " + str(rc))

def on_message(mqttc, obj, msg):
    print("Message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.topic=="Update":
        print("checking chache....")
        # check cashe if data is reason
        if False:
            #send date from chache
            print("returning data from cache")
            mqttc.publish("FUpdateFromDevice", "Cached data From Node")
        else :
            # publish request of new data from Node
            print("Returning data collected from Node")
            mqttc.publish("ForcePoll", "ForceUpdate From Node")

    elif msg.topic=="FUpdateFromDevice":
            print("Updateing cache")

    elif msg.topic=="ContinuesUpdate":
        #should just update firebase data base
        # and update locale cache
        print("Pushing to firebase")
        pushToDatabase(msg.payload)
        print("Update local cache returned : ")


def on_publish(mqttc, obj, msg_id):
    print("msg_id: " + str(msg_id))

def on_subscribe(mqttc, obj, msg_id, granted_qos):
    print("Subscribed: " + str(msg_id) + " " + str(granted_qos))

def on_log(mqttc, obj, level, log_string):
    print(log_string)

def pushToDatabase(data):
    print("refresh")
    global user,db,localID,auth
    user = auth.refresh(user['refreshToken'])
    #should just update firebase data base
    # and update locale cache
    print("create json")
    data=data.decode("utf-8")
    res = ast.literal_eval(data) 
    print("Pushing to firebase")
    ret = db.child(localID).push(res, user['idToken'])



# Publish a message
#mqttc.publish("weather", "Getting started ...")
if __name__== "__main__":

    
    # Continue the network loop, exit when an error occurs
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
    mqttc.subscribe("Update", 0)
    mqttc.subscribe("ContinuesUpdate", 0)
    mqttc.subscribe("FUpdateFromDevice", 0)

    rc = 0
    print("setup done")

    while rc == 0:
        rc = mqttc.loop()
    print("rc: " + str(rc))
