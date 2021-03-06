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

from SmartMeshSDK import sdk_version
from SmartMeshSDK.utils import AppUtils, \
    FormatUtils
from SmartMeshSDK.IpMgrConnectorSerial import IpMgrConnectorSerial
from SmartMeshSDK.IpMgrConnectorMux import IpMgrSubscribe
from SmartMeshSDK.protocols.oap import OAPDispatcher, \
    OAPNotif

# ============================ logging =========================================

# local

import logging
import datetime
from random import randint

class NullHandler(logging.Handler): # defining new class based on logging.handler but overwriting emit() so it passes
    def emit(self, record):
        pass


log = logging.getLogger('App')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

# global

AppUtils.configureLogging()

# ============================ defines =========================================

DEFAULT_SERIALPORT = 'COM15'


# ============================ helper functions ================================
def simple_data_Logging(mac, samples):
    # generating random humidity, light, wind speed, accelerometer data
    #spoof_samples = [samples[0], randint(0,10000),randint(0,1000), randint(0,600)]
    #acceldata = []
    #for index in range(10):
        #acceldata.append((randint(0,10), randint(0,10), randint(0,10)))
    #spoof_samples.append(acceldata)

    # logging
    currentDTandTM = datetime.datetime.now()
    logFile = open("sampleLog.log","a")
    logFile.writelines('\n{TIME} - mote: ({MAC}), sampled: {SAMPLES}'.format(
        TIME= currentDTandTM.strftime('%H:%M:%S'),
        MAC=FormatUtils.formatMacString(mac),
        SAMPLES= samples,
    ))

# called when the manager generates a data notification
def handle_data(notifName, notifParams):
    # have the OAP dispatcher parse the packet.
    # It will call handle_oap_data() is this data is a valid OAP data.
    oapdispatcher.dispatch_pkt(notifName, notifParams)


# called when the OAP dispatcher can succesfully parse received data as OAP
def handle_oap_data(mac, notif):
    if isinstance(notif, OAPNotif.OAPTempSample):
        print 't={TEMP:.2f}C at {MAC}'.format(
            TEMP=float(notif.samples[0]) / 100,
            MAC=FormatUtils.formatMacString(mac),
        )
        simple_data_Logging(mac,notif.samples)



# ============================ main ============================================

# print banner
print 'TempLogger - (c) Dust Networks'
print 'SmartMesh SDK {0}'.format('.'.join([str(b) for b in sdk_version.VERSION]))

# set up the OAP dispatcher (which parses OAP packets)
oapdispatcher = OAPDispatcher.OAPDispatcher()
oapdispatcher.register_notif_handler(handle_oap_data)

# start logging file
logFile = open("sampleLog.log","w")

logFile.write('Date: ' + datetime.datetime.now().strftime('%m/%d/%Y' + '\n'))
logFile.close()

# ask user for serial port number
serialport = raw_input('\nSmartMesh IP manager\'s API serial port (leave blank for ' + DEFAULT_SERIALPORT + '): ')
if not serialport.strip():
    serialport = DEFAULT_SERIALPORT

# connect to manager
connector = IpMgrConnectorSerial.IpMgrConnectorSerial()
try:
    connector.connect({
        'port': serialport,
    })
except Exception as err:
    print 'failed to connect to manager at {0}, error ({1})\n{2}'.format(
        serialport,
        type(err),
        err
    )
    raw_input('Aborting. Press Enter to close.')
    sys.exit(1)
else:
    print 'Connected to {0}.\n'.format(serialport)

# subscribe to data notifications
subscriber = IpMgrSubscribe.IpMgrSubscribe(connector)
subscriber.start()
subscriber.subscribe(
    notifTypes=[
        IpMgrSubscribe.IpMgrSubscribe.NOTIFDATA,
    ],
    fun=handle_data,
    isRlbl=False,
)
