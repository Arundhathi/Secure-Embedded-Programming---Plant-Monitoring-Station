#develop code to display webapage with functionalities from previous assignments using flask
import mraa
import pytz

from flask import Flask 
from flask import render_template
from flask import Markup 
from flask import request
from flask_bootstrap import Bootstrap
from time import strftime 
from datetime import datetime 
from pytz import timezone 

fmt = "%Y-%m-%d %H:%M:%S"
fmta = "%H:%M:%S"

#set of instructions to initialise both buttons a and b and the led  
buttona = mraa.Gpio(2)
buttona.dir(mraa.DIR_IN)
buttonb = mraa.Gpio(4)
buttonb.dir(mraa.DIR_IN)
led = mraa.Gpio(7)
led.dir(mraa.DIR_OUT)
temp_read = mraa.Aio(0)
temp_read.setBit(12)

#declaring variables  to store button state reads as pressed or not pressed 
current_state_a = 0
last_state_a  = 0
current_state_b = 0
last_state_b = 0

#defining timezones
now_utc = datetime.now(timezone('UTC'))
now_mountain = now_utc.astimezone(timezone('US/Mountain'))


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/ButtonClick')
def ButtonClick():
    now_utc = datetime.now(timezone('UTC'))
    current_state_a = buttona.read() #reads state of button a
    current_state_b = buttonb.read() #reads state of button b 
    if (current_state_a == 1):
        #current_timea = now_utc.astimezone(timezone('US/Mountain')
        bodyText = Markup("<b>Button A Connected __\n</b>")
                       
    elif (current_state_b == 1):
       # current_timeb = now_utc.astimezone(timezone('US/Mountain'))
        bodyText = Markup("<b>Button B Connected __\n</b>")

    else:
        bodyText = Markup("<b>No Buttons Active\n</b>")

    return render_template ('button.html', bodyText = bodyText)

@app.route('/Temperature')
def Temperature():
    temp_raw = temp_read.read()
    v = float(temp_raw/819.0)
    C_deg = ((v*100.0)-50.0)
    F_deg = (((C_deg*9.0)/5.0)+32.00)
   
    bodyText = Markup("<b>Temperature in deg Celcius: \n </b>"+str(C_deg))
    return render_template('temperature.html',bodyText = bodyText)

 
@app.route('/LedDisco/<int:state>')
def LedDisco(state):
    if (state==1):
        led.write(1)
        bodyText = Markup ("<b> LED is ON</b>")
    else:
        led.write(0)
        bodyText = Markup ("<b> LED is OFF</b>")
    return render_template('led.html', bodyText = bodyText)

if __name__ == '__main__':
    app.debug = False 
    app.run(host='0.0.0.0',port=8000)

