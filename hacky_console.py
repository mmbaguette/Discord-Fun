import discord_hacks
import inspect
import threading
import animate_message
import os

f = open(os.getcwd() + r"\auth jer.txt","r")
params = {
    "channelID": "",
    "guildID": "", # server id
    "messageID": "",
    "authorization": f.read(),
    "text": "",
    "nickname": "",
    "username": "",
    "blankspace": "",
    "total_length": "",
    "cover": "",
    "limit": "",
    "invite": ""
}
f.close()

while True:
    hackName = input("\nEnter a hack or change a parameter: ")

    if hackName in params:
        newValue = input("Enter a new value for this parameter: ")

        if hackName == "authorization":
            filePath = f"{os.getcwd()}\\{newValue}"
            f = open(filePath, "r")

            if os.path.exists(filePath):
                params["authorization"] = f.read()
                f.close()
        else:
            params[hackName] = newValue
    elif hackName.endswith("()"):
        methodName = hackName[:-2].lower()

        if methodName == "send_message" or methodName == "send":
            if discord_hacks.send_message(params["text"], params["channelID"], params["authorization"]):
                print("Successfully sent message!")
            else:
                print("Parameters: " + params["text"] + " " + params["channelID"] + " AUTHORIZATION")
        elif methodName == "delete_message" or methodName == "delete":
            if discord_hacks.delete_message(params["channelID"], params["messageID"], params["authorization"]):
                print("Successfully deleted message!")
        elif methodName == "edit_message" or methodName == "edit":
            if discord_hacks.edit_message(params["text"], params["channelID"], params["messageID"], params["authorization"]):
                print("Successfully edit message!")
        elif methodName == "join_server" or methodName == "join":
            join_status = discord_hacks.join_server(params["invite"], params["authorization"])
            print(join_status)
        elif methodName == "change_nickname" or methodName == "nickname" or methodName == "nick":
            if discord_hacks.change_nickname(params["nickname"], params["guildID"], params["authorization"]):
                print("Successfully changed nickname!")
        elif methodName == "send_dm" or methodName == "dm":
            if discord_hacks.send_DM(params["username"], params["text"], params["authorization"]):
                print("Successfully sent DM message!")
        elif methodName == "get_guilds" or methodName == "guilds":
            guilds = discord_hacks.get_guilds(params["authorization"])

            if type(guilds) is list: # not none
                print("Discord servers:")

                for guild in guilds:
                    print(guild["name"] + ": " + guild["id"])
            else:
                print("Could not fetch guilds.")
        elif methodName == "get_dms" or methodName == "dms":
            DMs = discord_hacks.get_DMs(params["authorization"])

            if type(DMs) is list: # not none
                print("Direct messages:")

                for DM in DMs:
                    for user in DM["recipients"]:
                        print(user["username"] + "#" + user["discriminator"] + ": " + DM["id"])
            else:
                print("Could not fetch DMs.")
        elif methodName == "get_channels" or methodName == "channels":
            channels = discord_hacks.get_channels(params["guildID"], params["authorization"])

            if type(channels) is list: # not none
                print("Discord channels:")

                for channel in channels:
                    print(channel["name"] + ": " + channel["id"])
            else:
                print("Could not fetch channels.")
        elif methodName == "get_messages" or methodName == "get":
            print("Make sure you have the messageID for the last message you want to get.")
            messages = discord_hacks.get_messages(params["channelID"], params["authorization"], lastMessageID=params["messageID"], limit=params["limit"])
            
            if messages:
                messages.reverse() # reverse messages list
                for messageObj in messages:
                    print("\n" + messageObj["author"]["username"] + "#" + messageObj["author"]["discriminator"] + ": ")
                    print("\t" + messageObj["content"])

                    for attachment in messageObj["attachments"]:
                        if "url" in attachment:
                            print("\t" + attachment["url"])

                    for embed in messageObj["embeds"]:
                        if "url" in embed:
                            print("\t" + embed["url"])
            else:
                print("Could not fetch messages, or channel is empty.")
        elif methodName == "scroll_text" or methodName == "scroll":
            args = (params["message"], params["channelID"], params["blankspace"], params["total_length"], params["blankspace"], params["cover"],  params["authorization"])
            thread = threading.Thread(animate_message.scroll_text(), args=args)
            thread.start()
            print("Successfully started scrolling text!") # where's the if?
    else:
        try:
            paramNames = inspect.getfullargspec(getattr(discord_hacks, hackName))
            print("\nParameters required:")
            print(paramNames)
        except:
            print(f"\nDid you mean \"{hackName}()\"?")