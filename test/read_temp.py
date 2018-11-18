import time

def read_temp(id):
	with open("/sys/bus/w1/devices/" + id  + "/w1_slave") as tempfile:
		res = tempfile.read()
	tempdata = res.split("\n")[1].split(" ")[9]
	res_clean = float(tempdata[2:])
	res_celcius = res_clean / 1000
	return res_celcius

while 1:
	temp1 = read_temp("28-041700305eff")
	print("Sensor 1: ", temp1)
	temp2 = read_temp("28-0517001488ff")
	print("Sensor 2:", temp2)
