# SSVEP 脑电控制小车（SSVEP_Car_Control_Clean）

基于 SSVEP（稳态视觉诱发电位）的脑电控制小车项目，包含两个独立应用：

| 应用 | 源码位置 | 入口脚本 | 作用 |
| --- | --- | --- | --- |
| **EEGViewer**（上位机 / 解码端） | `decoder/` | `python -m decoder.EEGViewer` | 通过串口(460800)读取脑电设备数据，SSVEP 解码识别目标频率，将结果通过本地 UDP 发出 |
| **controlCenter**（控制中心 / 刺激与控制端） | 根目录 + `guienginemp/` | `python main.py` | 呈现 SSVEP 刺激界面，监听本地 UDP(127.0.0.1:8093) 接收解码结果，通过串口(9600)控制小车 |

> 两个应用均为**纯本地程序**：脑电设备串口 460800、小车串口 9600、本地 UDP 127.0.0.1:8093，无云授权或联网逻辑。

---

## 目录结构

```
SSVEP_Car_Control_Clean/
├── main.py                 # controlCenter 入口（PyQt5 主窗口）
├── controlcenterUI.py      # controlCenter 主窗口 UI（由 Qt Designer 生成）
├── stimulimanager.py       # SSVEP 刺激管理器（StiManager）
├── wheelmanager.py         # 小车控制管理器（WheelManager，串口 9600）
├── wheeltec.py             # 小车串口通信底层封装（WheelTec）
├── readconfig.py           # 读取 expconfig.xls 实验参数
├── mycombox.py             # 自定义下拉框控件
├── mymessbox.py            # 消息弹窗封装
├── expconfig.xls           # 实验参数配置（刺激频率、串口等）
├── requirements.txt        # Python 依赖清单
│
├── decoder/                # EEGViewer 上位机（解码端）
│   ├── EEGViewer.py        # EEGViewer 入口（PyQt5 主窗口）
│   ├── viewerui.py         # EEGViewer 主窗口 UI
│   ├── devmanager.py       # 设备管理（串口连接 460800）
│   ├── datadecodervep.py   # SSVEP 数据解码（DataDecoderVep）
│   ├── datamanager.py      # 数据管理（DataManager）
│   ├── eegdisplay.py       # 脑电波形显示（pyqtgraph）
│   ├── SSVEPmethod.py      # SSVEP 识别算法（CCA 典型相关分析）
│   ├── butterfilter.py     # 巴特沃斯 / FIR 滤波器
│   ├── protocol.py         # 设备通信协议（ProtocolV4）
│   ├── rda.py              # 串口数据接收封装（RDA）
│   ├── commonsetting.py    # 公共常量与设置
│   ├── readconfig.py       # 读取实验参数
│   ├── mymessbox.py        # 消息弹窗封装
│   └── __init__.py
│
└── guienginemp/            # Pygame 图形引擎（controlCenter 侧）
    ├── hguiengine.py       # 图形引擎主类（HGuiEngine，游戏循环）
    ├── baseobj.py          # 图形对象基类（BaseObj）
    ├── block.py            # 方块对象（Block）
    ├── sinblock.py         # 正弦波动画块（sinBlock）
    ├── getfps.py           # 帧率测量（FPS 计数器）
    └── __init__.py
```

## 运行方式

```bash
# 安装依赖（Python 3.9）
pip install -r requirements.txt

# 运行解码端 EEGViewer（需在 decoder 所在目录下，使用相对导入）
python -m decoder.EEGViewer

# 运行刺激与控制端 controlCenter
python main.py
```

> 提示：`decoder` 是包（含 `__init__.py`），EEGViewer 使用相对导入，必须在工程根目录下以 `python -m decoder.EEGViewer` 方式启动。

## 依赖清单（requirements.txt）

PyQt5、pygame、pyserial、xlrd、numpy、scipy、scikit-learn、screeninfo、pyqtgraph

## 精简说明

本工程由原始源码整理而来，已删除：

- `Result/` 整目录（历史整合版，与模块化工程重复）
- `CLAUDE.md`（开发备注）
- `decoder/final_test.py`（一次性抓包验证脚本）
- `decoder/expconfig.xls`（与根目录重复的实验配置，MD5 相同）

以及清理了无用的注释代码与未使用的 import。