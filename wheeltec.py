"""
Time    : 2025/5/25 16:04
Author  : mrtang
Email   : 810899799@qq.com
"""

import serial
import serial.tools.list_ports as lp

import time
import threading

class WheelTec:
    def __init__(self):
        self.ser = None

    def getallserial(self):
        """返回所有可用的串口列表（不做芯片筛选）"""
        ports = lp.comports()
        device = []
        for p in ports:
            device.append(p.device)   # 直接加入所有串口
        return device

    def initSer(self, com):
        # 先安全关闭旧连接
        try:
            if self.ser is not None:
                self.ser.close()
        except:
            pass
        # 尝试打开新串口
        try:
            self.ser = serial.Serial(port=com, baudrate=9600, timeout=0.1)
            print(f"串口 {com} 打开成功")
            return True
        except Exception as e:
            print(f"串口打开失败: {e}")
            self.ser = None
            return False

    def sendCmd(self, cmd):
        print("  [WheelTec.sendCmd] 准备发送")
        print(f"    命令: {cmd}")
        print(f"    类型: {type(cmd)}")
        print(f"    串口对象: {self.ser}")
        
        try:
            if self.ser is not None and self.ser.is_open:
                print("    串口状态: 已打开")
                data = cmd.encode('ascii') if isinstance(cmd, str) else cmd
                print(f"    编码后数据: {data}")
                
                bytes_written = self.ser.write(data)
                print(f"    ✅ 成功写入 {bytes_written} 字节")
                
                self.ser.flush()
                print("    缓冲区已刷新")
            else:
                if self.ser is None:
                    print("    ❌ 错误: 串口对象为 None")
                else:
                    print(f"    ❌ 错误: 串口未打开 (is_open={self.ser.is_open})")
        except Exception as e:
            print(f"    ❌ 串口发送失败: {e}")
            import traceback
            traceback.print_exc()

    def testfun(self):
        if self.ser is not None:
            self.ser.write(b"6")
            time.sleep(0.4)
        self.ser.close()

    def test(self):
        thread = threading.Thread(target=self.testfun)
        thread.start()

    def close(self):
        try:
            if self.ser is not None and self.ser.is_open:
                self.ser.close()
        except:
            pass