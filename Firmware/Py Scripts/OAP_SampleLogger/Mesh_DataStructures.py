from datetime import datetime

class samples: # Sample Object structure
    def __init__(self, timeStr, temp, humid, lux, wind, accel):
        self.timeStr = timeStr
        self.temp = temp
        self.humid = humid
        self.lux = lux
        self.wind = wind
        self.accel = accel


class Mote(samples): # mote Object structure : inherits from samples
    def __init__(self, MAC):
        self.MAC = MAC

    # load a single mote from logfile into ram, using motes MAC address:
    def LoadMote(self, logfile):
        self.temp = []
        self.humid = []
        self.lux = []
        self.wind = []
        self.accel = []
        self.timeStr = []
        for lines in logfile.readlines():
            words = lines.split()
            MACaddr = ''
            if len(words) > 5:
                MACaddr = words[3][1:-2]

            if self.MAC == MACaddr:
                self.timeStr.append(words[0])
                temperature = ''.join(filter(lambda i: i.isdigit(), words[5]))
                self.temp.append(int(temperature))
                #print 'Temp: ' + str(temperature)

                Humid = ''.join(filter(lambda i: i.isdigit(), words[6]))
                self.humid.append(int(Humid))
                #print 'Humid: ' + str(Humid)

                Lux = ''.join(filter(lambda i: i.isdigit(), words[7]))
                self.lux.append(int(Lux))
                #print 'LUX: ' + str(Lux)

                wind = ''.join(filter(lambda i: i.isdigit(), words[8]))
                self.wind.append(int(wind))
                #print 'wind: ' + wind

                axel = ''
                for i in range(9, len(words)):
                    axel = axel + words[i]
                XYZaccel = ''.join(filter(lambda i: i.isdigit(), axel))
                XYZ = []
                for i in range(0, len(XYZaccel) / 3):
                    XYZ.append((int(XYZaccel[i * 3]), int(XYZaccel[i * 3 + 1]), int(XYZaccel[i * 3 + 2])))
                #print 'accel: ' + str(XYZ)
                self.accel.append(XYZ)
        logfile.seek(0)

    # return sample that matches time stamp:
    def timestamp(self, hour, min):
        hours = str(hour)
        mins = str(min)
        if hour < 10:
            hours = '0' + hours
        if min < 10: mins = '0' + mins
        testTime = hours + ':' + mins
        for i in range(len(self.timeStr)):
            if testTime[0:5] == self.timeStr[i][0:5]:
                print 'timestamp found! --> ' + self.timeStr[i]
                return samples(self.timeStr[i], self.temp[i], self.humid[i], self.lux[i], self.wind[i], self.accel[i])


class MeshNetwork(Mote): # Mesh Network object structure : inherits from mote
    def __init__(self):
        self.Motes = []

    # find unique adresses, define mote object with them, and load each one using loadMote():
    def loadMesh(self, logfile):
        uniqAddr = []
        addresses = []
        for lines in logfile.readlines():
            words = lines.split()
            MACaddr = ''
            if len(words) > 5:
                MACaddr = words[3][1:-2]
            addresses.append(MACaddr)
        [uniqAddr.append(x) for x in addresses if x not in uniqAddr]
        uniqAddr.reverse()
        uniqAddr = uniqAddr[0:-1]
        logfile.seek(0)

        print '\nNumber of motes: ' + str(len(uniqAddr))
        for i in range(len(uniqAddr)):
            print 'mote ' + str(i) + ' ---> MAC: ' + uniqAddr[i]
            self.Motes.append(Mote(uniqAddr[i])) # define mote object using MAC
            self.Motes[i].LoadMote(logfile)      # load mote into ram

    # return mote object that matches time stamp:
    def moteMAC(self, MACaddress):
        for i in range(len(self.Motes)):
            if self.Motes[i].MAC == MACaddress:
                return self.Motes[i]

'''
#========================================= MESH NETWORK =============================================
                                        /       |       \
                                      /         |         \
                                    /           |           \
#===============================MOTE1=========MOTE2========MOTE3========MOTE_N.. ====
                                  |             |            |
                                  |             |            |
                                  |             |            |
                            Samples:        Samples:        Samples:
                            Temp  = []      Temp  = []      Temp  = []
                            humid = []      humid = []      humid = []
                            light = []      light = []      light = [] 
                            etc.. = []      etc.. = []      etc.. = []
'''