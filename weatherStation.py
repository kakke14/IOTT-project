
from time import sleep
import paho.mqtt.client as paho, os, urllib.parse

import pyrebase
import json
import datetime

import random

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



def on_message(mqttc, obj, msg):
  print("Message: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
  if msg.topic=="ForcePoll":
      data = getData(False)

      mqttc1.publish("FUpdateFromDevice",str(data));
      # check cashe if data is reason

def on_message1(mqttc, obj, msg):
  print("Message - asd - : " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
  

def on_connect(mqttc, obj, flags, rc):
    print("flags, rc: " + str(flags) + " " + str(rc))

def on_publish(mqttc, obj, msg_id):
    print("msg_id: " + str(msg_id))

def on_subscribe(mqttc, obj, msg_id, granted_qos):
    print("Subscribed: " + str(msg_id) + " " + str(granted_qos))

def on_log(mqttc, obj, level, log_string):
    print(log_string)


def createJsonObject(temperature, humidity, pressure):
  

  dict_obj = {
    'date':str(datetime.datetime.now()),
    'temperature': temperature,
    'humidity': humidity,
    'pressure': pressure
    }
  json_obj = json.dumps(dict_obj, sort_keys=True)
  return dict_obj 

def getData(onTarget):

  if(onTarget==False):
    t=random.randrange(20,30)
    h=random.randrange(30,40)
    p=random.randrange(1000,1020)
    data=createJsonObject(t,h,p)
    #print(data)
    return data
    #ret = db.child(localID).push(data, user['idToken'])
    #print(ret)

  elif(onTarget==True):
    from sense_hat import SenseHat
    sense = SenseHat()
    sense.clear()
    while True:
      
      # Take readings from all three sensors
      t = sense.get_temperature()
      p = sense.get_pressure()
      h = sense.get_humidity()

      # Round the values to one decimal place
      t = round(t, 1)
      p = round(p, 1)
      h = round(h, 1)

      # Create the message
      # str() converts the value to a string so it can be concatenated
      message = "Temperature: " + str(t) + " Pressure: " + str(p) + " Humidity: " + str(h)

      # Display the scrolling message
      #sense.show_message(message, scroll_speed=0.05)
      #print(message)

      acceleration = sense.get_accelerometer_raw()
      x = acceleration['x']
      y = acceleration['y']
      z = acceleration['z']

      x=round(x, 0)
      y=round(y, 0)
      z=round(z, 0)

      #print("x={0}, y={1}, z={2}".format(x, y, z))
      data=createJsonObject(t,h,p)
      return data

def continuesUpdate(onTarget):
  while True:
    data = getData(onTarget)
    print("publish on Continues update")
    mqttc2.publish("ContinuesUpdate", str(data))
    sleep(5*60)


if __name__== "__main__":
  mqttc1 = paho.Client()
  mqttc2 = paho.Client()

  # Assign event callbacks
  mqttc1.on_message = on_message
  mqttc1.on_connect = on_connect
  mqttc1.on_publish = on_publish
  mqttc1.on_subscribe = on_subscribe

  mqttc2.on_message = on_message1
  mqttc2.on_connect = on_connect
  mqttc2.on_publish = on_publish
  mqttc2.on_subscribe = on_subscribe

  # Parse CLOUDMQTT_URL (or fallback to localhost)
  url_str = os.environ.get('CLOUDMQTT_URL', 'farmer.cloudmqtt.com')
  url = urllib.parse.urlparse(url_str)

  # Uncomment to enable debug messages
  #mqttc.on_log = on_log

  # Connect
  mqttc1.username_pw_set("tizwftfs", "YdfYCynSzl23")
  mqttc1.connect("farmer.cloudmqtt.com", 14138)

  mqttc2.username_pw_set("tizwftfs", "YdfYCynSzl23")
  mqttc2.connect("farmer.cloudmqtt.com", 14138)

  # Start subscribe, with QoS level 0
  mqttc1.subscribe("ForcePoll", 0)





  onTarget = False
  x = Thread(target=continuesUpdate, args=(onTarget,))
  x.start()
  rc1 = 0
  rc2 = 0
  print("setup done")
  while rc1 == 0 & rc2 == 0:
      rc1 = mqttc1.loop()
      rc2 = mqttc2.loop()
  print("rc1: " + str(rc1) + "rc2: " + str(rc2))
  
