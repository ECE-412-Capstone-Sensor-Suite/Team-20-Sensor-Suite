import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

readfile = open('spoofed sampleLog.log', 'r')
openwrite = open('output1.txt', "w")
openwrite2 = open('output2.txt', "a+")
openwrite3 = open('output2.txt', "w")
motes = []

lines = readfile.readlines()
for info in lines:
    try:
        a = info.replace("[", " ").replace("]", " ").replace(",", " ", 5);
        b = a.split()
        c = ('Time=' + b[0] + '\t' + "mote address=" + b[3] + '\t' + 'Temperature=' + b[5] +'C' + '\t' + 'humidity=' + b[
            6] + '\t' + 'light=' + b[7] + '\t' + 'wind speed=' + b[8] + 'm/s'+'\t' +
             'accelerometer=' + b[9] + b[10] + b[11] + '\n')
        openwrite.write(c)
    except:
        print("Completed")

exit = False
while not exit:
    s = input("input address of mote, for example:(00-17-0d-00-00-32-cd-b6)# ：")
    if '#' in s:
        n = s.index('#')
        s = s[:n]
        exit = True
    motes.append(s)


def picture(list):
    list2=[]
    MinNum=9999
    MaxNum=0
    for num in list:
        num2=int(num)
        if MinNum>num2:
            MinNum=num2
        if MaxNum<num2:
            MaxNum=num2
        list2.append(num2)
    size1 = len(list)
    fig, ax = plt.subplots(1, 1)
    y = range(0, size1)
    print(y)
    ax.plot(y,list2)
    if MaxNum - MinNum >= 100 and MaxNum - MinNum <= 500:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    if MaxNum-MinNum>=500 and MaxNum-MinNum<=1000:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    if MaxNum-MinNum>=1000 and MaxNum-MinNum<=4000:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(200))
    if MaxNum - MinNum > 4000 :
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
    plt.show()


class readdata:
    openwrite3.write("")
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
                    openwrite2.write(c)
                    Temperature.append(b[5])
                    humidity.append(b[6])
                    light.append(b[7])
                    windSpeed.append(b[8])
            except:
                print("Completed")


        picture(Temperature)
        picture(humidity)
        picture(light)
        picture(windSpeed)


readfile.close()
openwrite.close()