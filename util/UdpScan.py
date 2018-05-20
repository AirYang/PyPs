import socket
import struct
import threading
import Scanner
import NetworkHelp


class UdpScan(Scanner.Scanner):

    def _scanPort(self, hostIp, port):
        try:
            sUdp = NetworkHelp.createUdpSocket()
            sUdp.settimeout(self.timeout)

            # print "test0"

            sIcmp = NetworkHelp.createIcmpRawSocket()
            sIcmp.settimeout(self.timeout)

            # print "test1"

            message = 'hello'
            sUdp.sendto(message.encode('utf_8'), (hostIp, port))

            # print "test2"

            while True:
                icmpData, icmpAddr = sIcmp.recvfrom(65535)
                # print icmpAddr, hostIp
                # print len(icmpData)
                if icmpAddr[0] == hostIp:
                    # print "ip"
                    type = struct.unpack('!B', icmpData[20:21])[0]
                    code = struct.unpack('!B', icmpData[21:22])[0]
                    fromPort = struct.unpack('!H', icmpData[50:52])[0]
                    # print recvPort, port
                    if ((type == 3) or (code == 3)) and (fromPort == port):
                        break

            self.printMutex.acquire()
            print "[%d] close" % port
            self.printMutex.release()
        except:
            self.printMutex.acquire()
            print "[%d] open" % port
            self.printMutex.release()
        finally:
            sUdp.close()
            sIcmp.close()
