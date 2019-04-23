from __future__ import print_function
import sys,os,struct,network, ussl, datetime, time, json

try:
    import usocket as socket
except ImportError:
    import socket
import websocket_helper

DEBUG = True
# Define to 1 to use builtin "uwebsocket" module of MicroPython
USE_BUILTIN_UWEBSOCKET = False
# import network, usocket, ussl, datetime, utime, os, json
def debugmsg(msg):
    if DEBUG:
        print(msg)
if USE_BUILTIN_UWEBSOCKET:
    from uwebsocket import websocket
else:
    class websocket:

        def __init__(self, s):
            self.s = s
            self.buf = b""

        def write(self, data):
            l = len(data)
            if l < 126:
                # TODO: hardcoded "binary" type
                hdr = struct.pack(">BB", 0x82, l)
            else:
                hdr = struct.pack(">BBH", 0x82, 126, l)
            self.s.send(hdr)
            self.s.send(data)

        def recvexactly(self, sz):
            res = b""
            while sz:
                data = self.s.recv(sz)
                if not data:
                    break
                res += data
                sz -= len(data)
            return res

        def read(self, size, text_ok=False):
            if not self.buf:
                while True:
                    hdr = self.recvexactly(2)
                    assert len(hdr) == 2
                    fl, sz = struct.unpack(">BB", hdr)
                    if sz == 126:
                        hdr = self.recvexactly(2)
                        assert len(hdr) == 2
                        (sz,) = struct.unpack(">H", hdr)
                    if fl == 0x82:
                        break
                    if text_ok and fl == 0x81:
                        break
                    debugmsg("Got unexpected websocket record of type %x, skipping it" % fl)
                    while sz:
                        skip = self.s.recv(sz)
                        debugmsg("Skip data: %s" % skip)
                        sz -= len(skip)
                data = self.recvexactly(sz)
                assert len(data) == sz
                self.buf = data

            d = self.buf[:size]
            self.buf = self.buf[size:]
            assert len(d) == size, len(d)
            return d

        def ioctl(self, req, val):
            assert req == 9 and val == 2

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
    NETWORK_SETTINGS = 'settings.json'
    EMOTE_SETTINGS = 'emotes.json' # write a handler for this file, cartufer
    max_buff = 1024
    # setup = False
    # nick = ""
    # password = ""
    # chan = ""
    serveraddr = "irc-ws.chat.twitch.tv" # update to wss, cartufer
    # wss_server = "irc-ws.chat.twitch.tv"
    # wss = None
    sockaddr = None
    wait_time = 1600 # minimum time between messages in milliseconds, any less than a thousand and it's likely to just kick you
    #the tightest time limit is 20 messages in 30 seconds, i set it 0.1 seconds over that
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
        m = "PRIVMSG #" + self.chan + " :" + message + "\r\n"
        print("< %s".format(reading))
        if self.wss:
            self.wss_sock.write(m)
        else:
            self.sock.send(m)

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
        # self.post("CAP REQ :twitch.tv/membership")
        # self.post("CAP REQ :twitch.tv/tags")
        # self.post("CAP REQ :twitch.tv/commands")
        # self.post("CAP REQ :twitch.tv/tags twitch.tv/commands")
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
                print("> %s".format(reading))
            	if ("PING" == reading[0:4]):
                    self.wait()
                    reading.replace("PING", "PONG")
                    print("< %s".format(reading))
                    if self.wss:
                        self.wss_sock.write(reading)
                    else:
                        self.sock.send(reading)
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
