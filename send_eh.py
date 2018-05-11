import time
import json
import socket
import time
import datetime
from gpiozero import LED
from azure.servicebus import ServiceBusService

# Connection strings for Event Hub
key_name = 'mysecretkeyname'
key_value = 'mysecretkeyvalue'
service_namespace = 'coffeeevents'
eventhub_name = 'pavoni'

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
led_red = LED(17)
led_green = LED(27)

# Current timestamp
start_time = datetime.datetime.now()

# Fetch values from sensors
def read_temp(id):
    try:
        with open("/sys/bus/w1/devices/" + id + "/w1_slave") as f:
            temp = f.read()
        temp = temp.split("\n")[1].split(" ")[9]
        temp = float(temp[2:]) / 1000
        error = False
    except OSError:
        temp = 0.0
        error = True
        print('>Read Error<')
    return temp, error

while True:
    # Read sensor values
    temp1, error1 = read_temp(sensor1)
    temp2, error2 = read_temp(sensor2)
    # Create timestamp
    now = datetime.datetime.now()
    
    # Flag for when machine is on
    if temp1 > 30:
        on = True
        led_red.on()
    else:
        on = False
        led_red.off()

    # Flag for espresso temperature reached
    if temp1 > 90:
        ready = True
        led_green.on()
    else:
        ready = False
        led_green.off()

    # Startup Signal
    if (now - start_time) < datetime.timedelta(0,20):
        led_red.on()
        led_green.on()

    # Package data
    data = {'Hostname': host, 'Timestamp': str(now), 'Temperature1': temp1, 'Temperature2': temp2, 'On': on, 'Ready': ready}
    msg = json.dumps(data)
    print(msg)
    # Send to event hub
    if not error1:
        sbs.send_event(eventhub_name, msg)

    time.sleep(interval)
