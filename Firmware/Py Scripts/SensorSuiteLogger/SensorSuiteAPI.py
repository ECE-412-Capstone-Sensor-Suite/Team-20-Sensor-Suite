from datetime import datetime
import sys
import os
from datetime import datetime
class sample: # Sample Object structure
    def __init__(self, timestamp, temp, humid, lux, O2, Co2, accel, wind, rain):
        self.timestamp = timestamp
        self.temp = temp
        self.humid = humid
        self.lux = lux
        self.O2 = O2
        self.Co2 = Co2
        self.accel = accel
        self.wind = wind
        self.rain = rain



class Mote(sample): # mote Object structure : inherits from samples
    def __init__(self, Directory, Logname):
        self.Logname = Logname
        self.Directory = Directory
        self.Logfile = open(self.Directory + self.Logname, "r")

        self.MAC = self.Logfile.readline().split()[2]
        self.status = 'Disconnected'
        self.UID = None
        self.coord = None
        self.samples = []

    # load a single mote from logfile into ram, using motes MAC address:
    def LoadMote(self):
        Loglines = self.Logfile.readlines()
        self.status = Loglines[0].split()[2]
        self.coord = Loglines[1].split()[2]
        self.UID = Loglines[2].split()[3]
        self.CurrentDate = None

        for line in Loglines:
            word = line.split()
            #print word
            if len(word) > 0:
                if word[0] == "--":                         # Update Current Date
                    #datetime.strptime(word[1], "%m/%d/%Y")
                    self.CurrentDate = word[1]
                if word[0] != "~" and word[0] != "--":      # Convert Logfile text into organized sample objects
                    timedate = self.CurrentDate +':'+ word[0][0:-1] # combine time stamp with current date
                    timestamp = datetime.strptime(timedate, "%m/%d/%Y:%H:%M:%S")
                    temp = float(word[1][0:-1])/100
                    humid = float(word[2][0:-1]) / 100
                    lux = float(word[3][0:-1]) / 100
                    o2 = float(word[4][0:-1]) / 100
                    co2 = float(word[5][0:-1]) / 100
                    accel = (float(word[6][0:-1]) / 100,float(word[7][0:-1]) / 100,float(word[8][0:-1]) / 100)
                    wind = float(word[9][0:-1]) / 100
                    rain = float(word[10][0:-1]) / 100
                    self.samples.append(sample(timestamp,temp, humid, lux, o2, co2, accel, wind, rain))
        self.Logfile.seek(0)
        self.Logfile.close()

    # return sample that matches time stamp:
    def timestamp(self, From, to):
        print 's'
    def Sensor(self, sensorIn):
        sensors = ('temp', 'humid')
        self.array = []
        if sensorIn == sensors[0]:
            for sample in self.samples:
                self.array.append(sample.temp)
            return self.array
        elif sensorIn == sensors[1]:
            for sample in self.samples:
                self.array.append(sample.humid)
            return self.array





class MeshNetwork(Mote): # Mesh Network object structure : inherits from mote
    def __init__(self, Directory):
        self.Dir = Directory
        self.Motes = []
        self.MACaddresses = []
        self.MoteFiles = []
        self.NumberofMotes = None
        addresses = []
        MAC_root = "00-17-0d-00-00"
        print("Data Storage Directory: " + self.Dir)
        for file in os.listdir(self.Dir):
            if file.endswith(".log"):
                addresses.append(MAC_root + "-" + file[0:2] + "-" + file[2:4] + "-" + file[4:6])
                self.MoteFiles.append(file)

        [self.MACaddresses.append(x) for x in addresses if x not in self.MACaddresses]
        print("Known Motes: " + str(self.MACaddresses))
    # find unique adresses, define mote object with them, and load each one using loadMote():
    def loadMesh(self):

        print '\nNumber of motes: ' + str(len(self.MACaddresses))
        for i in range(len(self.MoteFiles)):
            print 'mote ' + str(i) + ' ---> MAC: ' + self.MACaddresses[i]

            self.Motes.append(Mote(self.Dir, self.MoteFiles[i])) # define mote object using MAC
            self.Motes[i].LoadMote()      # load mote into ram

    # return mote object that matches time stamp:
    def moteMAC(self, MACaddress):
        for i in range(len(self.Motes)):
            if self.Motes[i].MAC == MACaddress:
                return self.Motes[i]

Data_Loc = sys.path[0] + "/DataOrganization/"
print Data_Loc
Mesh1 = MeshNetwork(Data_Loc)
Mesh1.loadMesh()
print Mesh1.Motes[0].Sensor('humid')
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