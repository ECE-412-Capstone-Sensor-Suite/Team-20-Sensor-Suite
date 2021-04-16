/*
Copyright (c) 2014, Dust Networks.  All rights reserved.

Arduino sketch which connects to a SmartMesh IP mote and periodically sends a
2-byte value to the manager. You can use the SensorDataReceiver application of
the SmartMesh SDK to see that data arrive.

Note: before you can run this sketch, you need import the sm_clib
library. To do so:
- double click on this file to open the Arduino IDE
- In Sketch > Import Library... > Add Library..., select navigate to the
  sm_clib folder and click open.

Note: before running this sketch:
- configure your SmartMesh IP mote to run in slave mode
- on your SmartMesh IP mote, configure the network ID you the mote to connect
  to.
- remove the battery from your SmartMesh IP mote, it will be powered by the
  Arduino Due
- connect your Arduino Due board to your DC9003 SmartMesh IP mote as detailed
  in the documentation.
- make sure the power switch of the DC9003 SmartMesh IP mote is in the ON
  position.

To run this sketch, connect your Arduino Due board to your computer, and Select
File > Upload. 
  
\license See attached DN_LICENSE.txt.
*/
///////////////////////SMART MESH CLIB//////////////////////////////////////
#include <IpMtWrapper.h>
#include <TriangleGenerator.h>
#include <dn_ipmt.h>

IpMtWrapper       ipmtwrapper;
TriangleGenerator generator;
int arbitraryData;


//=========================== data generator ==================================

void generateData(uint16_t *returnVal) {
   //generator.nextValue(returnVal);
   
   arbitraryData = (arbitraryData + 1) % 10;
   returnVal[0] =  arbitraryData;
   returnVal[1] =  arbitraryData*2;
   returnVal[2] =  arbitraryData*3;
   returnVal[3] =  arbitraryData*4;
   returnVal[4] =  arbitraryData*5;
   returnVal[5] =  arbitraryData*6;
   returnVal[6] =  arbitraryData*7;
   returnVal[7] =  arbitraryData*8;
   returnVal[8] =  arbitraryData*9;
   returnVal[9] =  arbitraryData*10;
   Serial.print("\n     GENERATED VALUE:"); Serial.println(arbitraryData);
   Serial.print("     RETURNED VALUE:"); Serial.println(returnVal[0]);
   Serial.print("     RETURNED VALUE:"); Serial.println(returnVal[1]);
   Serial.print("     RETURNED VALUE:"); Serial.println(returnVal[9]);
}

//=========================== "main" ==========================================

void setup() {
   ipmtwrapper.setup( // SET UP SMART MESH MOTE
      60000,                           // srcPort
      (uint8_t*)ipv6Addr_manager,      // destAddr
      61000,                           // destPort
      10000,                           // dataPeriod (ms)
      generateData                     // dataGenerator
   );
   
}

void loop() {
   ipmtwrapper.loop();
   
}
