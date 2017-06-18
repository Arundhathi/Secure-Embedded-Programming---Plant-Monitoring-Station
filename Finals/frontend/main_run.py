import argparse
import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from OpenSSL import SSL
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, Markup
import hashlib
import os
from os import urandom
import time
import datetime
import random
from random import *
import MySQLdb
from bokeh.charts import color, marker 
from bokeh.charts import Chart, Bar, output_file, show, save 
import os.path
import shutil 
from bokeh.io import output_file 
from bokeh.plotting import figure 
import numpy as np

app = Flask(__name__)

no_op = 0
global s_key

global last_timestamp1
last_timestamp1 = 0

global last_timestamp
last_timestamp = 0

global failed_attempt
failed_attempt = 0

global failed_login_attempt
failed_login_attempt = 0

global sensor_id
sensor_id = 0

conn = MySQLdb.connect('localhost','aswami','aswami','aswami' )
c = conn.cursor()

c.execute("create table if not exists user_data_table(username TEXT, email_id TEXT, password TEXT, salt TEXT, register TEXT)")
c.execute("create table if not exists admin_data_table (username TEXT, failed_login_attempts REAL,verified_email TEXT)")
c.execute("create table if not exists sensor_data_table (username TEXT, sensor_name TEXT, sensor_key TEXT,sensor_data TEXT, lower_limit TEXT, upper_limit TEXT, alert_value TEXT)")
c.execute("create table if not exists login_ip_table (IP_address TEXT, login_attempt TEXT)")

query = " INSERT INTO user_data_table VALUES (%s,%s,%s,%s,%s)"

fromaddr = 'arundhathirs1993@gmail.com'
pwd = 'C11Durgameshwari'
smtp_server = 'smtp.gmail.com:587'
t = ("-","-","-","-","-")

try:
    c.execute(query,t)
    conn.commit()
except:
    no_op = 0
    no_op

global otp_sent

def getHash(pwd):
    hashPass=hashlib.md5()
    hashPass.update(pwd)
    return(hashPass.hexdigest())

def validate(username,password):
    completion = False
    with conn:
        c.execute("SELECT username,password FROM user_data_table")
        conn.commit()
        rows= c.fetchall()
        for rows in rows:
            user = rows[0]
            epass = rows[1]
            if user == username and epass == password:
                completion = True
    return completion

@app.route('/')
def home():
    if session.get('logged_in'):
        response = redirect(url_for('user_home_page'))
        return response
    else:
        return render_template('login_page.html')
    return render_template('login_page.html')

@app.route('/sensor_register_page',methods = ['GET', 'POST'])
def sensor_register_page():
    if session.get('logged_in'):
        if request.method == 'POST':
            username = request.form['username']   
            sensor_key = request.form['sensor_key']
            sensor_name = request.form['sensor_name'] 
            sensor_key_hashed = getHash(sensor_key)
            sensor_data = 0
            lower_limit = 0
            upper_limit = 100 
            with conn:
                c.execute("SELECT username,email_id FROM user_data_table WHERE username = %s",(username,))
                conn.commit()
                x = c.fetchall()            
            if(x):
                for x in x:
                    e_id = x[1]
            else:
                error = "No such username registered. Please try again."
                return render_template("sensor_register_page.html" , error = error)
            with conn:
                c.execute("SELECT sensor_name FROM sensor_data_table WHERE username = %s",(username,))
                conn.commit()
                x = c.fetchall()            
            if(x):
                if(sensor_name == x[0][0]): 
                    error = "Sensor already registered."
                    return render_template("sensor_register_page.html" , error = error)
            
            sensor_query = "INSERT INTO sensor_data_table VALUES (%s,%s,%s,%s,%s,%s,%s)"
            alert = 8
            t = (username,sensor_name,sensor_key,sensor_data,lower_limit,upper_limit,alert)
            with conn:
                c.execute(sensor_query,t)
                conn.commit()
                return render_template('user_home_page.html')
        return render_template('sensor_register_page.html')
    else:
        error = "You are not logged in.Please Login"
        return render_template('login_page.html' ,error = error)

