#!/usr/bin/env python

import sys

from util.Ping import Ping
from util.TcpConnect import TcpConnect
from util.TcpSyn import TcpSyn
from util.UdpScan import UdpScan
from util.TcpFin import TcpFin
from util.TcpNull import TcpNull
from util.TcpXmas import TcpXmas
from util.TcpAck import TcpAck
from util.TcpMaimon import TcpMaimon

if __name__ == '__main__':

    if len(sys.argv) != 5:
        print "./PortScanner.py TypeNumber DestIp MinPort MaxPort"
        print "type number include: "
        print "              1 ping ip"
        print "              2 tcp connect scan ip from min port to max port"
        print "              3 tcp syn scan ip from min port to max port"
        print "              4 udp scan ip from min port to max port"
        print "              5 tcp fin scan ip from min port to max port"
        print "              6 tcp null scan ip from min port to max port"
        print "              7 tcp xmas scan ip from min port to max port"
        print "              8 tcp ack scan ip from min port to max port"
        print "              9 tcp maimon scan ip from min port to max port"
        exit()

    typeNumber = int(sys.argv[1])
    destIp = sys.argv[2]
    minPort = int(sys.argv[3])
    maxPort = int(sys.argv[4])
    # print minPort, maxPort

    if typeNumber == 1:
        # test www.baidu.com 220.181.112.244 good
        # test noj.cn 192.168.0.242 bad
        print "--- Icmp Ping ---"
        pinger = Ping()
        pinger.verbose_ping(destIp)

    elif typeNumber == 2:
        # test www.baidu.com 220.181.112.244 (80 443 open begin)
        # test noj.cn 192.168.0.242 (80 3389 open)
        tcpConnect = TcpConnect(
            desc="--- Tcp Connect %s ---", works=4, timeout=0.5)
        tcpConnect.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    elif typeNumber == 3:
        # test www.baidu.com 220.181.112.244 (80 443 open)
        # test noj.cn 192.168.0.242 (80 3389 open)
        # test www.taobao.com 58.205.221.214 (80 443 open)
        tcpSyn = TcpSyn(desc="--- Tcp Syn %s ---", works=4, timeout=0.5)
        tcpSyn.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    elif typeNumber == 4:
        # test Xi'an 117.34.105.104 (445 448 450 not recv)
        # test noj.cn 192.168.0.242 (all not recv)
        # test www.baidu.com 220.181.112.244 (all not recv)
        udpScan = UdpScan(desc="--- Udp Scan %s ---", works=1, timeout=1.0)
        udpScan.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    elif typeNumber == 5:
        # test noj.cn 192.168.0.242 (80 3389 recv ack rst)
        # test Xi'an 117.34.105.104 (not recv all)
        # test www.nwpu.edu.cn 202.117.94.248 (recv ack rst all)
        tcpFin = TcpFin(desc="--- Tcp Fin %s ---", works=4, timeout=0.5)
        tcpFin.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    elif typeNumber == 6:
        # test noj.cn 192.168.0.242 (80 3389 recv ack rst)
        # test www.nwpu.edu.cn 202.117.94.248 (recv ack rst all)
        # test github.com 13.250.177.223 (not recv all)
        # test www.taobao.com 58.205.221.214 (not recv all)
        tcpNull = TcpNull(desc="--- Tcp Null %s ---", works=4, timeout=0.5)
        tcpNull.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    elif typeNumber == 7:
        # test noj.cn 192.168.0.242 (80 3389 recv ack rst)
        # test www.nwpu.edu.cn 202.117.94.248 (recv ack rst all)
        # test BeiJing 123.206.91.84 (not recv all)
        tcpXmas = TcpXmas(desc="--- Tcp Xmas %s ---", works=4, timeout=0.5)
        tcpXmas.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    elif typeNumber == 8:
        # test noj.cn 192.168.0.242 (80 3389 recv rst with win 0)
        # test www.nwpu.edu.cn 202.117.94.248 (recv all)
        # test  www.runoob.com 125.76.247.179 (not recv all)
        tcpAck = TcpAck(desc="--- Tcp Ack Win %s ---", works=4, timeout=0.5)
        tcpAck.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    elif typeNumber == 9:
        # test noj.cn 192.168.0.242 (80 3389 recv rst)
        # test www.nwpu.edu.cn 202.117.94.248 (recv all)
        tcpMaimon = TcpMaimon(
            desc="--- Tcp Maimon %s ---", works=4, timeout=0.5)
        tcpMaimon.scanSingleHost(
            destIp, [x for x in range(minPort, maxPort+1)])

    else:
        print "not include this type number\n"
        exit()
