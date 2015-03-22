#The MIT License (MIT)
#
#Copyright (c) 2015 Robert Anthony Bouterse, WD8RDE
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
import time
import usb.core
import usb.util
import math
from g59_si570 import Si570Utils

FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump(src, length=8):
    N=0; result=''
    while src:
       s,src = src[:length],src[length:]
       hexa = ' '.join(["%02X"%ord(str(x)) for x in s])
       s = s.translate(FILTER)
       result += "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
       N+=length
    return result

class g59_cmd:

    def __init__(self):
        self.usb_connect()

    def usb_connect(self):
        # find our device
        self.dev = usb.core.find(idVendor=0xfffe, idProduct=0x1970)

        # was it found?
        if self.dev is None:
            raise ValueError('Device not found')

        self.interface = 0
        if self.dev.is_kernel_driver_active(self.interface):
            self.dev.detach_kernel_driver(self.interface)

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.dev.set_configuration()

        # get an endpoint instance
        self.cfg = self.dev.get_active_configuration()
        self.intf = self.cfg[(0,0)]

        self.ep_out = usb.util.find_descriptor(
            self.intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        assert self.ep_out is not None

        self.ep_in = usb.util.find_descriptor(
            self.intf,
            # match the first IN endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

        assert self.ep_in is not None

    def usb_disconnect(self):
        if self.dev.is_kernel_driver_active(self.interface):
            self.dev.detach_kernel_driver(self.interface)

    def __send_cmd(self, cmd, param):
        cmd_array = self.__str2array(cmd)
        cmd_packet = self.__pack_cmd(cmd_array)
        packet = self.__pack_request(cmd_packet, param)
        print dump(packet)
        self.ep_out.write(packet)

    def __pack_request(self,cmd,args):
        packet=[]
        for i in range(0,64):
            packet.append(0x00)

        i = 0
        for byte in cmd:
            packet[i] = byte
            i += 1

        if args is not None:
            i = 8
            for byte in args:
                packet[i] = byte
                i += 1

        return ''.join([chr(c) for c in packet])

    def __pack_cmd(self, cmd):
        packet=[]
        for i in range(8):
            packet.append(0x20)

        i=0
        for byte in cmd:
            packet[i] = byte
            i += 1
            if i > 7:
                break
        return packet

    def __str2array(self, strng):
        arry = []
        for c in strng:
            arry.append(ord(c))
        return arry

    def att_on(self):
        self.__send_cmd("ATT_ON",None)
        return

    def att_off(self):
        self.__send_cmd("ATT_OFF",None)
        return

    def set_name(self, name):
        return

    def set_freq(self, freq):
        si570 = Si570Utils(verbose=4)
        registers = si570.setFreq(freq)
        cmd = 'SET_FREQ'
        cmd_array = self.__str2array(cmd)
        cmd_packet = self.__pack_cmd(cmd_array)

        freq_str = str(int(freq * 1000000))
        freq_str = '00000000' + freq_str
        freq_str = freq_str[-8:]
        freq_array = self.__str2array(freq_str)

        param = []
        for i in range(56):
            param.append(0x00)

        for i in range(8):
            param[i] = freq_array[i]

        param[10] = 0xaa # i2c address

        param[12] = registers[0] #0xe7
        param[13] = registers[1] #0x42
        param[14] = registers[2] #0xb2
        param[15] = registers[3] #0x8b
        param[16] = registers[4] #0x24
        param[17] = registers[5] #0xe0

        packet = self.__pack_request(cmd_packet, param)
        print dump(packet)
        self.ep_out.write(packet)
        return

    def set_filt(self,fltr):
        param = []
        for i in range(56):
            param.append(0x00)
        param[12] = fltr
        self.__send_cmd("SET_FILT", param)
        return

    def k_speed(self):
        return

    def af_on(self):
        self.__send_cmd("AF_ON",None)
        return

    def af_off(self):
        self.__send_cmd("AF_OFF",None)
        return

    def mute_on(self):
        self.__send_cmd("MUTE_ON",None)
        return

    def mute_off(self):
        self.__send_cmd("MUTE_OFF",None)
        return

    def trv_on(self):
        self.__send_cmd("TRV_ON",None)
        return

    def trv_off(self):
        self.__send_cmd("TRV_OFF",None)
        return

    def rf_on(self):
        self.__send_cmd("RF_ON",None)
        return

    def rf_off(self):
        self.__send_cmd("RF_OFF",None)
        return

    def tx_on(self):
        self.__send_cmd("TX_ON",None)
        return

    def tx_off(self):
        self.__send_cmd("TX_OFF",None)
        return

    def k_mode(self):
        return

    def k_ratio(self):
        return

    def pa10_on(self):
        return

    def auto_cor(self):
        return

    def sec_rx2(self):
        return

    def monitor(self):
        return




