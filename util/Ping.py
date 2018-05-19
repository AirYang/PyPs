import os
import sys
import struct
import select
import socket
import time


class Ping(object):
    'ping ip address'

    def __init__(self):
        self.default_timer_ = time.clock if sys.platform == 'win32' else time.time
        self.ICMP_ECHO_REQUEST = 8

    def _checksum(self, source_string):
        sum = 0
        countTo = (len(source_string)/2)*2
        count = 0
        while count < countTo:
            thisVal = ord(source_string[count + 1]) * \
                256 + ord(source_string[count])
            sum = sum + thisVal
            sum = sum & 0xffffffff  # Necessary?
            count = count + 2

        if countTo < len(source_string):
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff  # Necessary?

        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff

        # Swap bytes. Bugger me if I know why.
        answer = answer >> 8 | (answer << 8 & 0xff00)

        return answer

    def _receive_one_ping(self, my_socket, ID, timeout):
        timeLeft = timeout
        while True:
            startedSelect = self.default_timer_()
            whatReady = select.select([my_socket], [], [], timeLeft)
            howLongInSelect = (self.default_timer_() - startedSelect)
            if whatReady[0] == []:  # Timeout
                return

            timeReceived = self.default_timer_()
            recPacket, addr = my_socket.recvfrom(1024)
            icmpHeader = recPacket[20:28]
            type, code, checksum, packetID, sequence = struct.unpack(
                "bbHHh", icmpHeader
            )
            # Filters out the echo request itself.
            # This can be tested by pinging 127.0.0.1
            # You'll see your own request
            if type != 8 and packetID == ID:
                bytesInDouble = struct.calcsize("d")
                timeSent = struct.unpack(
                    "d", recPacket[28:28 + bytesInDouble])[0]
                return timeReceived - timeSent

            timeLeft = timeLeft - howLongInSelect
            if timeLeft <= 0:
                return

    def _send_one_ping(self, my_socket, dest_addr, ID):

        dest_addr = socket.gethostbyname(dest_addr)

        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        my_checksum = 0

        # Make a dummy heder with a 0 checksum.
        header = struct.pack(
            "bbHHh", self.ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        bytesInDouble = struct.calcsize("d")
        data = (192 - bytesInDouble) * "Q"
        data = struct.pack("d", self.default_timer_()) + data

        # Calculate the checksum on the data and the dummy header.
        my_checksum = self._checksum(header + data)

        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy.
        header = struct.pack(
            "bbHHh", self.ICMP_ECHO_REQUEST, 0, socket.htons(
                my_checksum), ID, 1
        )
        packet = header + data
        my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1

    def _do_one(self, dest_addr, timeout):
        icmp = socket.getprotobyname("icmp")
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error, (errno, msg):
            if errno == 1:
                # Operation not permitted
                msg = msg + (
                    " - Note that ICMP messages can only be sent from processes"
                    " running as root."
                )
                raise socket.error(msg)
            raise  # raise the original error

        my_ID = os.getpid() & 0xFFFF

        self._send_one_ping(my_socket, dest_addr, my_ID)
        delay = self._receive_one_ping(my_socket, my_ID, timeout)

        my_socket.close()
        return delay

    def verbose_ping(self, dest_addr, timeout=2, count=4):
        successCount = 0
        for i in xrange(count):
            print "ping %s..." % dest_addr,
            try:
                delay = self._do_one(dest_addr, timeout)
            except socket.gaierror, e:
                print "[%d]:failed. (socket error: '%s')" % (i, e[1])
                break

            if delay == None:
                print "[%d]:failed. (timeout within %ssec.)" % (i, timeout)
            else:
                delay = delay * 1000
                successCount += 1
                print "[%d]:get ping in %0.4fms" % (i, delay)
        return (successCount >= (count/2))