@app.route('/user_home_page', methods = ['GET','POST'])
def user_home_page():
    if session.get('logged_in'):    
        if request.method == 'POST':
            username = request.form['username']
            with conn:
                c.execute("SELECT sensor_name FROM sensor_data_table WHERE username = %s",(username,))
                conn.commit()
                x = c.fetchall()
                if(x):
                    with conn:
                        c.execute("SELECT username,sensor_name,sensor_data,upper_limit,lower_limit FROM sensor_data_table WHERE username = %s ",(username,))
                        conn.commit()     
                        rows = c.fetchall()
                        #if request.form['submit'] == 'VIEW SENSOR DATA':
                        return render_template("sensor_data_view_page.html",rows=rows) 
                        #elif request.form['submit'] == 'VIEW SENSOR DATA GRAPH':
                         #   return render_template("getgraph_option_page.html")
                        #else:
                         #   no_op = 0
                          #  no_op
                else:
                    error = "Username not registered. Please register first"
                    return render_template('user_home_page.html',error=error)
        return render_template('user_home_page.html')
    else:
        return home()

@app.route('/sid/<string:sid>', methods = ['GET', 'POST'])
def sid(sid):
    global sensor_id
    with conn:
        c.execute("SELECT sensor_key FROM sensor_data_table WHERE  sensor_key = %s",(sid,))
        conn.commit()
        x = c.fetchall()
        if(x):
            if(sid == x[0][0]):
                sensor_id = sid
                return render_template('user_home_page.html')
            else:
                error = "Sensor key is invalid. Please enter a valid key."
                return render_template('user_home_page.html',error=error)

@app.route('/getalert/<string:alert>', methods = ['GET', 'POST'])
def getalert(alert):
    print alert
    return render_template('user_home_page.html')


@app.route('/getdata/<string:moisture>', methods = ['POST', 'GET'])
def getdata(moisture):
    global moisture_value
    global sensor_id
    sensor_data = moisture
    if request.method == 'POST':
        print moisture
        moisture_value = moisture 
	print moisture_value
        #current_time = time.time()
        #print current_time
        if moisture == '5':
            alert = 'Moisture Level High'
        elif moisture == '3':
            alert = 'Moisture Level Okay'
        else:
            alert = 'Moisture Level Low'
        with conn:
            c.execute("SELECT username,sensor_name,lower_limit,upper_limit FROM sensor_data_table WHERE sensor_key = %s",(sensor_id,))
            conn.commit()
            rows= c.fetchall()
            for rows in rows:
                uname = rows[0]
                sname = rows[1]
                l_limit = rows[2]
                u_limit = rows[3] 
            sensor_query = "INSERT INTO sensor_data_table VALUES (%s,%s,%s,%s,%s,%s,%s)"
            t = (uname,sname,sensor_id,sensor_data,l_limit,u_limit,'0')
            with conn:
                c.execute(sensor_query,t)
                conn.commit()
                                        
	return render_template('user_home_page.html')  
    else:
	no_op = 0 
        no_op

		
@app.route('/delete_page',methods = ['GET','POST'])
def delete_page():
    if session.get('logged_in'):
        if request.method == 'POST':
            username = request.form['username']
            entered_pwd = request.form['password']
            print(username)
            with conn:
                c.execute("SELECT username, salt FROM user_data_table where username = %s",(username,))
                conn.commit()
                rows= c.fetchall()
                for rows in rows:
                    user = rows[0] 
                    salt = rows[1] 
                epass = getHash(entered_pwd+salt)
                completion = validate(username,epass)
                print(completion)
                if completion == False:
                    error = 'Wrong username or password. try again'
                    return render_template('login_page.html',error=error)
                else:
                    #print "hello"
                    with conn:
                        c.execute('''DELETE FROM user_data_table WHERE username = %s''',(username,))
                        conn.commit()
                    with conn:
                        c.execute('''DELETE FROM admin_data_table WHERE username = %s''',(username,))
                        conn.commit()
                    with conn:
                        c.execute('''DELETE FROM sensor_data_table WHERE username = %s''',(username,))
                        conn.commit()
                    response = redirect('/logout_page',code = 302)
                    return response
        return render_template('delete_page.html')    


