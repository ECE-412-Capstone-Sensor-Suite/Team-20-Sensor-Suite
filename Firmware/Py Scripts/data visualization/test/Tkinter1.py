import Tkinter
import read
import cv2
## This is to create two windows, one is control interface, another is display interface
top = Tkinter.Tk() ## control interface
top2 = Tkinter.Tk() ## display interface

## adjust form
num=[]
TimesList = u""
MotesList = u""


##1.check all datas
def helloCallBack():
    mylb.delete(0, 99999999)
    for item in read.test1():
        mylb.insert("end", item)
        scrolly.config(command=mylb.yview)
    mylb2.delete(0, 10)
    mylb2.insert("end", u"Read all sensors file")
    scrolly.config(command=mylb2.yview)

## 2.read data through time, input time, for example 18# (18:00-19:00) or 18#,19# for 2 hours.
def helloCallBack1():
    del num[:]
    num.append(2)
    mylb2.delete(0, 10)
    mylb2.insert("end", u"Read mote1 file")
    scrolly.config(command=mylb2.yview)

 ##3.read data through mac address, input address, for example (00-17-0d-00-00-32-dc-61)#
def helloCallBack2():
    del num[:]
    num.append(3)
    mylb2.delete(0, 10)
    mylb2.insert("end", u"Read mote2 file")
    scrolly.config(command=mylb2.yview)

 ##4.read data through mac address and time
def helloCallBack3():
    del num[:]
    num.append(4)
    lableTime.pack()
    TimeBox.pack()
    lableMotes.pack()
    MotesBox.pack()
    mylb2.delete(0, 10)
    mylb2.insert("end", u"Input mac adress to check mote")
    scrolly.config(command=mylb2.yview)
## for import ok
def ThisOk():
    print num
    if num[0]==2:
        mylb.delete(0, 99999999)
        for item in read.test2(TimeBox.get()):
            mylb.insert("end", item)
            scrolly.config(command=mylb.yview)
    if num[0] == 3:
        mylb.delete(0, 99999999)
        for item in read.test3(MotesBox.get()):
            mylb.insert("end", item)
            scrolly.config(command=mylb.yview)
    if num[0] == 4:
        mylb.delete(0, 99999999)
        for item in read.test4(TimeBox.get(),MotesBox.get()):
            mylb.insert("end", item)
            scrolly.config(command=mylb.yview)


## function to show respectively plots
def showPicture():
    img = cv2.cv2.imread(u"Temperature.png")
    cv2.cv2.imshow(u"Temperature",img)

def showPicture2():
    img = cv2.cv2.imread(u"humidity.png")
    cv2.cv2.imshow(u"humidity",img)

def showPicture3():
    img = cv2.cv2.imread(u"light.png")
    cv2.cv2.imshow(u"light",img)

def showPicture4():
    img = cv2.cv2.imread(u"windSpeed.png")
    cv2.cv2.imshow(u"windSpeed",img)

## B,C,D,E,F = button  A,G,H = label
A= Tkinter.Label(top, text= u"New checked: ")
B = Tkinter.Button(top, text=u"Read all sensors file", command=helloCallBack)
C = Tkinter.Button(top, text=u"Read data through time", command=helloCallBack1)
D = Tkinter.Button(top, text=u"Read data through address", command=helloCallBack2)
E = Tkinter.Button(top, text=u"Read data through time and address", command=helloCallBack3)
F = Tkinter.Button(top, text=u"import OK", command=ThisOk)
G=Tkinter.Label(top,text=u"Check to show picture:")
H=Tkinter.Label(top,text=u"input times and motes:")
## four respective button to show different plots
showTemperature = Tkinter.Button(top, text=u"Temperature", command=showPicture)
showHumidity = Tkinter.Button(top, text=u"humidity", command=showPicture2)
showLight = Tkinter.Button(top, text=u"light", command=showPicture3)
showWindSpeed = Tkinter.Button(top, text=u"windSpeed", command=showPicture4)

## this is function for two inputting block
lableTime=Tkinter.Label(top,text=u"Time:")
lableMotes=Tkinter.Label(top,text=u"Mac address: ")
TimeBox = Tkinter.Spinbox(top)
MotesBox = Tkinter.Spinbox(top)
Massage = Tkinter.Message(top2)
scrolly = Tkinter.Scrollbar(top2)
scrolly.pack({"side": "right"}, fill= "y")
mylb = Tkinter.Listbox(top2, yscrollcommand=scrolly.set,height=50,width=150)
mylb2 = Tkinter.Listbox(top, yscrollcommand=scrolly.set,height=1,width=20)
## pack means make deployment visible. if without it, the interface has no any things, just blank
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
mylb2.insert("end", u"null")
scrolly.config(command=mylb2.yview)
## loop means running it all the time
top.mainloop()