
from time import sleep
import pyrebase




import pyrebase
import json
import datetime

import random

onTarget = True

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
db = firebase.database()
#temp=db.child("pi1").child("temperature").get().val()
#print(temp)
#data = {"temperature": "123"}
#ret = db.child("pi1").set(data)
#print(ret)

def createJsonObject(temperature, humidity, pressure):
  

  dict_obj = {
    'date':str(datetime.datetime.now()),
    'temperature': temperature,
    'humidity': humidity,
    'pressure': pressure
    }
  json_obj = json.dumps(dict_obj, sort_keys=True)
  return dict_obj

if(onTarget==False):
    t=random.randrange(20,30)
    h=random.randrange(30,40)
    p=random.randrange(1000,1020)
    data=createJsonObject(t,h,p)
    ret = db.child("pi1").push(data)
  



if(onTarget==True):
  from sense_hat import SenseHat
  sense = SenseHat()
  sense.clear()
  while True:
    email="pi@asd.dk"
    password = "123456"
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    user = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
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
    print(message)

    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)

    print("x={0}, y={1}, z={2}".format(x, y, z))
    data=createJsonObject(t,h,p)
    ret = db.child("pi1").push(data)
    sleep(60*30)
