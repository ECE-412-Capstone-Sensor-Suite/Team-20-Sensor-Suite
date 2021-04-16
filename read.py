# coding=UTF-8

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

readfile = open('spoofed sampleLog.log', 'r')
openwrite = open('output1.txt', "w")
openwrite2 = open('output2.txt', "a+")
openwrite3 = open('output2.txt', "w")

lines = readfile.readlines()
for info in lines:
    try:
        a = info.replace("[", " ").replace("]", " ").replace(",", " ", 5);
        b = a.split()
        c = ('Time=' + b[0] + '\t' + "mote address=" + b[3] + '\t' + 'Temperature=' + b[5] + 'C' + '\t' + 'humidity=' +
             b[
                 6] + '\t' + 'light=' + b[7] + '\t' + 'wind speed=' + b[8] + 'm/s' + '\t' +
             'accelerometer=' + b[9] + b[10] + b[11] + '\n')
        openwrite.write(c)
    except:
        print("Completed")


def getAddress(s):
    motes = []
    exit = False
    while not exit:
        if '#' in s:
            n = s.index('#')
            s = s[:n]
            exit = True
        motes.append(s)
    return motes


def getTimes(s):
    print(s)
    Times = []
    exit = False
    while not exit:
        if '#' in s:
            n = s.index('#')
            s = s[:n]
            exit = True
        Times.append(s)
    return Times


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
    y = range(0, size1)
    print(y)
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
        plt.savefig(fname="Temperature.png",figsize=[10,10])
    if number==2:
        plt.savefig(fname="humidity.png",figsize=[10,10])
    if number==3:
        plt.savefig(fname="light.png",figsize=[10,10])
    if number==4:
        plt.savefig(fname="windSpeed.png",figsize=[10,10])



def readdata(motesList):
    openwrite3.write("")
    d = []
    motes = getAddress(motesList)
    for mote in motes:
        Temperature = []
        humidity = []
        light = []
        windSpeed = []
        for info2 in lines:
            try:
                a = info2.replace("[", " ").replace("]", " ").replace(",", " ", 5);
                b = a.split()
                if b[3] == mote:
                    c = ('Time=' + b[0] + '\t' + "mote address=" + b[3] + '\t' + 'Temperature=' + b[
                        5] + 'C' + '\t' + 'humidity=' + b[
                             6] + '\t' + 'light=' + b[7] + '\t' + 'wind speed=' + b[8] + 'm/s' + '\t' +
                         'accelerometer=' + b[9] + b[10] + b[11] + '\n')
                    d.append(c)
                    openwrite2.write(c)
                    Temperature.append(b[5])
                    humidity.append(b[6])
                    light.append(b[7])
                    windSpeed.append(b[8])
            except:
                print("Completed")
        picture(Temperature, 1)
        picture(humidity, 2)
        picture(light,3)
        picture(windSpeed,4)
        return d


def readdata2(TimesList):
    openwrite3.write("")
    d = []
    Times = getTimes(TimesList)
    for time in Times:
        Temperature = []
        humidity = []
        light = []
        windSpeed = []
        for info2 in lines:
            try:
                a = info2.replace("[", " ").replace("]", " ").replace(",", " ", 5);
                b = a.split()
                if len(b) > 1 and time == b[0][3:5]:
                    c = ('Time=' + b[0] + '\t' + "mote address=" + b[3] + '\t' + 'Temperature=' + b[
                        5] + 'C' + '\t' + 'humidity=' + b[
                             6] + '\t' + 'light=' + b[7] + '\t' + 'wind speed=' + b[8] + 'm/s' + '\t' +
                         'accelerometer=' + b[9] + b[10] + b[11] + '\n')
                    d.append(c)
                    openwrite2.write(c)
                    Temperature.append(b[5])
                    humidity.append(b[6])
                    light.append(b[7])
                    windSpeed.append(b[8])
            except:
                print("Completed")
        picture(Temperature, 1)
        picture(humidity, 2)
        picture(light, 3)
        picture(windSpeed, 4)
        return d


def readdata3(TimesList, motesList):
    openwrite3.write("")
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
                    a = info2.replace("[", " ").replace("]", " ").replace(",", " ", 5);
                    b = a.split()
                    if len(b) > 1 and time == b[0][3:5] and b[3] == mote:
                        c = ('Time=' + b[0] + '\t' + "mote address=" + b[3] + '\t' + 'Temperature=' + b[
                            5] + 'C' + '\t' + 'humidity=' + b[
                                 6] + '\t' + 'light=' + b[7] + '\t' + 'wind speed=' + b[8] + 'm/s' + '\t' +
                             'accelerometer=' + b[9] + b[10] + b[11] + '\n')
                        d.append(c)
                        openwrite2.write(c)
                        Temperature.append(b[5])
                        humidity.append(b[6])
                        light.append(b[7])
                        windSpeed.append(b[8])
                except:
                    print("Completed")
            picture(Temperature, 1)
            picture(humidity, 2)
            picture(light, 3)
            picture(windSpeed, 4)
            return d


def readdata5():
    openwrite3.write("")
    Temperature = []
    humidity = []
    light = []
    windSpeed = []
    d = []
    for info2 in lines:
        try:
            a = info2.replace("[", " ").replace("]", " ").replace(",", " ", 5);
            b = a.split()
            c = ('Time=' + b[0] + '\t' + "mote address=" + b[3] + '\t' + 'Temperature=' + b[
                5] + 'C' + '\t' + 'humidity=' + b[
                     6] + '\t' + 'light=' + b[7] + '\t' + 'wind speed=' + b[8] + 'm/s' + '\t' +
                 'accelerometer=' + b[9] + b[10] + b[11] + '\n')
            d.append(c)
            openwrite2.write(c)
            Temperature.append(b[5])
            humidity.append(b[6])
            light.append(b[7])
            windSpeed.append(b[8])
        except:
            c = "Completed"
            print("Completed")
    picture(Temperature, 1)
    picture(humidity, 2)
    picture(light, 3)
    picture(windSpeed, 4)
    return d


def test():
    lines = readfile.readlines()
    for info in lines:
        try:
            a = info.replace("[", " ").replace("]", " ").replace(",", " ", 5);
            b = a.split()
            c = ('Time=' + b[0] + '\t' + "mote address=" + b[3] + '\t' + 'Temperature=' + b[
                5] + 'C' + '\t' + 'humidity=' + b[
                     6] + '\t' + 'light=' + b[7] + '\t' + 'wind speed=' + b[8] + 'm/s' + '\t' +
                 'accelerometer=' + b[9] + b[10] + b[11] + '\n')
            openwrite.write(c)
        except:
            print("Completed")


def test1():
    return readdata5()


def test2(timesList):
    return readdata2(timesList)


def test3(motesList):
    return readdata(motesList)


def test4(timesList, motesList):
    return readdata3(timesList, motesList)


readfile.close()
openwrite.close()