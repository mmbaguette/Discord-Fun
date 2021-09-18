from discord_hacks import send_message
import os
import time
import threading

f = open(os.getcwd() + r"\auth.txt","r")
authorization = f.read()
channelID = "857175893629468682"
message = "_"
messageToAppend = "<@!662766320298754108>"
maxChars = 4000
f.close()

while len(message) + len(messageToAppend) < maxChars - 1:
    message += messageToAppend
message += "_"

def spam():
    while True:
        resp = send_message(message, channelID, authorization)

        if type(resp) is int:
            cooldown = 1 + resp
            print("Cooldown for %s", str(cooldown))
            time.sleep(cooldown)

spam1 = threading.Thread(target=spam)
spam2 = threading.Thread(target=spam)
spam3 = threading.Thread(target=spam)
spam4 = threading.Thread(target=spam)
spam1.start()
spam2.start()
spam3.start()
spam4.start()