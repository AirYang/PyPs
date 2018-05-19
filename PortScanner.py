#!/usr/bin/env python

import sys
from util.Ping import Ping
from util.TcpConnect import TcpConnect
# from util.TcpFin import TcpFin

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "./PortScanner.py DestIp"
        exit()

    pinger = Ping()
    if not pinger.verbose_ping(sys.argv[1]):
        print "Ping %s Failed!" % sys.argv[1]
        exit()

    tcpConnect = TcpConnect()
    tcpConnect.scanSingleHost(sys.argv[1], [x for x in range(70, 90)])

    # tcpFin = TcpFin(works=1)
    # tcpFin.scanSingleHost(sys.argv[1], [x for x in range(70, 90)])
