#!/usr/bin/python

# ============================ adjust path =====================================

import sys
import os

'''hard coding the location of lib in relation to C: (NOT VERY FLEXIBLE, will break if you move the script to another pc)'''
# sys.path.insert(0, 'C:\Users\Yesoooof\Desktop\ECE DOCUMENTS\Capstone\Sensor suite\Code\SmartMesh\smartmeshsdk-master\libs') # location of lib
# sys.path.insert(0, 'C:\Users\Yesoooof\Desktop\ECE DOCUMENTS\Capstone\Sensor suite\Code\SmartMesh\smartmeshsdk-master\external_libs') # location of lib

''' coding the location of lib in relation to the location of this script (Flexible as long as lib and this scripts /
                                                                         stay the same locations relative to each other)
'''
if __name__ == "__main__":
    here = sys.path[0]  # sys.path[0] is the file location of the current script
    sys.path.insert(0, os.path.join(here, '..', 'smartmeshsdk-master/libs'))  # join navigates from here to location of lib
    sys.path.insert(0, os.path.join(here, '..', 'smartmeshsdk-master/external_libs'))
# ============================ verify installation =============================

from SmartMeshSDK.utils import SmsdkInstallVerifier

(goodToGo, reason) = SmsdkInstallVerifier.verifyComponents(
    [
        SmsdkInstallVerifier.PYTHON,
        SmsdkInstallVerifier.PYSERIAL,
    ]
)
if not goodToGo:
    print "Your installation does not allow this application to run:\n"
    print reason
    raw_input("Press any button to exit")
    sys.exit(1)

# ============================ imports =========================================

import threading
from optparse import OptionParser

from SmartMeshSDK.utils import AppUtils, \
    FormatUtils
from SmartMeshSDK.ApiDefinition import IpMgrDefinition
from SmartMeshSDK.IpMgrConnectorMux import IpMgrConnectorMux, \
    IpMgrSubscribe
from dustUI import dustWindow, \
    dustFrameConnection, \
    dustFrameSensorData

# ============================ logging =========================================

# local

import logging
import datetime
from random import randint

class NullHandler(logging.Handler):
    def emit(self, record):
        pass


log = logging.getLogger('App')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

# global

AppUtils.configureLogging()

# ============================ defines =========================================

UPDATEPERIOD = 500  # in ms
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 9900

Known_Macs = []
Data_Loc = sys.path[3] + "/DataOrganization/"
MAC_root = "00-17-0d-00-00"
print("Data Storage Directory: " + Data_Loc)
for file in os.listdir(Data_Loc):
    if file.endswith(".log"):
        fileName = os.path.join(file)
        Known_Macs.append(MAC_root + "-" + fileName[0:2] + "-" + fileName[2:4] + "-" + fileName[4:6])
print("Known Motes: " + str(Known_Macs))
# ============================ body ============================================

##
# \addtogroup SensorDataReceiver
# \{
#


class notifClient(object):

    def __init__(self, connector, disconnectedCallback):

        # store params
        self.connector = connector
        self.disconnectedCallback = disconnectedCallback

        # variables
        self.data = None
        self.dataLock = threading.Lock()

        # subscriber
        self.subscriber = IpMgrSubscribe.IpMgrSubscribe(self.connector)
        self.subscriber.start()
        self.subscriber.subscribe(
            notifTypes=[
                IpMgrSubscribe.IpMgrSubscribe.NOTIFDATA,
            ],
            fun=self._notifDataCallback,
            isRlbl=False,
        )
        self.subscriber.subscribe(
            notifTypes=[
                IpMgrSubscribe.IpMgrSubscribe.ERROR,
                IpMgrSubscribe.IpMgrSubscribe.FINISH,
            ],
            fun=self.disconnectedCallback,
            isRlbl=True,
        )

    # ======================== public ==========================================

    def getSensorData(self):
        self.dataLock.acquire()
        if self.data:
            returnVal = self.data.copy()
            self.data = None
        else:
            returnVal = None
        self.dataLock.release()
        return returnVal

    def disconnect(self):
        self.connector.disconnect()

    # ======================== private =========================================

    def _notifDataCallback(self, notifName, notifParams):

        self.dataLock.acquire()
        self.data = {}
        self.data['srcMac'] = notifParams.macAddress
        self.data['srcPort'] = notifParams.srcPort
        self.data['destPort'] = notifParams.dstPort
        self.data['payload'] = notifParams.data
        self.data['ts_sec'] = notifParams.utcSecs
        self.data['ts_usec'] = notifParams.utcUsecs
        self.dataLock.release()
        simple_data_Logging(notifParams.macAddress, notifParams.data)


