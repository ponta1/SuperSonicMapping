# -*- coding:utf-8 -*-

# SuperSonicMapping
#
# pyserialのインストール方法
#   pip install pyserial

import sys
import math
import tkinter
from tkinter import messagebox
import serial

import SuperSonicMapping_setting

COM_PORT = SuperSonicMapping_setting.COM_PORT

TIMER_MS = 10 # タイマーの間隔 0.01秒

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

serial_rcv = ""     # シリアルで受信したデータ

DATA_SIZE = 180     # バッファの最大サイズ
arVal = []          # 座標のバッファ

# タイマー処理
def timer():
    global TIMER_MS
    global ser
    global serial_rcv

    # シリアルの受信
    while ser.in_waiting > 0:
        rcv = ser.read(1)
        if rcv != b'\r' and rcv != b'\n':
            serial_rcv = serial_rcv + rcv.decode('utf-8')
        if rcv == b'\n':
            #print("RECV:" + serial_rcv)
            ar_rcv = serial_rcv.split(',')
            if len(ar_rcv) == 2:
                dir = int(ar_rcv[0])
                dist = int(ar_rcv[1])
                plot(dir, dist)
            serial_rcv = ""
            break

    # 次のタイマーをセット
    root.after(TIMER_MS, timer)

# 座標を算出してバッファに追加
def plot(dir, dist):
    global arVal
    global DATA_SIZE

    dir = dir + 90
    x = int(math.cos(dir / 180 * math.pi) * dist)
    y = int(-math.sin(dir / 180 * math.pi) * dist)
    #print(" x:" + str(x) + " y:" + str(y))

    # バッファがいっぱいになったら古いデータを削除
    if len(arVal) > DATA_SIZE:
        del arVal[0]
    arVal.append((x, y))

    draw(dir)

# 描画
def draw(dir):
    global arVal
    global canvas

    cx = SCREEN_WIDTH / 2
    cy = SCREEN_HEIGHT / 2

    canvas.delete("all")
    i = 0
    for (x, y) in arVal:
        color = "#00" + '{:02x}'.format(int(i / len(arVal) * 255)) + "00"
        canvas.create_oval(cx + x - 2, cy + y - 2, cx + x + 2, cy + y + 2, fill=color, outline=color)
        i = i + 1

    x = int(math.cos(dir / 180 * math.pi) * 1000)
    y = int(-math.sin(dir / 180 * math.pi) * 1000)
    canvas.create_line(cx, cy, cx + x, cy + y, fill = "green")
    canvas.pack()
    #print("DIR:" + str(dir))

# ======================
# メイン
# ======================
if __name__ == "__main__":

    # ウィンドウ初期化
    root = tkinter.Tk()
    root.title(u"SuperSonicMapping")

    root.geometry(str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT))   # ウインドウサイズを指定

    canvas = tkinter.Canvas(
        root,
        width = SCREEN_WIDTH,
        height = SCREEN_HEIGHT,
        bg = "black"
    )
    canvas.pack()

    # -------------------------------------

    try:
        ser = serial.Serial(COM_PORT, 115200)
    except IOError:
        print("COMポートが開けません:" + COM_PORT)
        messagebox.showinfo(u"エラー", u"COMポートが開けません:" + COM_PORT)
        sys.exit()

    # タイマー開始
    root.after(TIMER_MS, timer)

    root.mainloop()
