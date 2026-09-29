import threading
import serial
from .datadecodervep import DataDecoderVep
import serial.tools.list_ports as lp
import re
import time

class RDA(threading.Thread):
    def __init__(self, pysig, queDev2Plot, setting):
        super().__init__()
        self.ser = None
        self.pysig = pysig
        self.running = True
        self.dec = DataDecoderVep(protocolVersion="v4", que2plot=queDev2Plot, expconfig=setting)
        self.daemon = True
        self.start()

    def getallserial(self):
        pp1 = re.compile("CP210x")
        pp2 = re.compile("CH340")
        ports = lp.comports()
        device = []
        for p in ports:
            id = p.device
            r1 = re.search(pp1, str(p))
            if r1 is not None:
                device.append(id + "-CP210x")
            r2 = re.search(pp2, str(p))
            if r2 is not None:
                device.append(id + "-CH340")
        return device

    def getportfromstring(self, portstring):
        return portstring.split("-")[0]

    def configDev(self, port="COM3", baudrate=460_800):
        self.port = port
        self.baudrate = baudrate

    def startAcq(self):
        if self.ser is not None:
            try:
                self.ser.close()
            except:
                pass
            self.ser = None

        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=0.1)
            print(f"串口 {self.port} 打开成功")
            return True
        except Exception as e:
            print(f"串口打开失败: {e}")
            self.ser = None
            return False

    def stopAcq(self):
        try:
            if self.ser is not None:
                self.ser.close()
        except:
            pass
        self.ser = None

    def close(self):
        self.running = False

    def run(self):
        print(f"[RDA] 线程启动，当前 ser 对象: {self.ser}")
        clk = time.time()
        while self.running:
            if self.ser is None:
                time.sleep(0.2)
                clk = time.time()
                continue

            try:
                if time.time() - clk >= 0.05:
                    buf = self.ser.read(self.ser.inWaiting())
                    if len(buf) > 0:
                        print(f"[RDA] 收到 {len(buf)} 字节: {buf[:20].hex()}")
                        self.dec.parseData(buf)
                    clk = time.time()
            except Exception as e:
                print(f"串口读取错误: {e}")
                self.ser = None
                self.pysig.emit("接收器断开!")

            time.sleep(max(0, 0.05 - (time.time() - clk)))