class dataGui(object):

    def __init__(self):

        # local variables
        self.guiLock = threading.Lock()
        self.apiDef = IpMgrDefinition.IpMgrDefinition()
        self.notifClientHandler = None

        # create window
        self.window = dustWindow.dustWindow('SensorDataReceiver',
                                            self._windowCb_close)

        # add a connection frame
        self.connectionFrame = dustFrameConnection.dustFrameConnection(
            self.window,
            self.guiLock,
            self._connectionFrameCb_connected,
            frameName="manager connection",
            row=0, column=0)
        self.connectionFrame.apiLoaded(self.apiDef)
        self.connectionFrame.show()

        # add a sensor data frame
        self.sensorDataFrame = dustFrameSensorData.dustFrameSensorData(self.window,
                                                                       self.guiLock,
                                                                       frameName="received sensor data",
                                                                       row=1, column=0)
        self.sensorDataFrame.show()

    # ======================== public ==========================================

    def start(self, connect_params):

        '''
        This command instructs the GUI to start executing and reacting to
        user interactions. It never returns and should therefore be the last
        command called.
        '''
        try:
            self.window.mainloop()
        except SystemExit:
            sys.exit()

    # ======================== private =========================================

    def _windowCb_close(self):
        if self.notifClientHandler:
            self.notifClientHandler.disconnect()

    def _connectionFrameCb_connected(self, connector):
        '''
        \brief Called when the connectionFrame has connected.
        '''

        # store the connector
        self.connector = connector

        # schedule the GUI to update itself in UPDATEPERIOD ms
        self.sensorDataFrame.after(UPDATEPERIOD, self._updateSensorData)
        # start a notification client
        self.notifClientHandler = notifClient(
            self.connector,
            self._connectionFrameCb_disconnected
        )

    def _connectionFrameCb_disconnected(self, notifName, notifParams):
        '''
        \brief Called when the connectionFrame has disconnected.
        '''

        # update the GUI
        self.connectionFrame.updateGuiDisconnected()

        # delete the connector
        if self.connector:
            self.connector.disconnect()
        self.connector = None

    def _updateSensorData(self):

        # get the data
        sensorDataToDisplay = self.notifClientHandler.getSensorData()
        # update the frame
        if sensorDataToDisplay:
            self.sensorDataFrame.update(sensorDataToDisplay)

        # schedule the next update
        self.sensorDataFrame.after(UPDATEPERIOD, self._updateSensorData)


def simple_data_Logging(mac, payload):
    macSTR = FormatUtils.formatMacString(mac)                                   # convert mac address to string
    logname = macSTR[-8:-6] + macSTR[-5:-3] + macSTR[-2] + macSTR[-1] + ".log"  # determine logname
    print('sensor data recieved --> ' + logname)

    CheckMoteRegestry(macSTR, logname)
    samples = [None] * (len(payload)/2)                         # reformating payload into 16 bit words
    for i in range(len(samples)):
        samples[i] = (payload[i*2] << 8) | (payload[ (i*2) + 1])

    # logging
    logFile = open(Data_Loc + logname, "a+")
    UpdateDate(logname,logFile)
    currentDTandTM = datetime.datetime.now()
    logFile.write('\n{TIME}, {SAMPLES}'.format(
        TIME=currentDTandTM.strftime('%H:%M:%S'),
        SAMPLES=str(samples)[1:-1],
    ))
    logFile.close()

def UpdateDate(logname,logFile):
    newdate = True
    currentDate = datetime.datetime.now().strftime('%m/%d/%Y')
    for lines in logFile.readlines():
        if len(lines.split())>1:
            if lines.split()[0] == "--":
                print 'checking date ' + lines.split()[1] + ' against ' + currentDate
                if lines.split()[1] == currentDate:
                    print 'same dates'
                    newdate = False
    if newdate == True:
        print 'new date --> ' + currentDate
        logFile.write('\n' + '-- ' + currentDate + '\n')
        return
    else:
        return
    return



def CheckMoteRegestry(testMac, logname):
    newMac = True
    for Mac in Known_Macs:
        if testMac == Mac:
            newMac = False
    if newMac:
        print("New Mote --->" + testMac)
        logFile = open(Data_Loc + logname, "w")
        logFile.write('~     MAC: ' + testMac + '\n')
        logFile.write('~  Status: ' + 'OPERATIONAL' + '\n')
        logFile.write('~   Coord: ' + '(' + str(None)+','+str(None)+')' + '\n')
        logFile.write('~ User ID: ' + str(None) + '\n')
        logFile.write('-- ' + datetime.datetime.now().strftime('%m/%d/%Y') + '\n')
        logFile.close()
        Known_Macs.append(testMac)

# ============================ main ============================================

def main(connect_params):
    dataGuiHandler = dataGui()
    dataGuiHandler.start(connect_params)

if __name__ == '__main__':
    # Parse the command line
    parser = OptionParser("usage: %prog [options]", version="%prog 1.0")
    parser.add_option("--host", dest="host",
                      default=DEFAULT_HOST,
                      help="Mux host to connect to")
    parser.add_option("-p", "--port", dest="port",
                      default=DEFAULT_PORT,
                      help="Mux port to connect to")
    (options, args) = parser.parse_args()

    connect_params = {
        'host': options.host,
        'port': int(options.port),
    }
    main(connect_params)

##
# end of SensorDataReceiver
# \}
#
