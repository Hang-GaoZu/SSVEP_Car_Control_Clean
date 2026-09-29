import numpy as np
from .protocol import ProtocolV4
from queue import Queue
from .commonsetting import EEGTYPE
import threading

devconfig = {"vref": 4.5, "bits": 24, "gain": [24] * 128}

PORT = 8093

class DataDecoderVep(threading.Thread):
    def __init__(self, protocolVersion="v4", que2plot=Queue(), expconfig=None):
        if expconfig is None:
            expconfig = {"freqs": [6.2, 7.2, 8.2, 9.2, 10.2, 11.2], "flashTime": 3}
        super(DataDecoderVep, self).__init__()
        self.expconfig = expconfig
        self.daemon = True
        self.srate = None
        self.chs = None
        self.que2vepdetector = Queue()

        if protocolVersion == "v4":
            self.protocol = ProtocolV4()
        else:
            self.protocol = None

        self.decoders = [Ads1299Decoder(), None]
        self.que2plot = que2plot

        self.devdata = None

        self.buffer = b""
        self.sampleCount = 0
        self.payloads = b""
        self.test = b""

        self.start()

    def parseData(self, buffer, *args):
        if isinstance(buffer, str):
            buffer = buffer.encode('latin-1')
        self.buffer += buffer

        # 真实帧头（来自 Wireshark 抓包）
        HEADER_6CH = b'\xab\x55\x06\x18'
        HEADER_8CH = b'\xab\x55\x07\x18'

        while True:
            pos6 = self.buffer.find(HEADER_6CH)
            pos8 = self.buffer.find(HEADER_8CH)
            pos = -1
            channels = 6
            if pos6 != -1 and (pos8 == -1 or pos6 < pos8):
                pos = pos6
                channels = 6
            elif pos8 != -1:
                pos = pos8
                channels = 8

            if pos == -1:
                self.buffer = self.buffer[-3:]
                break

            self.buffer = self.buffer[pos:]
            bytes_per_frame = 4 + channels * 4
            if len(self.buffer) < bytes_per_frame:
                break

            pkt_data = self.buffer[4:4 + channels * 4]
            if channels == 8:
                pkt_data = pkt_data[:24]
                channels = 6

            self.buffer = self.buffer[bytes_per_frame:]

            devData = {
                "device": 0,
                "srate": 250,
                "batlevel": 8,
                "payload": pkt_data,
                "test": b'\x00'
            }
            self.collectAll(devData)

        if self.sampleCount > 0:
            self.dataarange()

    def collectAll(self, dat, *args):
        self.payloads += dat["payload"]
        self.test += dat["test"]
        self.sampleCount += 1
        self.devdata = dat

    def dataarange(self):
        outputdata = {}
        outputdata["dataay"] = self.decoders[self.devdata["device"]].decode(
            self.payloads, self.sampleCount
        )
        outputdata["srate"] = self.devdata["srate"]
        self.srate = self.devdata["srate"]
        self.chs, _ = outputdata["dataay"].shape
        outputdata["batlevel"] = self.devdata["batlevel"]
        self.sampleCount = 0
        self.payloads = b""
        self.test = b""
        self.que2plot.put(outputdata)
        self.que2vepdetector.put(outputdata["dataay"])

    def run(self):
        pass

class Ads1299Decoder:
    def __init__(self, config=devconfig):
        self.rawdt = np.dtype("int32")
        self.rawdt = self.rawdt.newbyteorder(">")
        vref = config["vref"]
        bits = config["bits"]
        gain = config["gain"]
        self.facs = np.array([self._calFac(vref, bits, g) for g in gain])
        self.facs = self.facs[np.newaxis, :]

    def _calFac(self, vref, bits, gain):
        return vref / (gain * (2**bits - 1)) * 1000000.0

    def _tobuf32(self, buf24):
        if buf24[0] > 127:
            return b'\xff' + buf24[:3]
        return b'\x00' + buf24[:3]

    def decode(self, payloads, sampleN):
        chs = int(len(payloads) / 3 / sampleN)
        tmbuf = [self._tobuf32(payloads[i:i+3]) for i in range(0, len(payloads), 3)]
        buf = b"".join(tmbuf)
        eeg = np.frombuffer(buf, dtype=self.rawdt).astype(EEGTYPE).reshape(sampleN, chs)
        fac = np.repeat(self.facs[:, :chs], sampleN, axis=0)
        eeg = eeg * fac
        return eeg.transpose()