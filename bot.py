import network, usocket, ussl, datetime, time, os, json


# NETWORK_SETTINGS = 'settings.dat'
# EMOTE_SETTINGS = 'emotes.txt'
# max_buff = 1024
# nick = ""
# password = ""
# chan = ""
# chat_server = "irc-ws.chat.twitch.tv:80" // update to wss, cartufer
# wss = None
class lumiere_bot
    NETWORK_SETTINGS = 'settings.dat'
    EMOTE_SETTINGS = 'emotes.txt'
    max_buff = 1024
    # setup = False
    # nick = ""
    # password = ""
    # chan = ""
    serveraddr = "irc-ws.chat.twitch.tv" // update to wss, cartufer
    # wss_server = "irc-ws.chat.twitch.tv"
    # wss = None
    sockaddr = None
    def __init__(self, n = None, p = None, c = None, onmessage = None, onclose = None, wss_ssl = True):
        # self.nick = None
        # self.password = None
        # self.channel = None
        # self.wss = wss_ssl
        # self.setup = False
        print("attempting setup, %s".format(self))
        self.setup(n,p,c,onmessage, onclose, wss_ssl)
        # try:
        # read_settings()
            # except OSError:
                # write_settings()

        # print("attempting connection")
        # sock_connect()
        # run_loop()


    def post(self, message):
        if wss:
            pass
        else:
            pass

    def callbacks(self, onmessage, onclose):
        self.onmessage = onmessage
        self.onclose = onclose

    def setup(self, n = None, p = None, c = None, onmessage = None, onclose = None, wss_ssl = True):
        if n and p and c:
            self.nick = n
            self.password = p
            self.chan = c
            self.wss = wss_ssl
            self.setup = True
            self.onmessage = backcall
            self.onclose = onclose
        else:
            try:
                setup = read_settings()
                wss = wss_ssl
                self.onmessage = backcall
                self.onclose = onclose
            except OSError:
                print('error getting settings, %s'.format(self))
                write_settings()


    def connect(self, n, p, c):
        if !setup:
            print('not setup, %s'.format(self))
            return false
        if wss:
            self.sockaddr = usocket.getaddrinfo(serveraddr, 443)[0][-1]
        else:
            self.sockaddr = usocket.getaddrinfo(serveraddr, 80)[0][-1]
        # sockaddr = usocket.getaddrinfo(server, 80)[0][-1]
        self.sock = usocket.socket(af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP)
        self.sock.connect(sockaddr)
        if wss:
            self.wss_sock = ussl.wrap_socket(sock, server_side=False, keyfile=None, certfile=None, cert_reqs=CERT_NONE, ca_certs=None)
        # return False
        run_loop()

    def run_loop():
        try:
            if wss:
                reading = self.wss_sock.read(self.max_buff)
            else:
                reading = self.sock.recv(self.max_buff)
            # reading = socket.recv(max_buff)
            print(reading)
        	if ("PING" == reading[0:4]):
                if wss:
                    wss_sock.write(reading.replace("PING", "PONG"))
                else:
                    s.send(reading.replace("PING", "PONG"))
        		# s.send(line.replace("PING", "PONG"))
        		break

            self.onmessage(reading)
        except (IOError, OSError) as err:

                print("error found in run_loop, %s, %s".format(self, err))
            onclose(err)



    def read_settings():
        try:
            with open(NETWORK_SETTINGS) as f:
                line = f.readlines()
                nick, password, chan = line.strip("\n").split(";")
                return True
        except IOError:
            write_settings()
        # else:
            # with f:
                # print f.readlines()
        # with open(NETWORK_SETTINGS) as f:
            # line = f.readlines()
            # nick, password, chan = line.strip("\n").split(";")
            # return True
        return False


    def write_settings():
        print('there is not yet a way to configure user settings, follow instructions on github page') // todo, cartufer
            # do something to make settings, or reset
            # os.remove("ChangedFile.csv")

        # with open(NETWORK_SETTINGS , "w") as f:
        #     f.write("%s;%s\n" % (nick, password))
        return False
