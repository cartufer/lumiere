import network, usocket, datetime, time, os


NETWORK_SETTINGS = 'settings.dat'
EMOTE_SETTINGS = 'emotes.txt'
max_buff = 1024
nick = ""
password = ""
server = "irc-ws.chat.twitch.tv:80"
chan = ""

def main(nick, password, chan):
    # self.nick = nick
    # self.password = password
    # self.channel = channel
    print("reading settings")
    try:
            read_settings()
        except OSError:
            write_settings()

    print("attempting connection")
    sock_connect()
    run_loop()





def sock_connect():
    sockaddr = usocket.getaddrinfo(server, 80)[0][-1]
    sock.connect(sockaddr)

def run_loop():
    reading = socket.recv(max_buff)

			if ("PING" == reading[0:4]):
				s.send(line.replace("PING", "PONG"))
				break

def read_settings():
    # try:
    with open(NETWORK_SETTINGS) as f:
    # except IOError:
        # return false
    # else:
        # with f:
            # print f.readlines()
    # with open(NETWORK_SETTINGS) as f:
        line = f.readlines()
        nick, password, chan = line.strip("\n").split(";")
        return true


def write_settings():

        # do something to make settings, or reset
        # os.remove("ChangedFile.csv")

    with open(NETWORK_SETTINGS , "w") as f:
        f.write("%s;%s\n" % (nick, password))
