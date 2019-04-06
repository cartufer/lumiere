import network, usocket, ussl, datetime, utime, os, json

# try not to put things before the class, they won't be brought into your code when you reference the class
# 
# 
# NETWORK_SETTINGS = 'settings.dat'
# EMOTE_SETTINGS = 'emotes.txt'
# max_buff = 1024
# nick = ""
# password = ""
# chan = ""
# chat_server = "irc-ws.chat.twitch.tv:80" # update to wss, cartufer
# wss = None
class lumiere_bot
    NETWORK_SETTINGS = 'settings.dat'
    EMOTE_SETTINGS = 'emotes.txt' # write a handler for this file, cartufer
    max_buff = 1024
    # setup = False
    # nick = ""
    # password = ""
    # chan = ""
    serveraddr = "irc-ws.chat.twitch.tv" # update to wss, cartufer
    # wss_server = "irc-ws.chat.twitch.tv"
    # wss = None
    sockaddr = None
    wait_time = 1000 # minimum time between messages in milliseconds, any less than a thousand and it's likely to just kick you
    def __init__(self, n = None, p = None, c = None, onmessage = None, onclose = None, wss_ssl = True):
        # you can pass in the credentials through init and it'll just pass it to setup
        # setup won't attempt to read from the .dat if setup is already done
        # it won't attempt to connect until you tell it so, and then it'll run_loop
        # 
        # self.nick = None
        # self.password = None
        # self.chan = None
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

    def dummy(self, dontcare):
        pass # this is the dummy function for the callbacks, so it has a default value

    def wait():
        n = utime.ticks_diff(ticks1, ticks2) # this function ensures we won't send messages too fast
        if n >= 0 and n < self.wait_time: # make sure you wait atleast a second
            utime.sleep_ms(self.wait_time - n) # this math is probably bad, longer is better
        self.lastmessage = utime.ticks_ms()

    def post(self, message): # this does not yet support PRIVMSG to indivdual users and probably won't, poke me and i'll make it
        self.wait()
        if self.wss:
            self.wss_sock.write("PRIVMSG #" + self.chan + " :" + message + "\r\n")
        else:
            self.sock.send("PRIVMSG #" + self.chan + " :" + message + "\r\n")

    def callbacks(self, onmessage, onclose): # you can use this function to configure callbacks if you setup credentials in a .dat
        self.onmessage = onmessage
        self.onclose = onclose
        print('callbacks setup, %s'.format(self))

    def setup(self, n = None, p = None, c = None, onmessage = self.dummy, onclose = self.dummy, wss_ssl = True):
        if n and p and c:
            self.nick = n
            self.password = p
            self.chan = c
            self.wss = wss_ssl # is you are using this with a wifi device, please use wss/ssl, you'll thank me
            self.setup = True
            self.onmessage = onmessage
            self.onclose = onclose
        else:
            try:
                self.setup = read_settings()
                self.wss = wss_ssl
                self.onmessage = onmessage
                self.onclose = onclose
            except OSError:
                print('error getting settings, %s'.format(self))
                write_settings()


    def connect(self, n, p, c):
        if n and p and c:
            self.nick = n
            self.password = p
            self.chan = c
            self.wss = True # if you are using this with a wifi device, please use wss/ssl, you'll thank me
            self.setup = True
            self.onmessage = self.dummy # if you have to you can even setup callbacks after you connect, not recommended
            self.onclose = self.dummy
        print('attempting connect, %s'.format(self)
        self.lastmessage = utime.ticks_ms()
        if !setup:
            print('not setup, aborting connect, %s'.format(self))
            return False
        if self.wss:
            self.sockaddr = usocket.getaddrinfo(serveraddr, 443)[0][-1]
        else:
            self.sockaddr = usocket.getaddrinfo(serveraddr, 80)[0][-1]
        # sockaddr = usocket.getaddrinfo(server, 80)[0][-1]
        self.sock = usocket.socket(af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP)
        self.sock.connect(sockaddr)
        if self.wss:
            self.wss_sock = ussl.wrap_socket(self.sock, server_side=False, keyfile=None, certfile=None, cert_reqs=CERT_NONE, ca_certs=None)
        # return False
        # do some conection stuff here, cartufer
        run_loop()

    def run_loop(): # this function is where the magic happens, it is where most of the program happens
        RUNNING = True
        while RUNNING:
            try:
                if self.wss:
                    reading = self.wss_sock.read(self.max_buff)
                else:
                    reading = self.sock.recv(self.max_buff)
                # reading = socket.recv(max_buff)
                print(reading)
            	if ("PING" == reading[0:4]):
                    self.wait()
                    if self.wss:
                        self.wss_sock.write(reading.replace("PING", "PONG"))
                    else:
                        self.sock.send(reading.replace("PING", "PONG"))
                else:
                    self.onmessage(reading)
            except (IOError, OSError) as err:
                print("error found while in run_loop, %s, %s".format(self, err))
                onclose(err)
                return err





    def read_settings():
        try:
            with open(NETWORK_SETTINGS) as f:
                line = f.readlines()
                self.nick, self.password, self.chan = line.strip("\n").split(";")
                self.setup = True
                return True
        except IOError:
            write_settings()
        return False
        # else:
            # with f:
                # print f.readlines()
        # with open(NETWORK_SETTINGS) as f:
            # line = f.readlines()
            # nick, password, chan = line.strip("\n").split(";")
            # return True


    def write_settings():
        self.setup = False
        print('there is not yet a way to configure user settings, follow instructions on github page') # todo, cartufer
            # do something to make settings, or reset
            # os.remove("ChangedFile.csv")

        # with open(NETWORK_SETTINGS , "w") as f:
        #     f.write("%s;%s\n" % (nick, password))
        return False
