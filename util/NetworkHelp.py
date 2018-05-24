import socket
import struct
import random


def getHostIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def checksum(msg):
    s = 0
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = (ord(msg[i]) << 8) + (ord(msg[i+1]))
        s = s + w

    s = (s >> 16) + (s & 0xffff)
    # s = s + (s >> 16);
    # complement and mask to 4 byte short
    s = ~s & 0xffff

    return s


def createTcpSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


def createUdpSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    return sock


def createUdpRawSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    return sock


def createTcpRawSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    return sock


def createIcmpRawSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    return sock


def getIpHeader(sourceIp, destIp):
    ipVersion = 4
    ipHLength = 5
    ipService = 0x00
    ipTotalLength = 40
    ipId = int(random.uniform(10000, 40000))
    ipFlags = 0  # int('010', 2)
    ipFragOff = 0
    ipTtl = int(random.uniform(40, 128))
    ipProtocol = socket.IPPROTO_TCP
    ipCheckSum = 0  # system will fill
    ipSourceIp = socket.inet_aton(sourceIp)
    ipDestIp = socket.inet_aton(destIp)
    # ipPayload = ''

    # print "test2"

    ipHeader = struct.pack(
        '!BBHHHBBH4s4s', (ipVersion << 4) + ipHLength, ipService, ipTotalLength, ipId,  (ipFlags << 13) + ipFragOff, ipTtl, ipProtocol, ipCheckSum, ipSourceIp, ipDestIp)
    return ipHeader


def getTcpHeader(urg, ack, psh, rst, syn, fin, sourceIp, destIp, destPort, seqnum, acknum):
    tcpSourcePort = int(random.uniform(10000, 60000))
    tcpDestPort = destPort
    tcpSeqNum = seqnum
    tcpAckNum = acknum
    tcpDataOff = 5
    tcpUrg = urg
    tcpAck = ack
    tcpPsh = psh
    tcpRst = rst
    tcpSyn = syn
    tcpFin = fin
    tcpWinSize = 1024
    tcpCheckSum = 0
    tcpUrgPtr = 0

    ipSourceIp = socket.inet_aton(sourceIp)
    ipDestIp = socket.inet_aton(destIp)

    tcpDataOffAndRes = (tcpDataOff << 4) + 0
    tcpFlags = tcpFin+(tcpUrg << 5) + (tcpAck << 4) + \
        (tcpPsh << 3) + (tcpRst << 2) + (tcpSyn << 1)

    tcpHeader = struct.pack(
        "!HHLLBBHHH", tcpSourcePort, tcpDestPort, tcpSeqNum, tcpAckNum, tcpDataOffAndRes, tcpFlags, tcpWinSize, tcpCheckSum, tcpUrgPtr)

    tcpPreHeader = struct.pack(
        "!4s4sBBH", ipSourceIp, ipDestIp, 0, socket.IPPROTO_TCP, len(tcpHeader))

    # print "test6"
    tcpCheckSum = checksum(tcpPreHeader + tcpHeader)

    # print "test5"
    tcpHeader = struct.pack(
        "!HHLLBBHHH", tcpSourcePort, tcpDestPort, tcpSeqNum, tcpAckNum, tcpDataOffAndRes, tcpFlags, tcpWinSize, tcpCheckSum, tcpUrgPtr)
    return tcpHeader
