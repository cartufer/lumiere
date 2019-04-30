# from __future__ import print_function
import sys,os,struct,network, uwss,usocket,time,json #,datetime

# try:
#     import usocket as socket
# except ImportError:
#     import socket
# try:
#     import ussl as ssl
# except ImportError:
#     import ssl
# try:
#     import utime as time
# except ImportError:
#     import time
# try:
#     import ujson as json
# except ImportError:
#     import json
# import websocket_helper
global debug
debug = True
# Define to 1 to use builtin "uwebsocket" module of MicroPython
# USE_BUILTIN_UWEBSOCKET = False
# import network, usocket, ussl, datetime, utime, os, json
# def debugmsg(msg):
#     if debug:
#         print(msg)
# if USE_BUILTIN_UWEBSOCKET:
#     from uwebsocket import websocket
# else:
# class websocket:
#
#     def __init__(self, s):
#         self.s = s
#         self.buf = b""
#
#     def write(self, data):
#         l = len(data)
#         if l < 126:
#             # TODO: hardcoded "binary" type
#             hdr = struct.pack(">BB", 0x82, l)
#         else:
#             hdr = struct.pack(">BBH", 0x82, 126, l)
#         self.s.send(hdr)
#         self.s.send(data)
#
#     def recvexactly(self, sz):
#         res = b""
#         while sz:
#             data = self.s.recv(sz)
#             if not data:
#                 break
#             res += data
#             sz -= len(data)
#         return res
#
#     def read(self, size, text_ok=False):
#         if not self.buf:
#             while True:
#                 hdr = self.recvexactly(2)
#                 assert len(hdr) == 2
#                 fl, sz = struct.unpack(">BB", hdr)
#                 if sz == 126:
#                     hdr = self.recvexactly(2)
#                     assert len(hdr) == 2
#                     (sz,) = struct.unpack(">H", hdr)
#                 if fl == 0x82:
#                     break
#                 if text_ok and fl == 0x81:
#                     break
#                 debugmsg("Got unexpected websocket record of type %x, skipping it" % fl)
#                 while sz:
#                     skip = self.s.recv(sz)
#                     debugmsg("Skip data: {}" % skip)
#                     sz -= len(skip)
#             data = self.recvexactly(sz)
#             assert len(data) == sz
#             self.buf = data
#
#         d = self.buf[:size]
#         self.buf = self.buf[size:]
#         assert len(d) == size, len(d)
#         return d
#
#     def ioctl(self, req, val):
#         assert req == 9 and val == 2

