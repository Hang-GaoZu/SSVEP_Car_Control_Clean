
class ProtocolV4:
    def __init__(self):
        self.package = b""
        self.buffer = b""
        self.sratelst = [250, 500, 1000, 2000]
        self.bytesPerSample = [3, 4]
        self.packlen = 0
        self.ccc = 0

    def headVerify(self, buf):
        self.buffer = buf
        return len(self.buffer) >= 2 and self.buffer[1] == 0x55

    def getEpochAndVerify(self):
        identifier = self.buffer[2]
        if not identifier >> 7:
            self.packlen = self.buffer[3]
            self.package = self.buffer[:self.packlen]
            if len(self.package) == self.packlen:
                return (True, (sum(self.package[:-1]) & 255) == self.package[-1])
            return (False, None)
        return (False, None)

    def parsePak(self):
        identifier = self.buffer[2]
        data = {}
        data["device"] = identifier >> 6 & 1
        data["srate"] = self.sratelst[identifier >> 4 & 3]
        data["batlevel"] = identifier & 15
        data["payload"] = self.package[4:-2]
        data["test"] = self.package[-2:-1]
        return data