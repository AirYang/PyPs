import threading


class Scanner(object):
    def __init__(self, works=4, timeout=0.5):
        self.works = works
        self.timeout = timeout
        self.printMutex = threading.Lock()

    def scanSingleHost(self, hostIp, ports=None):
        if ports is None:
            ports = [x for x in range(1, 65536)]

        print "--- Tcp Connect Scanning %s ---" % hostIp
        threads = []
        chunkSize = len(ports) // self.works
        for i in range(0, self.works):
            beginIndex = i * chunkSize
            endIndex = (i+1)*chunkSize if (i+1) != self.works else len(ports)
            t = threading.Thread(target=self._scanSingleHostDo, args=(
                hostIp, ports[beginIndex:endIndex]))
            threads.append(t)
            t.start()
        for th in threads:
            th.join()
        print "--- Tcp Connect Scanning End ---"

    def _scanSingleHostDo(self, hostIp, ports=None):
        for port in ports:
            self._scanPort(hostIp, port)

    def _scanPort(self, hostIp, port):
        pass
