import time
import json
import socket
import time
import datetime
from gpiozero import LED
from azure.servicebus import ServiceBusService

# Connection strings for Event Hub
secrets = json.load(open('secrets.json'))
key_name = secrets['key_name']
key_value = secrets['key_value']
service_namespace = secrets['service_namespace']
eventhub_name = secrets['eventhub_name']

# Establish connection to Event Hub
host = socket.gethostname()
sbs = ServiceBusService(service_namespace,
shared_access_key_name=key_name,
shared_access_key_value=key_value)
sbs.create_event_hub(eventhub_name)

# Parameters
interval = 10 #seconds
sensor1 = "28-041700305eff"
sensor2 = "28-0517001488ff"
led_red = LED(23)
led_green = LED(24)

# Current timestamp
start_time = datetime.datetime.now()

# Error Tracker
error = False 

# Status timestamps
timer_on = None
timer_ready = None

# Fetch values from sensors
def read_temp(id):
    global error

    try:
        with open("/sys/bus/w1/devices/" + id + "/w1_slave") as f:
            temp = f.read()
        temp = temp.split("\n")[1].split(" ")[9]
        temp = float(temp[2:]) / 1000
    except OSError:
        temp = 0.0
        error = True
        print('>Read Error<')
    return temp

def set_time(start_time, end_time):
    return round((end_time - start_time).total_seconds() / 60.0,2)

while True:
    # Read sensor values
    temp1 = read_temp(sensor1)
    temp2 = read_temp(sensor2)

    # Create timestamp
    now = datetime.datetime.now()
    
    # Flag for when machine is on
    if temp1 > 30:
        on = True
        led_red.on()
        if timer_on is None:
            timer_on_start = now
        timer_on = set_time(timer_on_start, now)
    else:
        on = False
        timer_on = None
        led_red.off()

    # Flag for espresso temperature reached
    if temp1 > 90:
        ready = True
        led_green.on()
        if timer_ready is None:
            timer_ready_start = now
        timer_ready = set_time(timer_ready_start, now)
    else:
        ready = False
        timer_ready = None
        led_green.off()

    # Startup Signal
    if (now - start_time) < datetime.timedelta(0,20):
        led_red.on()
        led_green.on()

    # Package data
    data = dict(
        Hostname = host, 
        Timestamp = str(now), 
        Temperature1 = temp1, 
        Temperature2 = temp2, 
        On = on, 
        DurationOn = str(timer_on),
        Ready = ready,
        DurationReady = str(timer_ready)
    )
    msg = json.dumps(data)
    print(msg)
    # Send to event hub
    if not error:
        try:
            sbs.send_event(eventhub_name, msg)
        except Exception as e:
            print("ERROR sending data to event hub. Check if the event hub is up and running: ", str(e))
        # Reset error for next round
        error = False

    time.sleep(interval)
