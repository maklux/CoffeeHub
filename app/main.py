from flask import Flask, request

# Initiate app
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Hello to Connected Coffee v0.1'


@app.route('/make')
def load_input():
    # Load variables
    try:
        pwd = request.args.get('pass')
    except Exception as e:
        pwd = ''
        res = 'Error: No Password Provided'
        return res 

    try:
        action = request.args.get('act')
    except Exception as e:
        action = ''    
        res = 'Error: No Action Provided'
        return res

    # Resolve variables
    if pwd == 'mak':
        res = action
    else: 
        res = 'Login failed.'
    return res

if __name__ == '__main__':
  app.run() #host='0.0.0.0',debug=False