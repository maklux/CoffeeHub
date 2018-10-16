import os
from flask import Flask, request, render_template

# Initiate app
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Hello to Connected Coffee v0.1 - (c) MAK 2018'


@app.route('/on')
def on():
    timer = request.args.get('timer')
    action = request.args.get('action')
    return render_template('on.html', timer=timer, action=action)

@app.route('/off')
def off():
    message='turning machine off'
    return render_template('on.html', message=message)

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
  app.run()