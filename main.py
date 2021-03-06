import wifimgr, network
from bot import lumiere_bot
global debug
debug = True

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False) # this forces shutdown of setup interface, i think, cartufer
# this file is going to be a sample implementation of bot.py
# below are several related functions that users may find helpful

def message_handler(message): # this will be the whole unmodified privmsg
    pass

def close_handler(error): # was it one thing or 2?, cartufer
    pass

def runloopcallback(): # this will be a place to put things to run inside of the bot's run loop
    pass

lumi = lumiere_bot()
lumi.callbacks(message_handler, close_handler, runloopcallback)

def is_sub_emote(word): # this function will eventually be able to evaluate if something is camelcase
    if word[0] == word[0].lower() and word != word.lower(): # maybe this could be a bool lambda?
        return True
    else:
        return False
lumi.issetup = True
lumi.connect()
