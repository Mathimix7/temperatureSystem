import requests
from types import SimpleNamespace
import datetime
from graphCreator import graph

TOKEN = "5514463490:AAFm9eStS9HGtXCAqJMxXI7PSrbo5ctdb2Q"

class Interaction:
    def __init__(self, request):
        request = request["result"][0]
        try:
            dictUser = {"id": request["message"]["from"]["id"], "name": request["message"]["from"]["first_name"], "last_name": request["message"]["from"]["last_name"]}
            self.user = SimpleNamespace(**dictUser)
            self.message = request["message"]["text"]
            self.type = "message"
        except KeyError:
            dictUser = {"id": request["callback_query"]["from"]["id"], "name": request["callback_query"]["from"]["first_name"], "last_name": request["callback_query"]["from"]["last_name"]}
            self.user = SimpleNamespace(**dictUser)
            self.message = request["callback_query"]["data"]
            self.type = "button"

    def response(self, message: str, parse_mode:str=None, keyboard:dict={'remove_keyboard': True}):
        #data = {'reply_markup': {'inline_keyboard':[[{'text':'Yes',"callback_data":hellohru},{'text':'No',"callback_data":1}]]}}
        #data = {'reply_markup': {'keyboard':[[{'text':'Yes'},{'text':'No'}]]}}
        #data = {'reply_markup': {'remove_keyboard': True}}
        json = {'reply_markup': keyboard}
        data = {"parse_mode": parse_mode, } # markdown
        urlSend = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={self.user.id}&text={message}"
        a = requests.get(urlSend, data, json=json)
        print(a)
        print(a.json())

    def responsePhoto(self, photo):
        urlSend = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={self.user.id}"
        a = requests.post(urlSend, files={'photo': photo})
        print(a)
        print(a.json())

offset = 546022623

def help(interaction):
    pass

def now(interaction: Interaction):
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        data = ""
        for i in range(len(request)):
            name = request[i]["name"]
            now = datetime.datetime.now()
            hour, minute = now.strftime("%H:%M").split(":")
            timestamp = int((int(hour)*60 + int(minute))/10)-1
            temp = request[i]["temperature"][timestamp]
            hum = request[i]["humidity"][timestamp]
            time = str(datetime.datetime.fromtimestamp(request[i]["timestamps"][timestamp])).replace("-", "/")
            data = data + f"\n   - {name}: 🌡 {temp}°C - 🌧️ {hum}%"
        interaction.response(message=f"*Actual temperature and humidity:* {data}\n\n_Last data from: {time}_", parse_mode="markdown")
    except Exception as e:
        interaction.response("[502] Server internal error! please report with code 105669", e)

def today(interaction: Interaction):
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        buttons = []
        subButtons = []
        for i in range(len(request)):
            name = request[i]["name"]
            nameID = request[i]["id"]
            subButtons.append({'text':f'{name}',"callback_data":f"today-{name}:{nameID}"})
            if len(subButtons) == 2:
                buttons.append(subButtons)
                subButtons = []
        if len(subButtons) == 1:
            subButtons.append({'text':f'all',"callback_data":f"today-all:all"})
            buttons.append(subButtons)
        elif len(subButtons) == 0:
            buttons.append([{'text':f'all',"callback_data":f"today-all:all"}])
        keyboard = {'inline_keyboard':buttons}
        interaction.response(message=f"*Today Interaction Menu:*\n_Please select one option to continue..._", parse_mode="markdown", keyboard=keyboard)
    except Exception as e:
        interaction.response("[502] Server internal error! please report with code 105670", e)

def yesterday(interaction: Interaction):
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        buttons = []
        subButtons = []
        for i in range(len(request)):
            name = request[i]["name"]
            nameID = request[i]["id"]
            subButtons.append({'text':f'{name}',"callback_data":f"yesterday-{name}:{nameID}"})
            if len(subButtons) == 2:
                buttons.append(subButtons)
                subButtons = []
        if len(subButtons) == 1:
            subButtons.append({'text':f'all',"callback_data":f"yesterday-all:all"})
            buttons.append(subButtons)
        elif len(subButtons) == 0:
            buttons.append([{'text':f'all',"callback_data":f"yesterday-all:all"}])
        keyboard = {'inline_keyboard':buttons}
        interaction.response(message=f"*Yesterday Interaction Menu:*\n_Please select one option to continue..._", parse_mode="markdown", keyboard=keyboard)
    except Exception as e:
        interaction.response("[502] Server internal error! please report with code 105671", e)

