from Mesh_DataStructures import MeshNetwork
from Mesh_DataStructures import Mote

# LOADING SAMPLES INTO MESH / MOTE STRUCTURE
readLog = open('spoofed sampleLog.log', 'r')

mote1 = Mote('00-17-0d-00-00-32-23-d3')    # define mote object with mac address = '00-17-0d-00-00-32-23-d3'
mote1.LoadMote(readLog)                    # load logfile contents related mote1 and store in mote1 object

Mesh = MeshNetwork()        # define MeshNetwrok Object
Mesh.loadMesh(readLog)      # load Log file contents for ALL motes within int Mesh object, Prints out mote MACs and IDs

readLog.close()

# MeshNetwork indexing: Mesh= [mote2, mote1, ... ], mote1 = [mac, temp,  humidity ...], temp = [sample0, sample1, ...]
# to access smaple1 from mote0: ---> sample1 =  Mesh.Motes[0].temp[1]
print '\nPrint 3 Temp and Humidity samples from each mote'
for mote in Mesh.Motes:
    print 'Mote: ' + mote.MAC
    for i in range(3):
        print 'Temp: ' + str( mote.temp[i] ) + ' & ' + 'Humidity: ' + str( mote.humid[i] ) + ' @ ' + mote.timeStr[i]

# MoteID and Timestamp Indexing
print '\nCalling sample from specific mote at specific time using MoteID and timeStamp:'
sample = Mesh.Motes[3].timestamp(18,3) # store all samples at time 18:03

print float(sample.humid)/100               # SAMPLES ARE LOADED AS INTEGERS SO THEY CAN BE MANIPULATED AS NUMBERS !!!!
print str( sample.wind ) + ' mph'
print str( float(sample.temp)/100 ) + 'C'
print str( sample.lux ) + ' lux'

# Calling all sample of a single type as an array:
print '\nAll temp readings from Mote 2'
Temps = Mesh.Motes[2].temp
print Temps

# if you dont know MoteID for specific mote:
print '\nCalling samples from specific mote at specific time using Mac Address and timeStamp:'
MacSample = Mesh.moteMAC('00-17-0d-00-00-32-23-d3').timestamp(19,10)   # store all samples at time 18:03
print 'temp = ' + str(float(MacSample.temp)/100) + 'C' + ' @ ' + MacSample.timeStr


print Mesh.Motes[0].temp[-1]

    #for index in range(1,3):
        #print moteI.temp[0]
        #print 'temp: ' + str( moteI.temp[index] ) + ' & ' + 'Humidity: ' + str( moteI.humid[index] ) + ' @ ' + moteI.timeStr[index]