@app.route('/sensor_limit_page',methods = ['GET','POST'])
def sensor_limit_page():
    if session.get('logged_in'):
        if request.method == 'POST':
            username = request.form['username']
            sensor_name = request.form['sensor_name']
            sensor_key = request.form['sensor_key']
            upper_limit = request.form['upper_limit']
            lower_limit = request.form['lower_limit']      
            with conn:
                c.execute("SELECT username FROM user_data_table WHERE username = %s",(username,))
                conn.commit()     
                x = c.fetchall()
                if(x):
                    no_op = 0
                    no_op
                else:
                    error = "Username not registered. Please register."
                    return render_template('sensor_limit_page.html',error = error)
            with conn:
                c.execute('''Select sensor_key FROM sensor_data_table WHERE sensor_name = %s''',(sensor_name,))
                conn.commit()
                x = c.fetchall()
                if(x):
                    if(sensor_key == x[0][0]):
                        with conn:
                            c.execute('''Select sensor_key FROM sensor_data_table WHERE sensor_name = %s''',(sensor_name,))
                            conn.commit()
                            y = c.fetchall()
                            if(y):
                                url = "https://192.168.1.149:4000/get_lowerlimit/"
                                url = url + str(lower_limit)
                                requests.post(url,verify = False)

                                url = "https://192.168.1.149:4000/get_upperlimit/"
                                url = url + str(upper_limit)
                                requests.post(url,verify = False)
                                
                                with conn:
                                    c.execute('''UPDATE sensor_data_table SET lower_limit = %s, upper_limit = %s WHERE sensor_key = %s''',(lower_limit,upper_limit,sensor_key))
                                    conn.commit()
                                response = redirect('/user_home_page', code = 302)
                                return response 
                    else:
                        error = "Wrong Sensor Key."
                        return render_template('sensor_limit_page.html', error = error)
                else:
                    error = "Sensor not registered. Please register sensor first."
                    return render_template('sensor_limit_page.html',error=error)
        return render_template('sensor_limit_page.html')
    else:
        error = "Please login first"
        return render_template('login_page.html',error = error)


@app.route('/register_new_user_page', methods=['GET', 'POST'])
def register_new_user_page():
    if request.method == 'POST':
        email_id = request.form['email_id']
        username = request.form['username'] 
        uname = (username)  
        password = request.form['password']
        password_conf = request.form['re_enter_password'] 
        with conn:
            c.execute("SELECT username FROM user_data_table WHERE username = %s",(username,))
            conn.commit()     
            x = c.fetchall()
            if(x):
                print(x[0])
                if (username == x[0][0]):
                    error = "Username Already Exists"
                    return render_template('register_new_user_page.html', error = error) 

        if(username != 'arsw7501'):
            admin_query = "INSERT INTO admin_data_table VALUES (%s,%s,%s)"
            t = (username,0,'no')
            try:
                c.execute(admin_query,t)
                conn.commit()
            except:
                no_op = 0
                no_op
        if password == password_conf:
            salt = urandom(32).encode('base-64')
            epass = getHash(password+salt)
            query = " INSERT INTO user_data_table VALUES (%s,%s,%s,%s,%s)"
            t = (username,email_id,epass,salt,"False")
            try:
                c.execute(query,t)
                conn.commit()
            except:
                no_op = 0
                no_op
            session['logged_in'] = False
            sub = "Verify your email"
            body = "https://192.168.1.51:5000/verify_page/"+uname
            server = smtplib.SMTP(smtp_server)
            server.ehlo()
            server.starttls()        
            server.ehlo()
            msg = """From: %s \nTo: %s \nSubject: %s\n\n%s """ % (fromaddr, ",".join(email_id), sub, body)
            server.login(fromaddr,pwd)
            server.sendmail(fromaddr,email_id,msg)
            server.quit()
            flash('Thank you for registering')
            bodyText = Markup("<b>\n Verification Link has been sent to your email. Please verify your email\n</b>")
            return render_template('preverify_page.html',bodyText = bodyText)
        else:
            error = "Passwords do not match"
            return render_template('register_new_user_page.html', error = error)
    return render_template('register_new_user_page.html')
   

@app.route('/verify_page/<string:uname>' ,methods = ['GET','POST'])
def verify_page(uname):
    session['logged_in'] = False
    try:    
        c.execute("SELECT username FROM user_data_table WHERE username = %s",(uname,))
        conn.commit() 
        x = c.fetchall()
        print(x)
    except:
        no_op = 0
        no_op
    
    if(uname == x[0][0]):         
        verified_value = "yes"
        print(verified_value)
        with conn:
            c.execute('''UPDATE admin_data_table SET verified_email = %s WHERE username = %s''',(verified_value,uname))
            conn.commit()
            #print("hello") 

        register_value = "True"
        try:
            c.execute('''UPDATE user_data_table SET register = %s WHERE username = %s''',(register_value,uname))
            conn.commit()
            bodyText = Markup("<b>\n Congratulations Your Email has been verified\n</b>")
            return render_template('verify_page.html',bodyText = bodyText)
        except:
            no_op = 0
            no_op
    else:
        verified = "no"        
        admin_query = "UPDATE admin_data_table SET verified_email = %s WHERE username = %s"
        t = (verified, uname)
        try:
            c.execute(admin_query,t)
            conn.commit()
        except:
            no_op = 0
            no_op

        query = "UPDATE user_data_table SET register = %s WHERE username = %s"
        register_value = "False"
        t = (register_value,uname)
        try:
            c.execute(query,t)
            conn.commit()
            bodyText = Markup("<b>\n Sorry Try Again</b>")
            return render_template('verify_page.html',bodyText = bodyText)
        except:
            no_op = 0
            no_op

