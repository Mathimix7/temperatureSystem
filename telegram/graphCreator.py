from copy import deepcopy
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np

colorList = ["blue", "green", "red", "purple", "cyan", "orange", "brown", "pink", "gray", "olive"]

def round_down(num, divisor=5):
    return num - (num%divisor)

def round_up(num, divisor=5):
    return num if num % divisor == 0 else num + divisor - (num % divisor)

def graph(timestamps, data, day):
	figure, axis = plt.subplots(2, constrained_layout=True)
	figure.set_size_inches((9,7))
	figure.set_facecolor("black")
	axis[1].set_facecolor("black")
	axis[0].set_facecolor("black")
	#Temperature
	tempMaximum = -1000
	humMaximum = -1000
	tempMinimum = 1000
	humMinimum = 1000
	datatemps = []
	for i in range(len(data)):
		for x in range(len(data[i][0])):
			if data[i][0][x] != "N/A":
				datatemps.append(data[i][0][x])
	datahums = []
	for i in range(len(data)):
		for x in range(len(data[i][1])):
			if data[i][1][x] != "N/A":
				datahums.append(data[i][1][x])
	tempMaximum = round_up(max(datatemps))
	humMaximum = round_up(max(datahums))
	tempMinimum = round_down(min(datatemps))
	humMinimum = round_down(min(datahums))
	for x in range(len(data)):
		temperature2 = deepcopy(data[x][0])
		for i in range(len(temperature2)):
			if temperature2[i] == "N/A":
				temperature2[i] = None
		for i in range(len(timestamps) - len(temperature2)):
			temperature2.append(None)
		axis[0].plot(timestamps, temperature2, color = colorList[x], label=f"{data[x][2]} Temp")
	axis[0].set_title(f'Temperature {day}')
	axis[0].legend(loc="upper right", framealpha=0.7)
	axis[0].set_xlim([0, max(timestamps)])
	listxticks = []
	listxticksnames = []
	for i in range(12):
		listxticks.append(timestamps[i*12])
		listxticksnames.append(timestamps[i*12].split(":")[0]+"h")
	listxticks.append("24:00")
	listxticksnames.append("24h")
	axis[0].set_xticks(listxticks, listxticksnames)
	dif = (tempMaximum-tempMinimum)/5
	yticks = np.arange(tempMinimum, tempMaximum+1, dif)
	yticksnames = []
	for i in range(len(yticks)):
		yticksnames.append(str(round(yticks[i]))+"°C")
	axis[0].set_yticks(yticks, yticksnames)
	axis[0].grid()
	#Humidity
	for x in range(len(data)):
		humidity2 = deepcopy(data[x][1])
		for i in range(len(humidity2)):
			if humidity2[i] == "N/A":
				humidity2[i] = None
		for i in range(len(timestamps) - len(humidity2)):
			humidity2.append(None)
		axis[1].plot(timestamps, humidity2, color = colorList[x], label=f"{data[x][2]} Hum")
	axis[1].set_title(f'Humidity {day}')
	axis[1].legend(loc="upper right", framealpha=0.7)
	axis[1].set_xlim([0, max(timestamps)])
	listxticks = []
	listxticksnames = []
	for i in range(12):
		listxticks.append(timestamps[i*12])
		listxticksnames.append(timestamps[i*12].split(":")[0]+"h")
	listxticks.append("24:00")
	listxticksnames.append("24h")
	axis[1].set_xticks(listxticks, listxticksnames)
	dif = (humMaximum-humMinimum)/5
	yticks = np.arange(humMinimum, humMaximum+1, dif)
	yticksnames = []
	for i in range(len(yticks)):
		yticksnames.append(str(round(yticks[i]))+"%")
	axis[1].set_yticks(yticks, yticksnames)
	axis[1].grid()
	axis[1].spines['bottom'].set_color('white')
	axis[1].spines['top'].set_color('white') 
	axis[1].spines['right'].set_color('white')
	axis[1].spines['left'].set_color('white')
	axis[0].spines['bottom'].set_color('white')
	axis[0].spines['top'].set_color('white') 
	axis[0].spines['right'].set_color('white')
	axis[0].spines['left'].set_color('white')
	axis[0].tick_params(axis='x', colors='white')
	axis[0].tick_params(axis='y', colors='white')
	axis[1].tick_params(axis='x', colors='white')
	axis[1].tick_params(axis='y', colors='white')
	axis[1].yaxis.label.set_color('white')
	axis[1].xaxis.label.set_color('white')
	axis[0].yaxis.label.set_color('white')
	axis[0].xaxis.label.set_color('white')
	axis[0].title.set_color('white')
	axis[1].title.set_color('white')
	plt.savefig("graph.png")

def asd(nameID):
	timestamps = []
	for i in range(144):
		i = i*10
		hour = str(int(i/60))
		minute = str(round((i/60 - int(i/60))*60))
		timestamps.append(f"{hour}:{minute}")
	now = datetime.datetime.now()
	hour, minute = now.strftime("%H:%M").split(":")
	timestamp = int((int(hour)*60 + int(minute))/10)-1
	if isinstance(nameID, int):
		request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
		name = request["name"]
		temperature = []
		humidity = []
		for i in range(timestamp):
			temperature.append(request["temperature"][i])
			humidity.append(request["humidity"][i])
		data = [[temperature, humidity, name]]
		graph(timestamps, data)
	elif nameID == "all":
		data = []
		request = requests.get(f"http://192.168.68.136:5555/").json()
		for x in range(len(request)):
			name = request[x]["name"] 
			temperature = []
			humidity = []
			for i in range(timestamp):
				temperature.append(request[x]["temperature"][i])
				humidity.append(request[x]["humidity"][i])
			data.append([temperature, humidity, name])
		graph(timestamps, data)

#asd("all")