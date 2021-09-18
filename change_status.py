import requests as rq
import os
import time
import json

authPath = os.getcwd() + r"\auth.txt"
f = open(authPath,"r")
authorization = f.read()
animated_text = "May the 4th be with you"
f.close()

def change_status(text, auth):
    url1 = "https://discord.com/api/v9/users/@me/settings"
    url2 = "https://discord.com/api/v9/science"

    data =  json.dumps({
        "custom_status": {"text": text}
    })

    headers = {
        "authorization": auth,
        "content-type": "application/json",
        "content-length": str(len(data))
    }

    r1 = rq.patch(url=url1, headers=headers, data=data)
    print(r1.status_code)

    headers = {
        "authorization": auth,
        "content-type": "application/json",
        "content-length": str(len(data))
    }

    data =  json.dumps({
        "token": "NzIyNzgxOTE3NTQ3NTkzNzY5.6DlFH8jgfMDmR6d9_4pM3z_hQEA",
        "events": [{
            "type": "custom_status_updated",
            "properties": {
                "client_track_timestamp": time.time(),
                "emoji_type": None,
                "text_len": len(text),
                "clear_after": None,
                "location_section": "Account Panel",
                "location_object": "Avatar",
                "accessibility_support_enabled": False,
                "accessibility_features": 128,
                "client_send_timestamp": time.time() + 20
            }
        }]
    })

    r2 = rq.post(url=url2, headers=headers, data=data)
    print(r2.status_code)

def animate_text(text,blankspace="⠀",total_length=12):
    textList = []
    placeholder = "" # this much fills the entire status bar
    for i in range(total_length):
        placeholder = placeholder + blankspace
    print(len(placeholder))
    newText = ""

    for count in range(1, len(text) + 1):
        if count > len(placeholder):
            textComingOut = text[(len(placeholder) - count) * - 1:count]
        else:
            textComingOut = text[0:count]
        newText = placeholder[0:len(placeholder) - len(textComingOut)] + textComingOut
        textList.append(newText)

        if count == len(text): # last index
            lastText = ""

            for count2 in range(1, len(newText) + 1):
                spacesInTheEnd = ""
                
                for _ in range(count2):
                    spacesInTheEnd = spacesInTheEnd + blankspace
                lastText = newText[count2:] + spacesInTheEnd
                textList.append(lastText)
    return textList

def keep_animating(text, auth):
    while True:
        textList = animate_text(text, blankspace="\u2800", total_length=12)
        print(textList)
        for status_text in textList:
            change_status(status_text, auth)

keep_animating(animated_text, authorization)