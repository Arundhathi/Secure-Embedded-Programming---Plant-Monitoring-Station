#!/usr/bin/env python

import mraa
import argparse
import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText

import time 
from time import strftime 

import datetime
from datetime import datetime 

from flask import Flask,render_template,Markup,request
from flask_bootstrap import  Bootstrap

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
soilSensorValue = 0
soilSensorMin = 0 #min/dry sensor value 
soilSensorMax = 1000 #maximum dry sensor value 
moisture_high_threshold = 800
moisture_low_threshold = 250
value_to_Send = 0
alert_flag = 0
sensor_name = 'plant'
#Creating a file for logging

with open('final_sensor_data.txt','w') as file:
    
	file.write('')

conn = sqlite3.connect('/home/root/final_test2/sensor_user.db')
c = conn.cursor()
	
lower_limit = "SELECT lower_limit FROM sensor_read"  
upper_limit = "SELECT upper_limit FROM sensor_read" 
sensor_key = "SELECT sensorKey FROM sensor_read WHERE sensorName = ? LIMIT 1"
t = (sensor_name,)
c.execute(sensor_key, t)
key = c.fetchall()
sensor_key = key[0][0]
urla = "https://192.168.1.51:5000/sid/"
urla = urla + str(sensor_key)
requests.post(urla,verify=False) 


c.execute(lower_limit)
lower = c.fetchall()
lower_value=lower[0][0]
ll = int(lower_value)

	
c.execute(upper_limit)
upper = c.fetchall()
upper_value = upper[0][0]
ul = int(upper_value)
	
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

    time.sleep(1)
    url = "https://192.168.1.51:5000/getalert/"
    url = url + str(alert_flag)
    requests.post(url,verify=False) 
    urlb = "https://192.168.1.51:5000/getdata/"
    urlb = urlb + str(moisture_value)
    requests.post(urlb,verify=False) 
	
    query = "UPDATE sensor_read SET sensor_data = ?"
    t = ((moisture_value,))
    c.execute(query,t)
    conn.commit()
