import pyowm 
import mraa
import datetime
import time 
from time import strftime 
import pytz


passkey = pyowm.OWM('c883917f37fa006bd8c959f8eb662d18')
location = passkey.weather_at_place("Bengaluru,in")
weather = location.get_weather()
temperature_at_location = weather.get_temperature('celsius')
list_temp = list(temperature_at_location.values())
location_temp = int(list_temp[2])
print(location_temp)

#logging values 
with open(temperature_list.txt','w') as file:
	file.write('')
with open('temperature_list.txt','a') as file:
	file.write(repr(location_temp))
	