def todayButton(interaction: Interaction):
    try:
        _, nameID = interaction.message.split(":")
        timestamps = []
        for i in range(144):
            i = i*10
            hour = str(int(i/60))
            minute = str(round((i/60 - int(i/60))*60))
            timestamps.append(f"{hour}:{minute}")
        now = datetime.datetime.now()
        hour, minute = now.strftime("%H:%M").split(":")
        timestamp = int((int(hour)*60 + int(minute))/10)-1
        if nameID.isnumeric():
            request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
            name = request["name"]
            temperature = []
            humidity = []
            for i in range(timestamp):
                temperature.append(request["temperature"][i])
                humidity.append(request["humidity"][i])
            data = [[temperature, humidity, name]]
            graph(timestamps, data, "Today")
            interaction.responsePhoto(open('graph.png', 'rb'))
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
            graph(timestamps, data, "Today")
            interaction.responsePhoto(open('graph.png', 'rb'))
        else:
            interaction.response("[104] Server internal error! working on a fix...")
    except Exception as e:
        interaction.response("[502] Server internal error! please report with code 105672", e)

def yesterdayButton(interaction: Interaction):
    try:
        _, nameID = interaction.message.split(":")
        timestamps = []
        for i in range(144):
            i = i*10
            hour = str(int(i/60))
            minute = str(round((i/60 - int(i/60))*60))
            timestamps.append(f"{hour}:{minute}")
        yesterday = datetime.datetime.now()-datetime.timedelta(days=1)
        unix_timestamp = int(datetime.datetime.timestamp(yesterday))
        if nameID.isnumeric():
            request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
            name = request["name"]
            request = requests.get(f"http://192.168.68.136:5555/day/{unix_timestamp}", json={"macAddress":request["macAddress"], "name": name, "id": nameID}).json()
            temperature = []
            humidity = []
            for i in range(144):
                temperature.append(request["temperature"][i])
                humidity.append(request["humidity"][i])
            data = [[temperature, humidity, name]]
            graph(timestamps, data, "Yesterday")
            interaction.responsePhoto(open('graph.png', 'rb'))
        elif nameID == "all":
            data = []
            request = requests.get(f"http://192.168.68.136:5555/").json()
            request2 = requests.get(f"http://192.168.68.136:5555/dayAll/{unix_timestamp}").json()
            for x in range(len(request)):
                name = request[x]["name"] 
                temperature = []
                humidity = []
                for i in range(144):
                    temperature.append(request2[x]["temperature"][i])
                    humidity.append(request2[x]["humidity"][i])
                data.append([temperature, humidity, name])
            graph(timestamps, data, "Yesterday")
            interaction.responsePhoto(open('graph.png', 'rb'))
        else:
            interaction.response("[105] Server internal error! working on a fix...")
    except Exception as e:
        interaction.response("[502] Server internal error! please report with code 105673", e)

def checkForNewUserButton(interaction: Interaction):
    try:
        _, result, id = interaction.message.split("-")
        if result == "no":
            interaction.response("Succesfully Rejected!")
        elif result == "yes":
            with open("telegram/usersID.txt", "r") as f:
                content = f.read()
            with open("telegram/usersID.txt", "w") as f:
                f.write(content+f",{id}")
            interaction.response("Succesfully added!")
            message = "You have been successfully granted permission to the bot. Use /help for help"
            urlSend = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={id}&text={message}"
            requests.get(urlSend) # Sent to the user
        elif result == "ignore":
            with open("telegram/ignoredusersID.txt", "r") as f:
                content = f.read()
            with open("telegram/ignoredusersID.txt", "w") as f:
                f.write(content+f",{id}")
            interaction.response("Succesfully added to ignore list!")
    except Exception as e:
        interaction.response("[502] Server internal error! please report with code 105674", e)

while True:
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}"
    request = requests.get(url).json()
    if request["result"]:
        interaction = Interaction(request)
        offset = request["result"][0]["update_id"] + 1
        with open("telegram/usersID.txt", "r") as f:
            users = f.read().split(",")
        if str(interaction.user.id) in users:
            if interaction.type == "message":
                if interaction.message == "/help":
                    help(interaction)
                if interaction.message == "/now":
                    now(interaction)
                if interaction.message == "/today":
                    today(interaction)
                if interaction.message == "/yesterday":
                    yesterday(interaction)
            elif interaction.type == "button":
                if interaction.message.startswith("today"):
                    todayButton(interaction)
                if interaction.message.startswith("yesterday"):
                    yesterdayButton(interaction)
                if interaction.message.startswith("confirmation"):
                    checkForNewUserButton(interaction)
        else:
            if interaction.message == "/start":
                with open("telegram/ignoredusersID.txt", "r") as f:
                    usersIgnored = f.read().split(",")
                if not str(interaction.user.id) in usersIgnored:
                    message = f"Do you want to allow {interaction.user.name} {interaction.user.last_name} to have access to the bot?"
                    urlSend = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=2126190570&text={message}"
                    buttons = [[{'text':f'Yes',"callback_data":f"confirmation-yes-{interaction.user.id}"}, {'text':f'No',"callback_data":f"confirmation-no-{interaction.user.id}"}, {'text':f'Ignore',"callback_data":f"confirmation-ignore-{interaction.user.id}"}]]
                    keyboard = {'inline_keyboard': buttons}
                    json = {'reply_markup': keyboard}
                    requests.get(urlSend, json=json) # Sent to me always
                    interaction.response("Hmm it seems like you are a new user who is not verified, please wait until you get confirmed. This may take some time...")  # Sent to the user