@app.route('/login_page', methods=['POST'])
def login_page():
    global failed_attempt
    global failed_login_attempt
    global otp_sent
    global last_timestamp
    global last_timestamp1
    uname = request.form['username']
    entered_pwd = request.form['password']    
    body = str(randint(10000,1000000))
    sub = "OTP for web server login"
    otp_sent = body
    ip = request.remote_addr
    with conn:
        c.execute("SELECT login_attempt FROM login_ip_table WHERE IP_address = %s",(ip,))
        conn.commit()
        x = c.fetchall()
        if(x):
            no_op = 0
            no_op
        else:
            print(ip)
            with conn:
                query = "INSERT INTO login_ip_table VALUES (%s,%s)"
                count = 0
                t = (ip,count)
                c.execute(query,t)
                conn.commit()
    with conn:
        c.execute("SELECT username,email_id,salt,register FROM user_data_table where username = %s",(uname,))
        conn.commit()
        rows= c.fetchall()
        if(rows):
            for rows in rows:
                user = rows[0]
                e_id = rows[1]
                salt = rows[2]
                register = rows[3]
                epass = getHash(entered_pwd+salt)
                completion = validate(uname,epass)
        else:
            error = "Username not registered"
            return render_template('login_page.html',error=error)
            
        if register == "True":
            if completion == False: 
                failed_login_attempt = failed_login_attempt + 1
                print failed_login_attempt
                query = "UPDATE login_ip_table SET login_attempt = %s WHERE IP_address = %s"
                t = (failed_login_attempt , ip)
                with conn:
                    c.execute(query,t)
                    conn.commit()
                if failed_login_attempt == 5:
                    current_timestamp = time.time()
                    if(current_timestamp - last_timestamp < 60):
                        #print "hello hi how are you"
                        bodyText = Markup("<b>\n Login blocked. Wait for 5 mins</b>")
                        return render_template('block_user_page.html',bodyText = bodyText)
                    else:
                        failed_login_attempt = 0
                        query = "UPDATE login_ip_table SET login_attempt = %s WHERE IP_address = %s"
                        t = (failed_login_attempt , ip)
                        with conn:
                            c.execute(query,t)
                            conn.commit() 
                error = 'Wrong username or password. try again'
                last_timestamp = time.time()
                failed_attempt = failed_attempt + 1 
                if failed_attempt == 5:
                    current_timestamp1 = time.time()
                    if(current_timestamp1 - last_timestamp1 < 60):
                        #print "hello hi how are you"
                        bodyText = Markup("<b>\n Login blocked. Wait for 5 mins</b>")
                        return render_template('block_user_page.html',bodyText = bodyText)
                    else:
                        failed_attempt = 0
                        query = "UPDATE admin_data_table SET failed_login_attempts = %s WHERE username = %s"
                        t = (failed_attempt , uname)
                        with conn:
                            c.execute(query,t)
                            conn.commit()
                last_timestamp1 = time.time()
                admin_query = "UPDATE admin_data_table SET failed_login_attempts = %s WHERE username = %s"
                t = (failed_attempt, uname)
                with conn:
                    c.execute(admin_query,t)
                    conn.commit()
                return render_template('login_page.html',error=error)
            else:
                if failed_login_attempt == 5:
                    current_timestamp = time.time()
                    if(current_timestamp - last_timestamp < 60):
                        #print "hello hi how are you"
                        bodyText = Markup("<b>\n Login blocked. Wait for 5 mins</b>")
                        return render_template('block_user_page.html',bodyText = bodyText)
                    else:
                        failed_login_attempt = 0
                        query = "UPDATE login_ip_table SET login_attempt = %s WHERE IP_address = %s"
                        t = (failed_login_attempt , ip)
                        with conn:
                            c.execute(query,t)
                            conn.commit() 
                if failed_attempt == 5:
                    current_timestamp1 = time.time()
                    if(current_timestamp1 - last_timestamp1 < 60):
                        #print "hello hi how are you"
                        bodyText = Markup("<b>\n Login blocked. Wait for 5 mins</b>")
                        return render_template('block_user_page.html',bodyText = bodyText)
                    else:
                        failed_attempt = 0
                        query = "UPDATE admin_data_table SET failed_login_attempts = %s WHERE username = %s"
                        t = (failed_attempt , uname)
                        with conn:
                            c.execute(query,t)
                            conn.commit()
 
                failed_login_attempt = 0
                query = "UPDATE login_ip_table SET login_attempt = %s WHERE IP_address = %s"
                t = (failed_login_attempt , ip)
                with conn:
                    c.execute(query,t)
                    conn.commit()
                if(uname == "arsw7501"):
                    session['logged_in'] = True
                    response = redirect(url_for('admin_page'))
                    return response
                toaddr = e_id
                server = smtplib.SMTP(smtp_server)
                server.ehlo()
                server.starttls()        
                server.ehlo()
                msg = """From: %s \nTo: %s \nSubject: %s\n\n%s """ % (fromaddr, ",".join(toaddr), sub, body)
                server.login(fromaddr,pwd)
                server.sendmail(fromaddr,toaddr,msg)
                server.quit()
                failed_attempt = 0
                admin_query = "UPDATE admin_data_table SET failed_login_attempts = %s WHERE username = %s"
                t = (failed_attempt, uname)
                with conn:
                    c.execute(admin_query,t)
                    conn.commit()
                response = redirect(url_for('OTP_generate_page'))
                return response
        else:
            error = "Email has not been verified. Please verify the email"
            return render_template('login_page.html',error=error)

