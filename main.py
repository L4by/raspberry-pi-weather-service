import threading
import requests
import time
import subprocess
from sense_hat import SenseHat
from flask import Flask, jsonify, render_template, Response
sense = SenseHat()
sense.set_rotation(180)

class myFlask(Flask):
    def process_response(self, response):
        response.headers['server'] = 'LabyCustomWeb/1.0'
        return (response)

app = myFlask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/weather')
def index_weather():
    temp_c = sense.get_temperature()
    humidity_data = sense.get_humidity() 
    pressure_mb = sense.get_pressure() 
    cpu_temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
    array = cpu_temp.split(b"=")
    array2 = array[1].split(b"'")

    cpu_tempc = float(array2[0])
    cpu_tempc = float("{0:.2f}".format(cpu_tempc))

    temp_calibrated_c = temp_c - ((cpu_tempc - temp_c)/5.466)
    temp_calibrated_c = float("{0:.2f}".format(temp_calibrated_c))
    humidity_data = float("{0:.2f}".format(humidity_data))
    pressure_mb = float("{0:.2f}".format(pressure_mb))

    return jsonify(info_temperature=temp_calibrated_c, info_pressure=pressure_mb, info_humidity=humidity_data, about_curdate=int(time.time()), about_measure_location="todo with gps")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True, threaded=True)