# try not to put things before the class, they won't be brought into your code when you reference the class
#
#
# self.NETWORK_SETTINGS = 'settings.dat'
# EMOTE_SETTINGS = 'emotes.txt'
# max_buff = 1024
# nick = ""
# password = ""
# chan = ""
# chat_server = "irc-ws.chat.twitch.tv:80" # update to wss, cartufer
# wss = None
class lumiere_bot:
    login_file = 'settings.json'
    emote_file = 'emotes.json' # write a handler for this file, cartufer
    max_buff = 1024
    # self.issetup = False
    # nick = ""
    # password = ""
    # chan = ""
    global debug
    if debug:
        serveraddr = "echo.websocket.org" # update to wss, cartufer
        wss = True
    else:
        serveraddr = "not yet" # update to wss, cartufer
        wss = True
    # wss_server = "irc-ws.chat.twitch.tv"
    # wss = None
    sockaddr = None
    wait_time = 1600 # minimum time between messages in milliseconds, any less than a thousand and it's likely to just kick you
    # the tightest time limit is 20 messages in 30 seconds, i set it 0.1 seconds over that
    def __init__(self, n = None, p = None, c = None, onmessage = None, onclose = None, wss_ssl = True):
        # you can pass in the credentials through init and it'll just pass it to setup
        # setup won't attempt to read from the .dat if setup is already done
        # it won't attempt to connect until you tell it so, and then it'll run_loop
        #
        # self.nick = None
        # self.password = None
        # self.chan = None
        # self.wss = wss_ssl
        # self.issetup = False
        print("attempting setup, {}".format(self))
        print(self)
        self.setup(n,p,c,onmessage, onclose, wss_ssl)
        # try:
        # self.read_settings()
            # except OSError:
                # write_settings()

        # print("attempting connection")
        # sock_connect()
        # run_loop()

    def dummy(self, dontcare = None):
        pass # this is the dummy function for the callbacks, so it has a default value

    def wait(self):
        n = time.ticks_diff(ticks1, ticks2) # this function ensures we won't send messages too fast
        if n >= 0 and n < self.wait_time: # make sure you wait atleast a second
            time.sleep_ms(self.wait_time - n) # this math is probably bad, longer is better
        self.lastmessage = time.ticks_ms()

    def post(self, message): # this does not yet support PRIVMSG to indivdual users and probably won't, poke me and i'll make it
        self.wait()
        m = "PRIVMSG #" + self.chan + " :" + message + "\r\n"
        print("< {}".format(m))
        # if self.wss:
        self.wss_sock.write(m)
        # else:
            # self.sock.send(m)

    def rawpost(self, message): # this does not yet support PRIVMSG to indivdual users and probably won't, poke me and i'll make it
        self.wait()
        # m = "PRIVMSG #" + self.chan + " :" + message + "\r\n"
        print("< {}".format(message))
        # if self.wss:
        self.wss_sock.write(message)
        # else:
            # self.sock.send(m)

    def callbacks(self, onmessage, onclose, onrunloop): # you can use this function to configure callbacks if you setup credentials in a .dat
        self.onmessage = onmessage
        self.onclose = onclose
        self.onrunloop = onrunloop
        print('callbacks setup, {}'.format(self))

    def setup(self, n = None, p = None, c = None, onmessage = None, onclose = None, wss_ssl = True):
        if n and p and c:
            self.nick = n
            self.password = p
            self.chan = c
            # self.wss = wss_ssl # if you are using this with a wifi device, please use wss/ssl, you'll thank me
            self.issetup = True
            # self.onmessage = onmessage
            # self.onclose = onclose
            if(onmessage != None):
                self.onmessage = onmessage
            else:
                self.onmessage = self.dummy
            if(onclose != None):
                self.onclose = onclose
            else:
                self.onclose = self.dummy
            if(wss_ssl != None):
                self.wss = wss_ssl
        else:
            try:
                self.issetup = self.read_settings()
                # if(onmessage != None):
                #     self.onmessage = onmessage
                # if(onclose != None):
                #     self.onclose = onclose
                # if(wss_ssl != None):
                #     self.wss_ssl = wss_ssl
            except OSError:
                print('error getting settings, {}'.format(self))
                write_settings()


    def connect(self, n = False, p = False, c = False):
        if n and p and c:
            self.nick = n
            self.password = p
            self.chan = c
            self.wss = True # if you are using this with a wifi device, please use wss/ssl, you'll thank me
            self.issetup = True
            self.onmessage = self.dummy # if you have to you can even setup callbacks after you connect, not recommended
            self.onclose = self.dummy
        print('attempting connect, {}'.format(self))
        self.lastmessage = time.ticks_ms()
        if self.issetup == False:
            print('not setup, aborting connect, {}'.format(self))
            return False
        # if self.wss:
        self.sockaddr = usocket.getaddrinfo(self.serveraddr, 443)[0][-1]
        # else:
            # self.sockaddr = usocket.getaddrinfo(serveraddr, 80)[0][-1]
        # sockaddr = usocket.getaddrinfo(server, 80)[0][-1]
        self.sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) # , proto=usocket.IPPROTO_TCP
        self.sock.connect(self.sockaddr)
        # if self.wss:
        self.wss_sock = uwss.wss(self.sock) # ussl.wrap_socket(self.sock, server_side=False, keyfile=None, certfile=None, cert_reqs=CERT_NONE, ca_certs=None)
        # return False
        time.sleep(5)
        print("< {}".format("PASS"))
        self.wss_sock.write("PASS " + self.password + "\r\n")
        print("< {}".format("NICK"))
    	self.wss_sock.write("NICK " + self.nick.lower() + "\r\n")
        time.sleep(5)
        self.rawpost("CAP REQ :twitch.tv/tags twitch.tv/commands")
        s.send("JOIN #" + self.channel + "\r\n")

        # do some conection stuff here, cartufer


        self.rawpost("CAP REQ :twitch.tv/membership")
        self.rawpost("CAP REQ :twitch.tv/tags")
        self.rawpost("CAP REQ :twitch.tv/commands")
        # self.post("CAP REQ :twitch.tv/tags twitch.tv/commands")
        eroor = run_loop() # this will return an error on failure, misspelled on purpose
        print(eroor)


        # put in an increasing delay before a new reconnect

    def run_loop(self): # this function is where the magic happens, it is where most of the program happens
        running = True
        while running:
            try:
                # if self.wss:
                reading = self.wss_sock.read(self.max_buff, True)
                # read_list = splitlines(reading)
                # for lines in read_list
                # else:
                    # reading = self.sock.recv(self.max_buff)
                # reading = usocket.recv(max_buff)
                print("> {}".format(reading))
            	if ("PING" == reading[0:4]):
                    self.wait()
                    reading.replace("PING", "PONG")
                    print("< {}".format(reading))
                    # if self.wss:
                    self.wss_sock.write(reading)
                    # else:
                        # self.sock.send(reading)
                else:
                    self.onmessage(reading)
                self.onrunloop()
            except OSError as err:
                print("error found while in run_loop, {}, {}".format(self, err))
                self.onclose(err)
                return err






    def read_settings(self):
        try:
            with open(self.login_file) as f:
                data = json.load(f)
                self.nick = data['nick']
                self.password = data['password']
                self.chan = data['chan']
                # line = f.readlines()
                # self.nick, self.password, self.chan = line.strip("\n").split(";")
                self.issetup = True
                return True
        except OSError as err:
            self.write_settings()
        try:
            with open(self.emote_file) as f:
                line = f.readlines()
                # self.nick, self.password, self.chan = line.strip("\n").split(";")
                # self.issetup = True
                return True
        except OSError as err:
            pass
        return False
        # else:
            # with f:
                # print f.readlines()
        # with open(self.NETWORK_SETTINGS) as f:
            # line = f.readlines()
            # nick, password, chan = line.strip("\n").split(";")
            # return True


    def write_settings(self): # this should be get_settings maybe?, cartufer
        self.issetup = False
        print('there is not yet a way to configure user settings, follow instructions on github page') # todo, cartufer
            # do something to make settings, or reset
            # os.remove("ChangedFile.csv")

        # with open(self.NETWORK_SETTINGS , "w") as f:
        #     f.write("{};{}\n" % (nick, password))
        return False
