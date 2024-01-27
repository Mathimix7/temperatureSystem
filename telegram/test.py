import requests
groupNumber = 1
RequestLink = f'http://192.168.68.103/api/tsbtK0JdOtfyfIZh64L8RJPMQM70Ght5GRl7stYT/groups/{groupNumber}'
groupBrightness = requests.get(RequestLink).json()
groupBrightness = groupBrightness['action']['bri']
groupBrightnessDecrease = 31
print(groupBrightness, str(int(groupBrightness - groupBrightnessDecrease)))
a = requests.put(f'http://192.168.68.103/api/tsbtK0JdOtfyfIZh64L8RJPMQM70Ght5GRl7stYT/groups/{groupNumber}/action', data='{"bri":' + str(int(groupBrightness - groupBrightnessDecrease)) + '}')
print(a.json())