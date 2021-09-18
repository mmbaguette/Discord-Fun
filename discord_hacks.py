import requests as req
import json
import os

message = ""
username = "" # discord username + "#" + user's tag containing four digits
channelID = ""
messageID = ""
f = open(os.getcwd() + r"\auth.txt","r")
authorization = f.read()
f.close()

def get_guilds(auth):
    url_g = f"https://discord.com/api/v9/users/@me/guilds"
    headers = {"authorization": auth}

    g = req.get(url_g,headers=headers)

    if g.status_code == 200:
        guilds = json.loads(g.text)
        return guilds
    else:
        print(g.status_code)
        print(g.text)

def get_channels(guildID, auth):
    url_c = f"https://discord.com/api/v9/guilds/{guildID}/channels"
    headers = {"authorization": auth}

    c = req.get(url_c,headers=headers)

    if c.status_code == 200:
        channels = json.loads(c.text)
        return channels
    else:
        print(c.status_code)
        print(c.text)
def join_server(invite, auth):
    url_j = "https://discord.com/api/v9/invites/%s" % invite
    headers = {"authorization": auth}

    j = req.post(url_j, headers=headers)

    if j.status_code == 200:
        response = json.loads(j.text)
        return response
    else:
        print(j.status_code)
        print(j.text)

def get_DMs(auth):
    url_c = "https://discord.com/api/v9/users/@me/channels" # url for getting user's DMs
    headers = {"authorization": auth} # needed for authorization
    
    c = req.get(url_c,headers=headers) # get all DMs

    if c.status_code == 200:
        DMs = json.loads(c.text) # turn DMs data text into dictionary
        return DMs
    else:
        print(c.status_code)
        print(c.text)

def send_DM(username, text, auth):
    url_c = "https://discord.com/api/v9/users/@me/channels" # url for getting user's DMs
    data =  {"content": text} # data for sending message
    headers = {"authorization": auth} # needed for authorization
    
    c = req.get(url_c,headers=headers) # get all DMs
    DMs = json.loads(c.text) # turn DMs data text into dictionary

    for DM in DMs:
        for user in DM["recipients"]:
            if user["username"] + "#" + user["discriminator"] == username: # if this DM's username is the one we're looking for
                channelID = DM["id"]
                url_m = "https://discord.com/api/v9/channels/" + str(channelID) + "/messages" # url for sending messages

                m = req.post(url_m,headers=headers,data=data) # send message request
                
                if m.status_code != 200:
                    print(m.status_code)
                    print(m.text)
                    return False
                else: # success
                    return str(json.loads(m.text)["id"])

def send_message(text, channelID, auth):
    data =  {"content": text} # data for sending message
    headers = {"authorization": auth} # needed for authorization

    url_m = "https://discord.com/api/v9/channels/" + str(channelID) + "/messages" # url for sending messages

    m = req.post(url_m, headers=headers, data=data) # send message request
    
    if m.status_code == 200:
        return str(json.loads(m.text)["id"])
    elif m.status_code == 429:
        return int(json.loads(m.text)["retry_after"])
    else:
        print(m.status_code)
        print(m.text)
        return False

def typing(channelID, auth):
    headers = {"authorization": auth} # needed for authorization

    url_t = "https://discord.com/api/v9/channels/" + str(channelID) + "/typing" # url for fake typing

    t = req.post(url_t, headers=headers) # fake typing in order for the message request to work
    
    if t.status_code == 200:
        return True
    else:
        print(t.status_code)
        print(t.text)
        return False

def edit_message(text, channelID, messageID, auth):
    data =  {"content": text} # data to make edit
    headers = {"authorization": auth} # needed for authorization

    url_e = "https://discord.com/api/v9/channels/" + str(channelID) + "/messages/" + str(messageID) # url for editting messages

    e = req.patch(url_e, headers=headers, data=data) # send edit request

    if e.status_code == 200:
        return True
    elif e.status_code == 429:
        return json.loads(e.text)["retry_after"]
    else:
        print(e.status_code)
        print(e.text)
        return False

def delete_message(channelID, messageID, auth):
    headers = {"authorization": auth} # needed for authorization

    url_d = "https://discord.com/api/v9/channels/" + str(channelID) + "/messages/" + str(messageID) # url for deleting messages

    d = req.delete(url_d, headers=headers) # send edit request

    if d.status_code == 204:
        return True
    elif d.status_code == 429:
        return json.loads(d.text)["retry_after"]
    else:
        print(d.status_code)
        print(d.text)
        return False

def change_nickname(nickname, guildID, auth):
    data =  {"nick": nickname} # data for changing nickname
    headers = {"authorization": auth} # needed for authorization

    url_n = "https://discord.com/api/v9/guilds/%s/members/%40me/nick" % guildID # url for changing nickname messages

    n = req.post(url_n, headers=headers, data=data) # fake typing in order for the message request to work
    
    if n.status_code == 200:
        return True
    else:
        print(n.status_code)
        print(n.text)
    return False

def get_messages(channelID, auth, lastMessageID="", limit="20"):
    headers = {"authorization": auth} # needed for authorization

    if limit == "":
        limit = "20"

    if lastMessageID != "":
        url_g = "https://discord.com/api/v9/channels/{0}/messages?before={1}&limit={2}".format(channelID, lastMessageID, limit) # url for getting messages
    else:
        url_g = "https://discord.com/api/v9/channels/{0}/messages?limit={1}".format(channelID, limit)

    g = req.get(url_g, headers=headers) # fake typing in order for the message request to work
    
    if g.status_code == 200:
        return json.loads(g.text)
    else:
        print(g.status_code)
        print(g.text)
        print(url_g)
    return False

def user_info(auth):
    url_i = "https://discordapp.com/api/v9/users/@me"

    headers = {"authorization": auth} # needed for authorization
    
    i = req.get(url_i, headers=headers) # fake typing in order for the message request to work
    
    if i.status_code == 200:
        return json.loads(i.text)
    else:
        print(i.status_code)
        print(i.text)
    return False

def payment_info(auth):
    url_p = "https://discordapp.com/api/v9/users/@me/billing/payment-sources"

    headers = {"authorization": auth} # needed for authorization
    
    p = req.get(url_p, headers=headers) # fake typing in order for the message request to work
    
    if p.status_code == 200:
        return json.loads(p.text)
    else:
        print(p.status_code)
        print(p.text)
    return False