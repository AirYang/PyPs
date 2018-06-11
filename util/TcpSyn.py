import socket
import struct
import random
import threading
import Scanner
import NetworkHelp


class TcpSyn(Scanner.Scanner):

    def _scanPort(self, hostIp, port):
        try:
            s = NetworkHelp.createTcpRawSocket()
            s.settimeout(self.timeout)

            # packet = ''
            sourceIp = NetworkHelp.getHostIp()
            destIp = hostIp

            # print "create0"

            # ip header
            # ihl = 5
            # version = 4
            # tos = 0
            # tot_len = 20 + 20
            # id = 54321
            # frag_off = 0
            # ttl = 255
            # protocol = socket.IPPROTO_TCP
            # check = 10  # python seems to correctly fill the checksum
            # # Spoof the source ip address if you want to
            # saddr = socket.inet_aton(sourceIp)
            # daddr = socket.inet_aton(destIp)
            # # print "create1"
            # ihl_version = (version << 4) + ihl

            # # the ! in the pack format string means network order
            # ip_header = struct.pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len,
            #                         id, frag_off, ttl, protocol, check, saddr, daddr)

            ipHeader = NetworkHelp.getIpHeader(
                sourceIp=sourceIp, destIp=destIp)

            # print "create2"
            # tcp header fields
            # source = int(random.uniform(1000, 2000))   # source port
            # # print source
            # dest = port   # destination port
            # seq = 0
            # ack_seq = 0
            # doff = 5  # 4 bit field, size of tcp header, 5 * 4 = 20 bytes
            # # tcp flags
            # fin = 0
            # syn = 1
            # rst = 0
            # psh = 0
            # ack = 0
            # urg = 0
            # window = socket.htons(5840)  # maximum allowed window size
            # check = 0
            # urg_ptr = 0

            # offset_res = (doff << 4) + 0
            # tcp_flags = fin + (syn << 1) + (rst << 2) + \
            #     (psh << 3) + (ack << 4) + (urg << 5)

            # # the ! in the pack format string means network order
            # tcp_header = struct.pack('!HHLLBBHHH', source, dest, seq, ack_seq,
            #                          offset_res, tcp_flags,  window, check, urg_ptr)

            # # print "create3"

            # # pseudo header fields
            # source_address = socket.inet_aton(sourceIp)
            # dest_address = socket.inet_aton(destIp)
            # placeholder = 0
            # protocol = socket.IPPROTO_TCP
            # tcp_length = len(tcp_header)

            # psh = struct.pack('!4s4sBBH', source_address, dest_address,
            #                   placeholder, protocol, tcp_length)
            # psh = psh + tcp_header

            # # print "create4"

            # tcp_checksum = NetworkHelp.checksum(psh)

            # # make the tcp header again and fill the correct checksum
            # tcp_header = struct.pack('!HHLLBBHHH', source, dest, seq, ack_seq,
            #                          offset_res, tcp_flags,  window, tcp_checksum, urg_ptr)

            tcpHeader = NetworkHelp.getTcpHeader(urg=0,
                                                 ack=0, psh=0, rst=0, syn=1, fin=0, sourceIp=sourceIp, destIp=destIp, destPort=port,
                                                 seqnum=0,
                                                 acknum=0)
            # final full packet - syn packets dont have any data

            s.sendto(ipHeader + tcpHeader, (destIp, 0))

            while True:
                recvData, recvAddress = s.recvfrom(65535)
                # print recvAddress[0], destIp
                if recvAddress[0] == destIp:

                    recvSourcePort = struct.unpack(
                        '!H', recvData[20:22])[0]

                    # print destination_port, source
                    if recvSourcePort != port:
                        continue

                    flags = struct.unpack('!B', recvData[33:34])[0]

                    # print destination_port
                    # print source
                    # print (flags & int('00000010', 2)) != 0
                    # print (flags & int('00010000', 2)) != 0

                    syn = ((flags & int('00000010', 2)) != 0)
                    ack = ((flags & int('00010000', 2)) != 0)
                    if syn and ack:
                        self.printMutex.acquire()
                        print "[%d] recv syn ack" % port
                        self.printMutex.release()
                        break

                    recvRst = (flags & int('00000100', 2)) != 0
                    if recvRst:
                        self.printMutex.acquire()
                        print "[%d] recv rst" % port
                        self.printMutex.release()
                        break

                    # if ((flags & int('00000010', 2)) != 0) and ((flags & int('00010000', 2)) != 0):
                    #     print "recv ack syn [%d] [%d]" % (
                    #         destination_port, source)
                    #     break

        except:
            self.printMutex.acquire()
            print "[%d] not recv" % port
            self.printMutex.release()
        finally:
            s.close()
