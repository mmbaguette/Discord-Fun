import cv2
import requests
import json
from time import sleep

fAuth = open("auth.txt","r")
authorization = fAuth.read() # authorization token
channelID = "852295420116729878" # channel ID we're reading and sending messages to
fAuth.close()

def send_message(channelID, text, authorization, imageBytes=None):
    files = {
        "file": ("yourmom.png", imageBytes)
    }
    payload_json = {
        "content": text, 
        "tts": False
    }
    headers = {
        "authorization": authorization
    }

    request_link = f"https://discord.com/api/v9/channels/{str(channelID)}/messages"

    if "file" in files:
        #headers["content-type"] = "multipart/form-data"
        r = requests.post(url=request_link, data=payload_json, files=files,  headers=headers)
    else:
        r = requests.post(url=request_link, data=payload_json, headers=headers)
    
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        print("Message request failed:", str(r.status_code))
        print("Status message:", r.text)
        return False

def get_messages(channelID, authorization, limit=50):
    headers = {
        "authorization": authorization
    }
    request_link = f"https://discord.com/api/v9/channels/{str(channelID)}/messages?limit={str(limit)}"

    r = requests.get(url=request_link, headers=headers)

    if r.status_code == 200:
        return json.loads(r.text)
    elif r.status_code == 429:
        print(r.status_code)
        sleep(int(json.loads(r.text)["retry_after"]) + 0.5)
    else:
        print(r.status_code)
        print(r.text)
        return False

# found from StackOverflow "resize image without distortion opencv python"
# I use it all the time. favourite function
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def welcome_banner(username, new_banner):
    # add text
    welcomeText = cv2.putText(new_banner, "Welcome,", (150,120), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255,255), thickness=6)
    full_banner = cv2.putText(welcomeText, username, (280,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255,255), thickness=6)
    bytesString = cv2.imencode(".png", full_banner)[1].tobytes()
    return bytesString

united_banner = cv2.imread("united_banner.png", cv2.IMREAD_UNCHANGED)
united_height = 400
united_banner = image_resize(united_banner, height=united_height)

def main():
    while True:
        messageList = get_messages(channelID, authorization, limit=1)
        
        if messageList:
            message = messageList[0]

            if str(message["type"]) == "7":
                author = message["author"]
                username = author["username"] + "#" + str(author["discriminator"])
                user_id = author["id"]
                print(f"{username}", "joined the server!")

                join_message = f"Welcome, <@!{user_id}> to **UA | United Airlineѕ**! <:unitedglobe:853479122503073843>\n"
                join_message += "Make sure to join our Roblox group! \nhttps://www.roblox.com/groups/7769193/UA-United-Airline"

                banner = welcome_banner(username, united_banner)
                send_message(channelID, join_message, authorization, imageBytes=banner)
        else:
            print("Could not retrieve last message!")
        sleep(1)

if __name__ == '__main__':
    main()