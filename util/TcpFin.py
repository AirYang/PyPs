import socket
import struct
import random
import threading
import Scanner
import NetworkHelp


class TcpFin(Scanner.Scanner):

    def _scanPort(self, hostIp, port):

        try:
            s = NetworkHelp.createTcpRawSocket()
            s.settimeout(self.timeout)

            # print "test0"

            # packet = ''
            sourceIp = NetworkHelp.getHostIp()
            destIp = hostIp

            # print "test1"

            # ip header
            ipVersion = 4
            ipHLength = 5
            ipService = 0x00
            ipTotalLength = 40
            ipId = 63326
            ipFlags = int('010', 2)
            ipFragOff = 0
            ipTtl = 64
            ipProtocol = socket.IPPROTO_TCP
            ipCheckSum = 0
            ipSourceIp = socket.inet_aton(sourceIp)
            ipDestIp = socket.inet_aton(destIp)
            # ipPayload = ''

            # print "test2"

            ipHeader = struct.pack(
                '!BBHHHBBH4s4s', (ipVersion << 4) + ipHLength, ipService, ipTotalLength, ipId,  (ipFlags << 13) + ipFragOff, ipTtl, ipProtocol, ipCheckSum, ipSourceIp, ipDestIp)

            # print "test3"

            # tcp header
            tcpSourcePort = int(random.uniform(10000, 60000))
            tcpDestPort = port
            tcpSeqNum = 512
            tcpAckNum = 0
            tcpDataOff = 5
            tcpUrg = 0
            tcpAck = 0
            tcpPsh = 0
            tcpRst = 0
            tcpSyn = 0
            tcpFin = 1
            tcpWinSize = 53270
            tcpCheckSum = 0
            tcpUrgPtr = 0

            tcpDataOffAndRes = (tcpDataOff << 4) + 0
            tcpFlags = tcpFin+(tcpUrg << 5) + (tcpAck << 4) + \
                (tcpPsh << 3) + (tcpRst << 2) + (tcpSyn << 1)

            tcpHeader = struct.pack(
                "!HHLLBBHHH", tcpSourcePort, tcpDestPort, tcpSeqNum, tcpAckNum, tcpDataOffAndRes, tcpFlags, tcpWinSize, tcpCheckSum, tcpUrgPtr)

            tcpPreHeader = struct.pack(
                "!4s4sBBH", ipSourceIp, ipDestIp, 0, socket.IPPROTO_TCP, len(tcpHeader))

            # print "test6"
            tcpCheckSum = NetworkHelp.checksum(tcpPreHeader + tcpHeader)

            # print "test5"
            tcpHeader = struct.pack(
                "!HHLLBBHHH", tcpSourcePort, tcpDestPort, tcpSeqNum, tcpAckNum, tcpDataOffAndRes, tcpFlags, tcpWinSize, tcpCheckSum, tcpUrgPtr)

            # print "test4"
            s.sendto(ipHeader + tcpHeader, (destIp, 0))

            # print "sendto"
            # pass

            while True:
                recvData, recvAddr = s.recvfrom(65535)
                # print recvAddr, destIp

                if recvAddr[0] == destIp:
                    recvSourcePort = struct.unpack(
                        '!H', recvData[20:22])[0]

                    recvFlags = struct.unpack('!B', recvData[33:34])[0]
                    # print recvFlags
                    # recvRst = (recvFlags & int('00000100', 2)) != 0
                    # port and rst acks
                    if (recvSourcePort == tcpDestPort) and (recvFlags == 20):
                        self.printMutex.acquire()
                        print "[%d] recv ack rst" % port
                        self.printMutex.release()
                        # print "ip port"
                        break
                    # print recvSourcePort
                    # break

        except:
            self.printMutex.acquire()
            print "[%d] not recv ack rst" % port
            self.printMutex.release()
        finally:
            # pass
            s.close()
