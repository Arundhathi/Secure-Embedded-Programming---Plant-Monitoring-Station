import mraa
import time 
import datetime
import argparse
import requests
import sqlite3
import smtplib 
from flask import Flask, render_template, Markup, request, url_for, redirect
from flask_bootstrap import Bootstrap
from time import strftime 
from OpenSSL import SSL

fmt = "%H:%M:%S"

#defining pins
moisture_sensor_power = mraa.Gpio(7)
moisture_sensor_pin = mraa.Aio(0)
moisture_sensor_pin.setBit(12)
led_blue = mraa.Gpio(2)
led_blue.dir(mraa.DIR_OUT)
led_blue.write(0)
led_yellow= mraa.Gpio(4)
led_yellow.dir(mraa.DIR_OUT)
led_yellow.write(0)

#directing pins
moisture_sensor_power.dir(mraa.DIR_OUT)

#global variables
global soilSensorValue
global soilSensorMin  #min/dry sensor value 
global soilSensorMax #maximum dry sensor value 
global moisture_high_threshold 
global moisture_low_threshold 
global value_to_Send 

soilSensorValue = 0
soilSensorMin = 0 #min/dry sensor value 
soilSensorMax = 1000 #maximum dry sensor value 
moisture_high_threshold = 800
moisture_low_threshold = 250
value_to_Send = 0
#note: more water = better conductivity = lower resistance = higher signal 

#sid = 'moisture001'

#urla = "http://192.168.1.51:5000/sid/"
#urla = urla + str(sid)
#requests.post(urla,verify=False)

conn = sqlite3.connect('sensor_user.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS sensor_read (sensorName TEXT, sensorKey TEXT, sensor_data TEXT, lower_limit TEXT, upper_limit TEXT)")
query = " INSERT INTO sensor_read VALUES (?,?,?,?,?)"
t = ("-","-","-","-","-",)
c.execute(query,t)
conn.commit()


app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    global soilSensorValue
    global soilSensorMin  #min/dry sensor value 
    global soilSensorMax #maximum dry sensor value 
    global moisture_high_threshold 
    global moisture_low_threshold 
    global value_to_Send 
    
    conn = sqlite3.connect('/home/root/final_test2/sensor_user.db')
    c = conn.cursor()
	
    lower_limit = "SELECT lower_limit FROM sensor_read"  
    upper_limit = "SELECT upper_limit FROM sensor_read" 
    c.execute(lower_limit)
    lower = c.fetchall()
    lower_value=lower[0][0]
    ll = int(lower_value)

	
    c.execute(upper_limit)
    upper = c.fetchall()
    upper_value = upper[0][0]
    ul = int(upper_value)

    if request.method == 'POST':
        print "hello"
        SensorName = request.form['Sensor_Name']
        #upper_val = int(upper_limit)
        SensorKey = request.form['Sensor_Key']
        #lower_val = int(lower_limit)
    	urla = "https://192.168.1.51:5000/sid/"
    	urla = urla + str(SensorKey)
    	requests.post(urla,verify=False)
        print SensorName 
        print SensorKey 
    		
    		
    	print("Moisture Sensor Functioning \n")
        print("calibration")
#calibration routine
        for i in range (0, 10):
            moisture_sensor_power.write(1)
            soilSensorValue = moisture_sensor_pin.read()

            if (soilSensorValue <= soilSensorMax):
                soilSensorMax = soilSensorValue
               
            if (soilSensorValue >= soilSensorMin):
                soilSensorMin = soilSensorValue
                
    
        time.sleep(5)

        moisture_sensor_power.write(1)
        soilSensorValue = moisture_sensor_pin.read()  
        if (soilSensorValue >= ul):
            print("Water Level High\n")
            moisture_value = 5
	    alert_flag = 2
	    led_blue.write(1)
    
        elif (soilSensorValue <= ll):
            print ("Water Level Low\n")
            moisture_value = 1
	    alert_flag = 1
	    led_yellow.write(1)

        else:
            print ("Water Level Alright\n")
            moisture_value = 3
	    alert_flag = 0
	    led_blue.write(0)
	    led_yellow.write(0)

       # if (soilSensorValue >= moisture_high_threshold ):
        #    print("Water Level High\n")
         #   moisture_value = 5
    
       # elif (soilSensorValue <= moisture_low_threshold):
        #    print ("Water Level Low\n")
         #   moisture_value = 1

            
        #else:
         #   print ("Water Level Alright\n")
          #  moisture_value = 3

        time.sleep(1)
        url = "https://192.168.1.51:5000/getdata/"
        url = url + str(moisture_value)
        requests.post(url,verify=False) 
	
        query = "UPDATE sensor_read SET sensorName = ?, sensorKey = ?, sensor_data = ?"
        t = (SensorName, SensorKey, moisture_value)
        c.execute(query,t)
        conn.commit()


        time.sleep(5)
        #led_green.write(0)
       # led_red.write(0)
    
        response = redirect('/read_sensor_data', code = 302)
        return response 
    return render_template('sid_input.html') 

@app.route('/get_lowerlimit/<string:lower_limit>', methods = ['POST', 'GET'])
def get_lower_limit(lower_limit):
    if request.method == 'POST':
        print lower_limit
        ll = int(lower_limit)
        c.execute('''UPDATE sensor_read SET lower_limit = ?''', (lower_limit,))
        conn.commit()
        response = redirect('/read_sensor_data', code = 302)
        return response 

@app.route('/get_upperlimit/<string:upper_limit>', methods = ['POST', 'GET'])
def get_upperlimit(upper_limit):
    if request.method == 'POST':
        print upper_limit
        print (type (upper_limit))
        ul = int(upper_limit)
        print (type (upper_limit))
        c.execute('''UPDATE sensor_read SET upper_limit = ?''', (upper_limit,))
        conn.commit()
        response = redirect('/read_sensor_data', code = 302)
        return response 

@app.route('/read_sensor_data', methods = ['POST', 'GET'])
def read_sensor_data():
    global soilSensorValue
    c.execute("SELECT sensorName, sensorKey, sensor_data, lower_limit, upper_limit FROM sensor_read")
    conn.commit()
    rows = c.fetchall()
    bodyText = Markup("<b>Moisture Level: \n</b>"+str(soilSensorValue))
    return render_template('read_sensor_data.html', rows = rows)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=4000, ssl_context='adhoc')

