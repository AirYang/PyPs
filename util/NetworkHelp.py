import socket
import struct


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
    #s = s + (s >> 16);
    # complement and mask to 4 byte short
    s = ~s & 0xffff

    return s


def createTcpSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


# def createRawSocket():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#     return sock


def createTcpRawSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    return sock
