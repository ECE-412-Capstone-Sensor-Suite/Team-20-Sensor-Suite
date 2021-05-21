# coding=UTF-8

from __future__ import absolute_import
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from io import open

readfile = open(u'spoofed_sampleLog.log', u'r')
openwrite = open(u'output1.txt', u"w")
openwrite2 = open(u'output2.txt', u"a+")
openwrite3 = open(u'output2.txt', u"w")

## Part1 ：read all data before click anything because if without it, process cannot be executed
lines = readfile.readlines()
for info in lines:
    try:
        a = info.replace(u"[", u" ").replace(u"]", u" ").replace(u",", u" ", 5)
        b = a.split()
        c = (u'Time=' + b[0] + u'\t' + u"mote address=" + b[3] + u'\t' + u'Temperature=' + b[5] + u'C' + u'\t' + u'humidity=' +
             b[
                 6] + u'\t' + u'light=' + b[7] + u'\t' + u'wind speed=' + b[8] + u'm/s' + u'\t' +
             u'accelerometer=' + b[9] + b[10] + b[11] + u'\n')
        openwrite.write(c)
    except:
        print u"Completed"

## This function is used to tell you that the input number(address) should be ended by #
def getAddress(s):
    motes = []
    exit = False
    while not exit:
        if u'#' in s:
            n = s.index(u'#')
            s = s[:n]
            exit = True
        motes.append(s)
    return motes

## This function is used to tell you that the input number(time) should be ended by #
def getTimes(s):
    print s
    Times = []
    exit = False
    while not exit:
        if u'#' in s:
            n = s.index(u'#')
            s = s[:n]
            exit = True
        Times.append(s)
    return Times

## This function is used to limit the range of plots, because if without it, the range of plots is random
def picture(list,number):
    list2 = []
    MinNum = 9999
    MaxNum = 0
    for num in list:
        num2 = int(num)
        if MinNum > num2:
            MinNum = num2
        if MaxNum < num2:
            MaxNum = num2
        list2.append(num2)
    size1 = len(list)
    fig, ax = plt.subplots(1, 1)
    y = xrange(0, size1)
    print y
    ax.plot(y, list2)
    if MaxNum - MinNum >= 100 and MaxNum - MinNum <= 500:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    if MaxNum - MinNum >= 500 and MaxNum - MinNum <= 1000:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    if MaxNum - MinNum >= 1000 and MaxNum - MinNum <= 4000:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(200))
    if MaxNum - MinNum > 4000:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
    if number==1:
        plt.savefig("Temperature.png",figsize=[10,10])
    if number==2:
        plt.savefig("humidity.png",figsize=[10,10])
    if number==3:
        plt.savefig("light.png",figsize=[10,10])
    if number==4:
        plt.savefig("windSpeed.png",figsize=[10,10])


## This function is used to get data by imputing mac address
def readdata(motesList):
    openwrite3.write(u"")
    d = []
    motes = getAddress(motesList)
    for mote in motes:
        Temperature = []
        humidity = []
        light = []
        windSpeed = []
        for info2 in lines:
            try:
                a = info2.replace(u"[", u" ").replace(u"]", u" ").replace(u",", u" ", 5);
                b = a.split()
                if b[3] == mote:
                    c = (u'Time=' + b[0] + u'\t' + u"mote address=" + b[3] + u'\t' + u'Temperature=' + b[
                        5] + u'C' + u'\t' + u'humidity=' + b[
                             6] + u'\t' + u'light=' + b[7] + u'\t' + u'wind speed=' + b[8] + u'm/s' + u'\t' +
                         u'accelerometer=' + b[9] + b[10] + b[11] + u'\n')
                    d.append(c)
                    openwrite2.write(c)
                    Temperature.append(b[5])
                    humidity.append(b[6])
                    light.append(b[7])
                    windSpeed.append(b[8])
            except:
                print u"Completed"
        picture(Temperature, 1)
        picture(humidity, 2)
        picture(light,3)
        picture(windSpeed,4)
        return d

