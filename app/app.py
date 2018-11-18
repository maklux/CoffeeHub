import os
from flask import Flask, request, render_template
from rpi_rf import RFDevice

# Initiate app
app = Flask(__name__)

def switch(code):
    print('')
    rfdevice = RFDevice(17)
    rfdevice.enable_tx()
    rfdevice.tx_code(code, 1, 350)
    rfdevice.cleanup()

@app.route('/')
def welcome():
    return render_template('home.html',message='Hello to Connected Coffee v0.1 - (c) MAK 2018')

@app.route('/<device>/<action>')
def action(device, action):
    if action == 'on':
        switch(4474193)
        message = device + " just turned on. Enjoy your coffee!"
        action_text = "Turn Off"
    elif action == 'off':
        switch(4474196)
        message = device + ' just turned off. Give it some time to cool down. '
        action_text = "Turn On"
    else:
        message = 'Action not recognized. Please try again. Currently the following actions are available: on, off.'
        action_text = "Turn On"

    template_data = {
        'action' : action_text,
        'message' : message
    }
    return render_template('action.html', **template_data)

@app.route('/pipe')
def pipe():
    act = request.args.get("action")
    return action('mak',act)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)