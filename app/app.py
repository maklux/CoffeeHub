import os
from flask import Flask, request, render_template
from rpi_rf import RFDevice

# Initiate app
app = Flask(__name__)

def switch(code):
    rfdevice = RFDevice(17)
    rfdevice.enable_tx()
    rfdevice.tx_code(code, 1, 350)
    rfdevice.cleanup()

@app.route('/')
def welcome():
    return 'Hello to Connected Coffee v0.1 - (c) MAK 2018'

@app.route('/on')
def on():
    switch(4474193)
    message = "Pavoni just turned on. Enjoy your coffee!"
    action="Turn Off"
    return render_template('on.html', message=message, action=action)

@app.route('/off')
def off():
    switch(4474196)
    message='Pavoni just turned off. Give it some time to cool down. '
    action="Turn On"
    return render_template('on.html', message=message, action=action)

@app.route('/test')
def load_input():
    # Load variables
    pwd = request.args.get('pwd')
    action = request.args.get('action')

    # Resolve variables
    if pwd == 'mak':
        if action is None:
            res = 'Error: No action Provided'
        else:
            res = action
    else: 
        res = 'Error: Login failed'

    return res

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)