@app.route('/admin_page' , methods = ['GET','POST'])
def admin_page():
    if session.get('logged_in'):
        c.execute("SELECT * FROM admin_data_table")
        conn.commit()
        rows = c.fetchall()
        return render_template("admin_page.html",rows=rows)

@app.route('/OTP_generate_page',methods = ['GET', 'POST'])
def OTP_generate_page():
    global otp_sent
    if request.method == 'POST':
        otp = request.form['OTP'] 
        if otp == otp_sent:
            session['logged_in'] = True
            return home()
        else:
            error = 'Wrong OTP entered'
    return render_template('OTP_generate_page.html')

@app.route('/getgraph_option_page', methods = ['POST', 'GET'])
def getgraph_option_page():
    global s_key
    if session.get('logged_in'):
        if request.method == 'POST':
            sensor_key = request.form['sensor_key']
            with conn:
                c.execute("SELECT sensor_key FROM sensor_data_table WHERE sensor_key = %s",(sensor_key,))
                conn.commit()
                key = c.fetchall()
                if(key):
                    print (key)
                    s_key = sensor_key
                    response = redirect ('/getthegraph_page', code = 302)
                    return response 
                else:
                    error = 'Invalid Key'
                    return render_template('getgraph_option_page.html')
        return render_template('getgraph_option_page.html')

    else:
        error = 'User not logged in. Please log in.'
        return render_template('login_page.html', error = error)

@app.route('/getthegraph_page', methods = ['POST', 'GET'])
def getthegraph_page():
    global s_key 
    if session.get('logged_in'):
        with conn: 
            data = []
            data_length =[]
            c.execute("SELECT sensor_data FROM sensor_data_table WHERE sensor_key = %s", (s_key,))
            conn.commit()
            rows = c.fetchall()
            for rows in rows:
                data.append(rows[0])
            print data
            length = len(data)
            print length 
            for i in range(0,length):
                data_length.append(i+1)
            print data_length 
            data_float = map(float, data)
            data_count = map(str, data_length)
            print type(data_count)
            print type(data_float)
            #Chart(df, color = 'red')
           # p = Bar(data_count, label = 'moisture level', values = data_float, agg ='count', title = "Moisture Levels Recorded", bar_width = 0.4)
            output_file("templates/graph.html")
           # show(p)
            #src = "/home/aswami/secure_embedded_final/graph.html"
            #dst = "/home/aswami/secure_embedded_final/templates"
            #shutil.move(src,dst)
            p = figure(plot_width = 1000, plot_height = 1000, x_range = data_count)
            p.line(data_count, data_float, color = 'navy', alpha = 0.5)
            p.xaxis.major_label_orientation = np.pi/6
            show(p)
            return render_template('graph.html')
    else:
        error = "Please Login"
        return render_template('login_page.html', error = error)

@app.route('/logout_page')
def logout_page():
    session['logged_in'] = False
    session.clear()
    response = redirect('/',code = 302)
    return response
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False,host='192.168.1.51', port=5000, ssl_context = 'adhoc')
