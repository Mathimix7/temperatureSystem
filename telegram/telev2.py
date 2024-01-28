from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests
import datetime
from graphCreator import graph, graphWeekly
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

def start(update, context):
    user_id = update.effective_user.id
    if not str(user_id) in read_allowed_users():
        context.bot.send_message(chat_id=user_id, text="Hmm it seems like you are a new user who is not verified, please wait until you get confirmed. This may take some time...")
        admin_message = f"New user request:\nName: {update.effective_user.first_name} {update.effective_user.last_name}\nUser ID: {user_id}"
        context.bot.send_message(chat_id=2126190570, text=admin_message,
                                 reply_markup=get_admin_buttons(user_id))
    else:
        context.bot.send_message(chat_id=user_id, text="You have already been granted permission to use the bot. Use /help for assistance.")

def read_allowed_users():
    with open("usersID.txt", "r") as file:
        return [line.strip() for line in file]

def write_allowed_users(user_id):
    with open("usersID.txt", "a") as file:
        file.write(str(user_id) + "\n")

def get_admin_buttons(user_id):
    accept_button = InlineKeyboardButton('Accept', callback_data=f'start-accept:{user_id}')
    ignore_button = InlineKeyboardButton('Ignore', callback_data=f'start-ignore:{user_id}')
    keyboard = [[accept_button, ignore_button]]
    return InlineKeyboardMarkup(keyboard)

def button_accept_callback(update, context):
    query = update.callback_query
    action, user_id = query.data.split(':')
    user = context.bot.get_chat_member(chat_id=user_id, user_id=user_id).user
    if action == 'accept':
        write_allowed_users(user_id)
        context.bot.send_message(chat_id=int(user_id), text="You have been successfully granted permission to the bot. Use /help for assistance.")
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f"Successfully granted permission to {user.first_name} {user.last_name}.")
    elif action == 'ignore':
        context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=f"Ignored user request from {user.first_name} {user.last_name}.")


