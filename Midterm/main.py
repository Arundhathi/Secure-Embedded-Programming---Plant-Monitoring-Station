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

import pytz
from pytz import timezone

from flask import Flask,render_template,Markup,request, url_for, redirect
from flask_bootstrap import  Bootstrap


global count 
count = 0
global alert_flag
alert_flag = 0
#Declaring GPIO pins for Led and temperature sensor 

led_red = mraa.Gpio(7) #using pin 7 for red led 
led_red.dir(mraa.DIR_OUT) #setting it as an output pin
led_red.write(0) #switching led off 

led_green = mraa.Gpio(4) #using digital pin 4 for green led 
led_green.dir(mraa.DIR_OUT) #setting it as an output pin
led_green.write(0) #switching off led

temp_rawread = mraa.Aio(0) #using analog pin 0 for reading temp sensor raw values 
temp_rawread.setBit(12) #12 bit adc precision


conn = sqlite3.connect('user_log.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS user_read (username TEXT, email_id TEXT, smtp_server TEXT, password TEXT, C_deg REAL, upper_limit REAL, lower_limit REAL)")
conn.commit()

sender = 'arundhathirs1993@gmail.com'
pwd = 'Durganihantree23671518'
username = "arswami"
sample_server = 'smtp.gmail.com:587'
sub = 'Temperature Sensor Alert' 
body = 'Temperature Exceeded Preset Range.'


#Creating a file for logging
with open('midterm.txt','w') as file:
    file.write('')

query = " INSERT INTO user_read VALUES (?,?,?,?,?,?,?)"
t = (username,"arundhathirs1993@gmail.com",sample_server,pwd,30,40,15)
c.execute(query,t)
conn.commit()

def validate(username,password):
    completion = False
    with conn:
        c.execute("SELECT username,password FROM user_read")
        rows= c.fetchall()
        for rows in rows:
            user = rows[0]
            epass = rows[1]
            if user == username and epass == password:
                completion = True
    return completion

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def login_page():
    error = None 
    if request.method == 'POST':
	username = request.form['username']
        password = request.form['password']
        completion = validate(username,password)
        if completion == False:
            error = 'Wrong Username or Password. Try Again'
        else:
            return redirect(url_for('user'))
    return render_template('login_page.html',error = error)	

@app.route('/read_nologin', methods = ['POST' , 'GET'])
def read_nologin():
    read_temp_value = temp_rawread.read()
    v = float(read_temp_value/819.0)
    C_deg = (v * 100) - 50
    F_deg = (C_deg * 9.0 / 5.0) + 32.0
    bodyText = Markup("<b>Temperature in Degree Celcius: \n</b>"+str(C_deg))
    return render_template('read_nologin.html',bodyText=bodyText)



@app.route('/user')
def user():
    global count 
    count = 0 
    return render_template("user.html")

@app.route('/read_temp',methods = ['POST', 'GET'])
def read_temp():
    if request.method == 'POST':
        global count 
        global alert_flag
        upper_limit = request.form['Upper_Temperature_Limit']
        upper_val = int(upper_limit)
        lower_limit = request.form['Lower_Temperature_Limit']
        lower_val = int(lower_limit)
	user_smtp_server = request.form['SMTP_Server']
        smtp_server = str(user_smtp_server)
        alert_status = request.form['Alerts_Disabled']
        alert = str(alert_status)
        if alert == 'yes':
            current_time_stamp = time.time()
	    alert_flag = 1
        
        result = request.form
        
        read_temp_value = temp_rawread.read()
        v = float(read_temp_value/819.0)
        C_deg = (v * 100) - 50
        F_deg = (C_deg * 9.0 / 5.0) + 32.0
        receiver = request.form['Email_ID']
        query = "UPDATE user_read SET email_id = ?, password = ?, smtp_server = ?,  C_deg = ?, upper_limit = ?, lower_limit = ?"
        t = (receiver,pwd,smtp_server,C_deg,upper_val,lower_val)
        c.execute(query,t)
        conn.commit()
        if(C_deg <lower_val or C_deg > upper_val):
            led_red.write(1)
            led_green.write(0)
            server = smtplib.SMTP(smtp_server)
            server.ehlo()
            server.starttls()        
            server.ehlo()
            msg = """From: %s \nTo: %s \nSubject: %s\n\n%s """ % (sender, ",".join(receiver), sub, body)
            server.login(sender,pwd)
            if (alert_flag == 1):
                if ((time.time() - current_time_stamp)<4 and count == 0):
                    server.sendmail(sender,receiver,msg)
                    count = count+1
                elif ((time.time() - current_time_stamp)>606):
                    server.sendmail(sender,receiver,msg)
                    count = 0
                    alert = 'no'
                    
            else:
                server.sendmail(sender,receiver,msg)
            server.quit()
            with open('midterm.txt','a') as file:
                file.write('\nTEMP NOT IN RANGE and VALUE IS:'+str(C_deg))
 
        else:
            led_green.write(1)
            led_red.write(0)
            with open('midterm.txt','a') as file:
                file.write('\nTEMP IN RANGE and VALUE IS:'+str(C_deg))

        time.sleep(5)
        led_green.write(0)
        led_red.write(0)
    
    bodyText = Markup("<b>Temperature in Degree Celcius: \n</b>"+str(C_deg))
    return render_template('read_temp.html',bodyText=bodyText,result=result)
        

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=8000)


