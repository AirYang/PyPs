import socket
import threading
import Scanner
import NetworkHelp


class TcpConnect(Scanner.Scanner):

    def _scanPort(self, hostIp, port):
        try:
            s = NetworkHelp.createTcpSocket()
            s.settimeout(self.timeout)
            s.connect((hostIp, port))
            self.printMutex.acquire()
            print "[%d] open" % port
            self.printMutex.release()
        except:
            self.printMutex.acquire()
            print "[%d] close" % port
            self.printMutex.release()
        finally:
            s.close()