## This function is used to get data by imputing time
def readdata2(TimesList):
    openwrite3.write(u"")
    d = []
    Times = getTimes(TimesList)
    for time in Times:
        Temperature = []
        humidity = []
        light = []
        windSpeed = []
        for info2 in lines:
            try:
                a = info2.replace(u"[", u" ").replace(u"]", u" ").replace(u",", u" ", 5);
                b = a.split()
                if len(b) > 1 and time == b[0][3:5]:
                    c = (u'Time=' + b[0] + u'\t' + u"mote address=" + b[3] + u'\t' + u'Temperature=' + b[
                        5] + u'C' + u'\t' + u'humidity=' + b[
                             6] + u'\t' + u'light=' + b[7] + u'\t' + u'wind speed=' + b[8] + u'm/s' + u'\t' +
                         u'accelerometer=' + b[9] + b[10] + b[11] + u'\n')
                    d.append(c)
                    openwrite2.write(c)
                    Temperature.append(b[5])
                    humidity.append(b[6])
                    light.append(b[7])
                    windSpeed.append(b[8])
            except:
                print u"Completed"
        picture(Temperature, 1)
        picture(humidity, 2)
        picture(light, 3)
        picture(windSpeed, 4)
        return d

## This function is used to get data by imputing mac address and time
def readdata3(TimesList, motesList):
    openwrite3.write(u"")
    d = []
    Times = getTimes(TimesList)
    motes = getAddress(motesList)
    for time in Times:
        for mote in motes:
            Temperature = []
            humidity = []
            light = []
            windSpeed = []
            for info2 in lines:
                try:
                    a = info2.replace(u"[", u" ").replace(u"]", u" ").replace(u",", u" ", 5);
                    b = a.split()
                    if len(b) > 1 and time == b[0][3:5] and b[3] == mote:
                        c = (u'Time=' + b[0] + u'\t' + u"mote address=" + b[3] + u'\t' + u'Temperature=' + b[
                            5] + u'C' + u'\t' + u'humidity=' + b[
                                 6] + u'\t' + u'light=' + b[7] + u'\t' + u'wind speed=' + b[8] + u'm/s' + u'\t' +
                             u'accelerometer=' + b[9] + b[10] + b[11] + u'\n')
                        d.append(c)
                        openwrite2.write(c)
                        Temperature.append(b[5])
                        humidity.append(b[6])
                        light.append(b[7])
                        windSpeed.append(b[8])
                except:
                    print u"Completed"
            picture(Temperature, 1)
            picture(humidity, 2)
            picture(light, 3)
            picture(windSpeed, 4)
            return d

## read all data
def readdata5():
    openwrite3.write(u"")
    Temperature = []
    humidity = []
    light = []
    windSpeed = []
    d = []
    for info2 in lines:
        try:
            a = info2.replace(u"[", u" ").replace(u"]", u" ").replace(u",", u" ", 5);
            b = a.split()
            c = (u'Time=' + b[0] + u'\t' + u"mote address=" + b[3] + u'\t' + u'Temperature=' + b[
                5] + u'C' + u'\t' + u'humidity=' + b[
                     6] + u'\t' + u'light=' + b[7] + u'\t' + u'wind speed=' + b[8] + u'm/s' + u'\t' +
                 u'accelerometer=' + b[9] + b[10] + b[11] + u'\n')
            d.append(c)
            openwrite2.write(c)
            Temperature.append(b[5])
            humidity.append(b[6])
            light.append(b[7])
            windSpeed.append(b[8])
        except:
            c = u"Completed"
            print u"Completed"
    picture(Temperature, 1)
    picture(humidity, 2)
    picture(light, 3)
    picture(windSpeed, 4)
    return d

## define above results as functions
def test1():
    return readdata5()


def test2(timesList):
    return readdata2(timesList)


def test3(motesList):
    return readdata(motesList)


def test4(timesList, motesList):
    return readdata3(timesList, motesList)

## close files
readfile.close()
openwrite.close()