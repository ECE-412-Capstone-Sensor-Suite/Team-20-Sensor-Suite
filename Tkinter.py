#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tkinter
from tkinter import *
import tkinter.messagebox
import read
import cv2

top = tkinter.Tk()
top2 = tkinter.Tk()
num=[]
TimesList=""
MotesList=""


##1.查看所有的数据 实时更新在第一个按钮， stop
def helloCallBack():
    mylb.delete(0,99999999)
    for item in read.test1():
        mylb.insert(END, item)
        scrolly.config(command=mylb.yview)
    mylb2.delete(0, 10)
    mylb2.insert(END, "Read all sensors file")
    scrolly.config(command=mylb2.yview)
## 2.input函数（地址） 然后跳出4个图表
def helloCallBack1():
    num.clear()
    num.append(2)
    mylb2.delete(0, 10)
    mylb2.insert(END, "Read mote1 file")
    scrolly.config(command=mylb2.yview)
 ##3.history所有的数据定一个时间（自定义时间）
def helloCallBack2():
    num.clear()
    num.append(3)
    mylb2.delete(0, 10)
    mylb2.insert(END, "Read mote2 file")
    scrolly.config(command=mylb2.yview)
 ##4.history固定的地址里的数据定一个时间（自定义时间）
def helloCallBack3():
    num.clear()
    num.append(4)
    lableTime.pack()
    TimeBox.pack()
    lableMotes.pack()
    MotesBox.pack()
    mylb2.delete(0, 10)
    mylb2.insert(END, "Input mac adress to check mote")
    scrolly.config(command=mylb2.yview)
def ThisOk():
    print(num)
    if num[0]==2:
        mylb.delete(0, 99999999)
        for item in read.test2(TimeBox.get()):
            mylb.insert(END, item)
            scrolly.config(command=mylb.yview)
    if num[0] == 3:
        mylb.delete(0, 99999999)
        for item in read.test3(MotesBox.get()):
            mylb.insert(END, item)
            scrolly.config(command=mylb.yview)
    if num[0] == 4:
        mylb.delete(0, 99999999)
        for item in read.test4(TimeBox.get(),MotesBox.get()):
            mylb.insert(END, item)
            scrolly.config(command=mylb.yview)



def showPicture():
    img = cv2.imread("Temperature.png")
    cv2.imshow("Temperature",img)

def showPicture2():
    img = cv2.imread("humidity.png")
    cv2.imshow("humidity",img)

def showPicture3():
    img = cv2.imread("light.png")
    cv2.imshow("light",img)

def showPicture4():
    img = cv2.imread("windSpeed.png")
    cv2.imshow("windSpeed",img)

A=tkinter.Label(top,text="New checked：")
B = tkinter.Button(top, text="Read all sensors file", command=helloCallBack)
C = tkinter.Button(top, text="Read data through time", command=helloCallBack1)
D = tkinter.Button(top, text="Read data through address", command=helloCallBack2)
E = tkinter.Button(top, text="Read data through time and address", command=helloCallBack3)
F = tkinter.Button(top, text="import OK", command=ThisOk)
G=tkinter.Label(top,text="Check to show picture:")
H=tkinter.Label(top,text="input times and motes:")

showTemperature = tkinter.Button(top, text="Temperature", command=showPicture)
showHumidity = tkinter.Button(top, text="humidity", command=showPicture2)
showLight = tkinter.Button(top, text="light", command=showPicture3)
showWindSpeed = tkinter.Button(top, text="windSpeed", command=showPicture4)

lableTime=tkinter.Label(top,text="Time：")
lableMotes=tkinter.Label(top,text="Mac address：")
TimeBox = tkinter.Spinbox(top)
MotesBox = tkinter.Spinbox(top)

Massage = tkinter.Message(top2)
scrolly = Scrollbar(top2)
scrolly.pack(side=RIGHT, fill=Y)
mylb = Listbox(top2, yscrollcommand=scrolly.set,height=50,width=150)
mylb2 = Listbox(top, yscrollcommand=scrolly.set,height=1,width=20)
A.pack()
mylb2.pack()
B.pack()
C.pack()
D.pack()
E.pack()
G.pack()
showTemperature.pack()
showHumidity.pack()
showLight.pack()
showWindSpeed.pack()
H.pack()
lableTime.pack()
TimeBox.pack()
lableMotes.pack()
MotesBox.pack()
F.pack()
mylb.pack()
mylb2.insert(END, "null")
scrolly.config(command=mylb2.yview)

top.mainloop()