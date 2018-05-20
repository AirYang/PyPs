#!/usr/bin/env python

import sys
from util.Ping import Ping
from util.TcpConnect import TcpConnect
from util.TcpSyn import TcpSyn
from util.UdpScan import UdpScan
from util.TcpFin import TcpFin

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "./PortScanner.py DestIp"
        exit()

    # pinger = Ping()
    # if not pinger.verbose_ping(sys.argv[1]):
    #     print "Ping %s Failed!" % sys.argv[1]
    #     exit()

    # tcpConnect = TcpConnect()
    # tcpConnect.scanSingleHost(sys.argv[1], [x for x in range(80, 84)])

    # test github.com and with no ping
    # tcpSyn = TcpSyn(works=4, timeout=0.5)
    # tcpSyn.scanSingleHost(sys.argv[1], [x for x in range(80, 91)])

    # test 117.34.105.104
    # udpScan = UdpScan(works=1, timeout=2.0)
    # udpScan.scanSingleHost(sys.argv[1], [x for x in range(80, 84)])

    # test 192.168.0.242
    # test 221.231.138.56
    # test 202.117.94.248 can test
    tcpFin = TcpFin(works=1, timeout=1)
    tcpFin.scanSingleHost(sys.argv[1], [x for x in range(80, 84)])
