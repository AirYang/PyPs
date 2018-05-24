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

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "./PortScanner.py DestIp MinPort MaxPort"
        exit()

    minPort = int(sys.argv[2])
    maxPort = int(sys.argv[3])
    # print minPort, maxPort

    # pinger = Ping()
    # pinger.verbose_ping(sys.argv[1])

    # tcpConnect = TcpConnect(
    #     desc="--- Tcp Connect %s ---", works=4, timeout=0.5)
    # tcpConnect.scanSingleHost(
    #     sys.argv[1], [x for x in range(minPort, maxPort+1)])

    # # test github.com and with no ping
    # tcpSyn = TcpSyn(desc="--- Tcp Syn %s ---", works=4, timeout=0.5)
    # tcpSyn.scanSingleHost(sys.argv[1], [x for x in range(minPort, maxPort+1)])

    # test 117.34.105.104
    udpScan = UdpScan(desc="--- Udp Scan %s ---", works=1, timeout=1.0)
    udpScan.scanSingleHost(sys.argv[1], [x for x in range(minPort, maxPort+1)])

    # test 192.168.0.242
    # test 221.231.138.56
    # test 202.117.94.248 can test
    # tcpFin = TcpFin(desc="--- Tcp Fin %s ---", works=4, timeout=0.5)
    # tcpFin.scanSingleHost(sys.argv[1], [x for x in range(minPort, maxPort+1)])

    # tcpNull = TcpNull(desc="--- Tcp Null %s ---", works=4, timeout=0.5)
    # tcpNull.scanSingleHost(sys.argv[1], [x for x in range(minPort, maxPort+1)])

    # tcpXmas = TcpXmas(desc="--- Tcp Xmas %s ---", works=4, timeout=0.5)
    # tcpXmas.scanSingleHost(sys.argv[1], [x for x in range(minPort, maxPort+1)])

    # tcpAck = TcpAck(desc="--- Tcp Ack %s ---", works=4, timeout=0.5)
    # tcpAck.scanSingleHost(sys.argv[1], [x for x in range(minPort, maxPort+1)])
