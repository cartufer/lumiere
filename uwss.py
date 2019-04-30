import network, socket, ussl, time, wss_helper, sys, os, struct
# import sys
# import os
# import struct
# this project contains code modified from https://github.com/micropython/webrepl
class wss:
    # you need to pass this a newly established socket, before sendings any data to it
    # you can then deal with the object returned by this class
    def __init__(self, s):
        self._s = s
        self.s = ussl.wrap_socket(s) # , server_side=False, keyfile=None, certfile=None, cert_reqs=ussl.CERT_NONE, ca_certs=None)
        wss_helper.client_handshake(self.s)
        self.buf = b""

    def write(self, data):
        l = len(data)
        if l < 126:
            # TODO: hardcoded "binary" type
            hdr = struct.pack(">BB", 0x82, l)
        else:
            hdr = struct.pack(">BBH", 0x82, 126, l)
        self.s.write(hdr)
        self.s.write(data)

    def recvexactly(self, sz):
        res = b""
        while sz:
            data = self.s.read(sz)
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
                print("Got unexpected websocket record of type %x, skipping it" % fl)
                while sz:
                    skip = self.s.read(sz)
                    print("Skip data: {}" % skip)
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
