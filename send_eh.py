import time
import json
import socket
import time
from gpiozero import LED
from azure.servicebus import ServiceBusService

key_name = 'mysecretkeyname'
key_value = 'mysecretkeyvalue'
service_namespace = 'eventhub namespace'
eventhub_name = 'eventhub name'
interval = 30 #seconds
sensor1 = "28-041700305eff"
sensor2 = "28-0517001488ff"
led_red = LED(17)
led_green = LED(18)
 
host = socket.gethostname()
sbs = ServiceBusService(service_namespace,
shared_access_key_name=key_name,
shared_access_key_value=key_value)
sbs.create_event_hub(eventhub_name)


# Fetch data from sensors
def read_temp(id):
    try:
        with open("/sys/bus/w1/devices/" + id + "/w1_slave") as f:
            temp = f.read()
        temp = temp.split("\n")[1].split(" ")[9]
        temp = float(temp[2:]) / 1000
    except OSError:
        temp = 0.0
    return temp

while True:
    temp1 = read_temp(sensor1)
    temp2 = read_temp(sensor2)
    unix = int(time.time())
    
    if temp1 > 90:
        ready = True
        led_green.on()
    else:
        ready = False
        led_green.off()

    if temp1 > 30:
        on = True
        led_red.on()
    else:
        on = False
        led_red.off()

    data = {'Hostname': host, 'Timestamp': unix, 'Temperature1': temp1, 'Temperature2': temp2, 'On': on 'Ready': ready}
    msg = json.dumps(data)
    print(msg)
    sbs.send_event(eventhub_name, msg)

    time.sleep(interval)