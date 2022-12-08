import requests

request = requests.get(f"http://192.168.68.136:5555/device/{1}").json()
print(request)