def help(update, context):
    if not str(update.effective_user.id) in read_allowed_users():
        return
    data = """
*Helpful Command List:*
- /help - Shows help info and commands
- /now - Get current temperature
- /today - Get today's temperature in the form of a graph!
- /yesterday - Get yesterday temperature in the form of a graph!
- /weekly - Get weekly temperature in the form of a graph!
- /monthly - Get monthly temperature in the form of a graph!
- /yearly - Get yearly temperature in the form of a graph!"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=data, parse_mode='Markdown')

def now(update, context):
    if not str(update.effective_user.id) in read_allowed_users():
        return
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
        data = f"*Actual temperature and humidity:* {data}\n\n_Last data from: {time}_"
        context.bot.send_message(chat_id=update.effective_chat.id, text=data, parse_mode='Markdown')
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="[502] Server internal error! please report with code 105669 " + e, parse_mode='Markdown')

def today(update, context):
    if not str(update.effective_user.id) in read_allowed_users():
        return
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        buttons = []
        subButtons = []
        for i in range(len(request)):
            name = request[i]["name"]
            nameID = request[i]["id"]
            subButtons.append(InlineKeyboardButton(text=name, callback_data=f"today-{name}:{nameID}"))
            if len(subButtons) == 2:
                buttons.append(subButtons)
                subButtons = []
        if len(subButtons) == 1:
            subButtons.append(InlineKeyboardButton(text='all', callback_data=f"today-all:all"))
            buttons.append(subButtons)
        elif len(subButtons) == 0:
            buttons.append([InlineKeyboardButton(text='all', callback_data=f"today-all:all")])
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text="*Today Interaction Menu:*\n_Please select one option to continue..._", parse_mode="markdown", reply_markup=reply_markup)
    except Exception as e:
        update.message.reply_text("[502] Server internal error! please report with code 105670")

def today_button_callback(update, context):
    query = update.callback_query
    _, nameID = query.data.split(":")
    timestamps = []
    for i in range(144):
        i = i * 10
        hour = str(int(i / 60))
        minute = str(round((i / 60 - int(i / 60)) * 60))
        timestamps.append(f"{hour}:{minute}")
    now = datetime.datetime.now()
    hour, minute = now.strftime("%H:%M").split(":")
    timestamp = int((int(hour) * 60 + int(minute)) / 10) - 1
    try:
        if nameID.isnumeric():
            request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
            name = request["name"]
            temperature = []
            humidity = []
            for i in range(timestamp):
                temperature.append(request["temperature"][i])
                humidity.append(request["humidity"][i])
            data = [[temperature, humidity, name, nameID]]
            graph(timestamps, data, "Today")
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
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
                data.append([temperature, humidity, name, request[x]["id"]])
            graph(timestamps, data, "Today")
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        else:
            query.message.reply_text("[104] Server internal error! working on a fix...")
    except Exception as e:
        query.message.reply_text("[502] Server internal error! please report with code 105672" + str(e))

def yesterday(update, context):
    if not str(update.effective_user.id) in read_allowed_users():
        return
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        buttons = []
        subButtons = []
        for i in range(len(request)):
            name = request[i]["name"]
            nameID = request[i]["id"]
            subButtons.append(InlineKeyboardButton(text=f'{name}', callback_data=f"yesterday-{name}:{nameID}"))
            if len(subButtons) == 2:
                buttons.append(subButtons)
                subButtons = []
        if len(subButtons) == 1:
            subButtons.append(InlineKeyboardButton(text='all', callback_data="yesterday-all:all"))
            buttons.append(subButtons)
        elif len(subButtons) == 0:
            buttons.append([InlineKeyboardButton(text='all', callback_data="yesterday-all:all")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        update.message.reply_text(text="*Yesterday Interaction Menu:*\n_Please select one option to continue..._", parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        update.message.reply_text(text="[502] Server internal error! please report with code 105671" + str(e))

def yesterday_button_callback(update, context):
    try:
        query = update.callback_query
        _, nameID = query.data.split(":")
        timestamps = []
        for i in range(144):
            i = i * 10
            hour = str(int(i / 60))
            minute = str(round((i / 60 - int(i / 60)) * 60))
            timestamps.append(f"{hour}:{minute}")
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        unix_timestamp = int(datetime.datetime.timestamp(yesterday))
        if nameID.isnumeric():
            request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
            name = request["name"]
            request = requests.get(f"http://192.168.68.136:5555/day/{unix_timestamp}", json={"macAddress": request["macAddress"], "name": name, "id": nameID}).json()
            temperature = []
            humidity = []
            for i in range(144):
                temperature.append(request["temperature"][i])
                humidity.append(request["humidity"][i])
            data = [[temperature, humidity, name, nameID]]
            graph(timestamps, data, "Yesterday")
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
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
                data.append([temperature, humidity, name, request[x]["id"]])
            graph(timestamps, data, "Yesterday")
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        else:
            query.message.reply_text(text="[105] Server internal error! working on a fix...")
    except Exception as e:
        query.message.reply_text(text="[502] Server internal error! please report with code 105673 " + str(e))

def weekly(update, context):
    if not str(update.effective_user.id) in read_allowed_users():
        return
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        buttons = []
        subButtons = []
        for i in range(len(request)):
            name = request[i]["name"]
            nameID = request[i]["id"]
            subButtons.append(InlineKeyboardButton(text=f'{name}', callback_data=f"weekly-{name}:{nameID}"))
            if len(subButtons) == 2:
                buttons.append(subButtons)
                subButtons = []
        if len(subButtons) == 1:
            subButtons.append(InlineKeyboardButton(text='all', callback_data="weekly-all:all"))
            buttons.append(subButtons)
        elif len(subButtons) == 0:
            buttons.append([InlineKeyboardButton(text='all', callback_data="weekly-all:all")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        update.message.reply_text(text="*Weekly Interaction Menu:*\n_Please select one option to continue..._", parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        update.message.reply_text(text="[502] Server internal error! please report with code 105671" + str(e))


def weekly_button_callback(update, context):
    try:
        query = update.callback_query
        _, nameID = query.data.split(":")
        timestamps = []
        days = 7
        weekly = datetime.datetime.now() - datetime.timedelta(days=days)
        today = datetime.datetime.now() + datetime.timedelta(days=1)
        unix_timestampWeekly = int(datetime.datetime.timestamp(weekly))
        unix_timestampToday = int(datetime.datetime.timestamp(today))
        if nameID.isnumeric():
            request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
            name = request["name"]
            request = requests.get(f"http://192.168.68.136:5555/start/{unix_timestampWeekly}/end/{unix_timestampToday}", json={"macAddress": request["macAddress"], "name": name, "id": nameID}).json()
            for i in range(len(request) * 144):
                i = i * 10
                hour = str(int(i / 60))
                minute = str(round((i / 60 - int(i / 60)) * 60))
                timestamps.append(f"{hour}:{minute}")
            temperature = []
            humidity = []
            for day in range(len(request)):
                for i in range(len(request[day]["temperature"])):
                    temperature.append(request[day]["temperature"][i])
                    humidity.append(request[day]["humidity"][i])
            data = [[temperature, humidity, name, nameID]]
            daysName = []
            for day in range(len(request)):
                daysName.append(datetime.datetime.fromtimestamp(request[day]["day"]).strftime("%d/%m"))
            graphWeekly(timestamps, data, "Weekly", daysName)
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        elif nameID == "all":
            data = []
            request = requests.get(f"http://192.168.68.136:5555/").json()
            allDataRequest = []
            allDataRequestName = []
            for device in request:
                allDataRequest.append(requests.get(f"http://192.168.68.136:5555/start/{unix_timestampWeekly}/end/{unix_timestampToday}", json={"macAddress": device["macAddress"], "name": device["name"], "id": device["id"]}).json())
                allDataRequestName.append({"macAddress": device["macAddress"], "name": device["name"], "id": device["id"]})
            for i in range(len(allDataRequest[0]) * 144):
                i = i * 10
                hour = str(int(i / 60))
                minute = str(round((i / 60 - int(i / 60)) * 60))
                timestamps.append(f"{hour}:{minute}")
            data = []
            for z, device in enumerate(allDataRequest):
                temperature = []
                humidity = []
                for day in range(len(device)):
                    for i in range(len(device[day]["temperature"])):
                        temperature.append(device[day]["temperature"][i])
                        humidity.append(device[day]["humidity"][i])
                data.append([temperature, humidity, allDataRequestName[z]["name"], allDataRequestName[z]["id"]])
            daysName = []
            for day in range(len(allDataRequest[0])):
                daysName.append(datetime.datetime.fromtimestamp(allDataRequest[0][day]["day"]).strftime("%d/%m"))
            graphWeekly(timestamps, data, "Weekly", daysName)
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        else:
            query.message.reply_text(chat_id=query.message.chat_id, text="[105] Server internal error! working on a fix...")
    except Exception as e:
        query.message.reply_text(chat_id=query.message.chat_id, text="[502] Server internal error! please report with code 105675 " + str(e))

def monthly(update, context):
    if not str(update.effective_user.id) in read_allowed_users():
        return
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        buttons = []
        subButtons = []
        for i in range(len(request)):
            name = request[i]["name"]
            nameID = request[i]["id"]
            subButtons.append(InlineKeyboardButton(text=f'{name}', callback_data=f"monthly-{name}:{nameID}"))
            if len(subButtons) == 2:
                buttons.append(subButtons)
                subButtons = []
        if len(subButtons) == 1:
            subButtons.append(InlineKeyboardButton(text='all', callback_data="monthly-all:all"))
            buttons.append(subButtons)
        elif len(subButtons) == 0:
            buttons.append([InlineKeyboardButton(text='all', callback_data="monthly-all:all")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        update.message.reply_text(text="*Monthly Interaction Menu:*\n_Please select one option to continue..._", parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        update.message.reply_text(text="[502] Server internal error! please report with code 105671" + str(e))

def monthly_button_callback(update, context):
    try:
        query = update.callback_query
        _, nameID = query.data.split(":")
        timestamps = []
        days = 28
        monthly = datetime.datetime.now() - datetime.timedelta(days=days)
        today = datetime.datetime.now() + datetime.timedelta(days=1)
        unix_timestampmonthly = int(datetime.datetime.timestamp(monthly))
        unix_timestampToday = int(datetime.datetime.timestamp(today))
        if nameID.isnumeric():
            request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
            name = request["name"]
            request = requests.get(f"http://192.168.68.136:5555/start/{unix_timestampmonthly}/end/{unix_timestampToday}", json={"macAddress": request["macAddress"], "name": name, "id": nameID}).json()
            for i in range(len(request) * 144):
                i = i * 10
                hour = str(int(i / 60))
                minute = str(round((i / 60 - int(i / 60)) * 60))
                timestamps.append(f"{hour}:{minute}")
            temperature = []
            humidity = []
            for day in range(len(request)):
                for i in range(len(request[day]["temperature"])):
                    temperature.append(request[day]["temperature"][i])
                    humidity.append(request[day]["humidity"][i])
            data = [[temperature, humidity, name, nameID]]
            daysName = []
            for day in range(len(request)):
                daysName.append(datetime.datetime.fromtimestamp(request[day]["day"]).strftime("%d/%m"))
            graphWeekly(timestamps, data, "Monthly", daysName)
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        elif nameID == "all":
            data = []
            request = requests.get(f"http://192.168.68.136:5555/").json()
            allDataRequest = []
            allDataRequestName = []
            for device in request:
                allDataRequest.append(requests.get(f"http://192.168.68.136:5555/start/{unix_timestampmonthly}/end/{unix_timestampToday}", json={"macAddress": device["macAddress"], "name": device["name"], "id": device["id"]}).json())
                allDataRequestName.append({"macAddress": device["macAddress"], "name": device["name"], "id": device["id"]})
            for i in range(len(allDataRequest[0]) * 144):
                i = i * 10
                hour = str(int(i / 60))
                minute = str(round((i / 60 - int(i / 60)) * 60))
                timestamps.append(f"{hour}:{minute}")
            data = []
            for z, device in enumerate(allDataRequest):
                temperature = []
                humidity = []
                for day in range(len(device)):
                    for i in range(len(device[day]["temperature"])):
                        temperature.append(device[day]["temperature"][i])
                        humidity.append(device[day]["humidity"][i])
                data.append([temperature, humidity, allDataRequestName[z]["name"], allDataRequestName[z]["id"]])
            daysName = []
            for day in range(len(allDataRequest[0])):
                daysName.append(datetime.datetime.fromtimestamp(allDataRequest[0][day]["day"]).strftime("%d/%m"))
            graphWeekly(timestamps, data, "Monthly", daysName)
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        else:
            update.message.reply_text(text="[105] Server internal error! working on a fix...")
    except Exception as e:
        update.message.reply_text(text="[502] Server internal error! please report with code 105675 " + str(e))

def yearly(update, context):
    if not str(update.effective_user.id) in read_allowed_users():
        return
    try:
        request = requests.get("http://192.168.68.136:5555/").json()
        buttons = []
        subButtons = []
        for i in range(len(request)):
            name = request[i]["name"]
            nameID = request[i]["id"]
            subButtons.append(InlineKeyboardButton(text=f'{name}', callback_data=f"yearly-{name}:{nameID}"))
            if len(subButtons) == 2:
                buttons.append(subButtons)
                subButtons = []
        if len(subButtons) == 1:
            subButtons.append(InlineKeyboardButton(text='all', callback_data="yearly-all:all"))
            buttons.append(subButtons)
        elif len(subButtons) == 0:
            buttons.append([InlineKeyboardButton(text='all', callback_data="yearly-all:all")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        update.message.reply_text(text="*Yearly Interaction Menu:*\n_Please select one option to continue..._", parse_mode="Markdown", reply_markup=keyboard)
    except Exception as e:
        update.message.reply_text(text="[502] Server internal error! please report with code 105671" + str(e))

def yearly_button_callback(update, context):
    try:
        query = update.callback_query
        _, nameID = query.data.split(":")
        timestamps = []
        days = 364
        weekly = datetime.datetime.now() - datetime.timedelta(days=days)
        today = datetime.datetime.now() + datetime.timedelta(days=1)
        unix_timestampWeekly = int(datetime.datetime.timestamp(weekly))
        unix_timestampToday = int(datetime.datetime.timestamp(today))
        if nameID.isnumeric():
            request = requests.get(f"http://192.168.68.136:5555/device/{nameID}").json()
            name = request["name"]
            request = requests.get(f"http://192.168.68.136:5555/start/{unix_timestampWeekly}/end/{unix_timestampToday}", json={"macAddress": request["macAddress"], "name": name, "id": nameID}).json()
            for i in range(len(request) * 144):
                i = i * 10
                hour = str(int(i / 60))
                minute = str(round((i / 60 - int(i / 60)) * 60))
                timestamps.append(f"{hour}:{minute}")
            temperature = []
            humidity = []
            for day in range(len(request)):
                for i in range(len(request[day]["temperature"])):
                    temperature.append(request[day]["temperature"][i])
                    humidity.append(request[day]["humidity"][i])
            data = [[temperature, humidity, name, nameID]]
            daysName = []
            for day in range(len(request)):
                daysName.append(datetime.datetime.fromtimestamp(request[day]["day"]).strftime("%d/%m"))
            graphWeekly(timestamps, data, "Yearly", daysName)
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        elif nameID == "all":
            data = []
            request = requests.get(f"http://192.168.68.136:5555/").json()
            allDataRequest = []
            allDataRequestName = []
            for device in request:
                allDataRequest.append(requests.get(f"http://192.168.68.136:5555/start/{unix_timestampWeekly}/end/{unix_timestampToday}", json={"macAddress": device["macAddress"], "name": device["name"], "id": device["id"]}).json())
                allDataRequestName.append({"macAddress": device["macAddress"], "name": device["name"], "id": device["id"]})
            for i in range(len(allDataRequest[0]) * 144):
                i = i * 10
                hour = str(int(i / 60))
                minute = str(round((i / 60 - int(i / 60)) * 60))
                timestamps.append(f"{hour}:{minute}")
            data = []
            for z, device in enumerate(allDataRequest):
                temperature = []
                humidity = []
                for day in range(len(device)):
                    for i in range(len(device[day]["temperature"])):
                        temperature.append(device[day]["temperature"][i])
                        humidity.append(device[day]["humidity"][i])
                data.append([temperature, humidity, allDataRequestName[z]["name"], allDataRequestName[z]["id"]])
            daysName = []
            for day in range(len(allDataRequest[0])):
                daysName.append(datetime.datetime.fromtimestamp(allDataRequest[0][day]["day"]).strftime("%d/%m"))
            graphWeekly(timestamps, data, "Yearly", daysName)
            photo_file = open('graph.png', 'rb')
            query.message.reply_photo(photo=photo_file)
            photo_file.close()
        else:
            update.message.reply_text(text="[105] Server internal error! working on a fix...")
    except Exception as e:
        update.message.reply_text(text="[502] Server internal error! please report with code 105675 " + str(e))

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CallbackQueryHandler(button_accept_callback, pattern='^start-'))

    dispatcher.add_handler(CommandHandler('help', help))

    dispatcher.add_handler(CommandHandler('now', now))

    dispatcher.add_handler(CommandHandler('today', today))
    dispatcher.add_handler(CallbackQueryHandler(today_button_callback, pattern='^today-'))

    dispatcher.add_handler(CommandHandler('yesterday', yesterday))
    dispatcher.add_handler(CallbackQueryHandler(yesterday_button_callback, pattern='^yesterday-'))

    dispatcher.add_handler(CommandHandler('weekly', weekly))
    dispatcher.add_handler(CallbackQueryHandler(weekly_button_callback, pattern='^weekly-'))

    dispatcher.add_handler(CommandHandler('monthly', monthly))
    dispatcher.add_handler(CallbackQueryHandler(monthly_button_callback, pattern='^monthly-'))

    dispatcher.add_handler(CommandHandler('yearly', yearly))
    dispatcher.add_handler(CallbackQueryHandler(yearly_button_callback, pattern='^yearly-'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
