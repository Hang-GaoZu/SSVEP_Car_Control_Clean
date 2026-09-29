"""
Time    : 2025/5/2 10:39
Author  : mrtang
Email   : 810899799@qq.com
"""

import xlrd

def readconfig(path="./expconfig.xls"):
    try:
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        scr = {}
        scr["width"] = int(sheet.cell_value(2, 0))
        scr["height"] = int(sheet.cell_value(2, 1))
        scr["fps"] = int(sheet.cell_value(2, 2))
        if int(sheet.cell_value(2, 3)):
            scr["type"] = "fullscreen"
        else:
            scr["type"] = "normal"
        cms = []
        peri = []
        layout = []
        for i in range(6):
            lay = {}
            lay["id"] = i
            lay["cmd"] = sheet.cell_value(6 + i, 1)
            lay["pos"] = (float(sheet.cell_value(6 + i, 3)), float(sheet.cell_value(6 + i, 4)))
            lay["size"] = (float(sheet.cell_value(6 + i, 5)), float(sheet.cell_value(6 + i, 6)))
            lay["freq"] = float(sheet.cell_value(6 + i, 7))
            layout.append(lay)
            t = float(sheet.cell_value(6 + i, 2))
            cms.append(lay["cmd"])
            peri.append(t)
        ctr = {}
        ctr["flashTime"] = float(sheet.cell_value(14, 1))
        ctr["commands"] = cms
        ctr["period"] = peri
        ctr["pauseTime"] = 1
        return (0, {"scr": scr, "layout": layout, "ctr": ctr})
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return (1, None)