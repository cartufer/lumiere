import wifimgr
from bot import *

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D


# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")
def message_handler():
    pass

def close_handler():
    pass

lumi = lumiere_bot()
lumi.callbacks(message_handler, close_handler)
