from discord_hacks import *
import time

def animate_text(text, blankspace="⠀", total_length=5, cover=""):
    textList = []
    placeholder = "" # this much fills the entire status bar

    for _ in range(total_length):
        placeholder += blankspace
    newText = ""

    for count in range(1, len(text) + 1):
        if count > len(placeholder):
            textComingOut = text[(len(placeholder) - count) * - 1:count]
        else:
            textComingOut = text[0:count]
        newText = placeholder[0:len(placeholder) - len(textComingOut)] + textComingOut
        textList.append(cover+newText+cover)

        if count == len(text): # last index
            lastText = ""

            for count2 in range(1, len(newText) + 1):
                spacesInTheEnd = ""
                
                for _ in range(count2):
                    spacesInTheEnd = spacesInTheEnd + blankspace
                lastText = newText[count2:] + spacesInTheEnd
                textList.append(cover+lastText+cover)
    return textList

def scroll_text(message, channelID, authorization, blankspace="\u2800",total_length=5,cover="", reverse=False):
    messageID = send_message(message, channelID, authorization) # send message and get ID
    nothingGoneWrong = True # no errors returned by discord while the loop is running

    if type(messageID) is str:
        print("Message was successfully sent! Editing message.")
        textList = animate_text(message, blankspace=blankspace, total_length=total_length, cover=cover)

        if reverse:
            textList.reverse()

        while nothingGoneWrong:
            for text in textList:
                successful = edit_message(text, channelID, messageID, authorization)# if this is less than 1 second, discord will make a
                time.sleep(1) # cooldown to prevent spam (but on top of that, we're sending requests which delay our program anyway)
                
                if not successful: 
                    nothingGoneWrong = False
                    print("Message has disappeared.")
                    break
                elif not isinstance(successful, (bool)):
                    print(f"Waiting %s for cooldown" % str(int(successful) + 1)) # 1 seconds more to be extra sure cooldown is over
                    time.sleep(int(successful) + 1)
    else:
        print("Message failed to send.")

# if you want blankspace, use \u2800
# f = open("auth.txt", "r")
# scroll_text("🐟", "694167091053330552", f.read(), total_length=6, blankspace="🌊", reverse=False)
# f.close()