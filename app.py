#!usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, make_response
import motors
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) #set up GPIO
GPIO.setwarnings(False)

app = Flask(__name__) #set up flask server
app.secret_key=os.urandom(24)
#when the root IP is selected, return index.html page
@app.route('/')
def index():
        return render_template('index.html')

#recieve which pin to change from the button press on index.html
#each button returns a number that triggers a command in this function
#
#Uses methods from motors.py to send commands to the GPIO to operate the motors
@app.route('/move', methods =['POST'])
def move():
	
        if form.action == "up":
                motors.tiltUp()
                
	response = make_response(redirect(url_for('index')))
	return(response)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True) #set up the server in debug mode to the port 5000
