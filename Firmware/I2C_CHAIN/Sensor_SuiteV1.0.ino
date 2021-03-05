/* The sketch is made for the Sensor Suite project(Capstone Team 20) that consists of 8 sensors total: 
-Humidity/Temperature, O2 Sensor, CO2 sensor, Vibration sensor(ADXL), Rain Sensor, Light Sensor(OPT3001), 
and Wind Speed Sensor. 

 Credits:
 -Paul Badger 2014
 -Created June 2012 by Anne Mahaffey - hosted on http://annem.github.com/ADXL362
 -ZhixinLiu(zhixin.liu@dfrobot.com)@version V0.2, 2019-10-10
 -Varad Kulkarni <http://www.microcontrollershub.com> Created 28 March 2018
 
 Hardware setup:
 ESP32 Wroom 3.3V, need volage supply of 5V for Wind Speed Sensor and the CO2 Sensor. Rain sensor 
 can operate at 3-5V. 

 */

#include <Wire.h>
#include <DFRobot_OxygenSensor.h>
#include <SPI.h>
#include <ADXL362.h>
#include "DFRobot_OxygenSensor.h"

#define COLLECT_NUMBER    10             // collect number, the collection range is 1-100.
#define Oxygen_IICAddress ADDRESS_3
/*   iic slave Address, The default is ADDRESS_3.
       ADDRESS_0               0x70      // iic device address.
       ADDRESS_1               0x71
       ADDRESS_2               0x72
       ADDRESS_3               0x73
*/
//************************** Global Variables *****************************//
// Slave Addresses:
int humidityAddr = 39; // temperature humidity address (0x27)
int unoAddr = 8; // temperature humidity address (0x08)
int optAddr = 68; //OPT3001 light address (0x44)

// chain sampling periods
int humidityT[2] = {10, 100}; // timing characteristics: {measure request - read request, resampling period}
int unoT[2] = {0, 10};
int opt3001T[2] = {100, 0};

// reading variables
int reading1; // humidity reading
int reading2; // temperature reading
byte reading[10];
//***************************CO2*************************************//
int sensorIn = A2; // CO2 Sensor Input

//*******************ADXL Sensor ************************************//
ADXL362 xl;
int16_t temp;
int16_t XValue, YValue, ZValue, Temperature;

//******************************O2**********************************//
DFRobot_OxygenSensor Oxygen;

//*****************************Wind Speed Sensor*******************//

#define analogPinForRV    1   // change to pins you the analog pins are using
#define analogPinForTMP   0

// to calibrate your sensor, put a glass over it, but the sensor should not be
// touching the desktop surface however.
// adjust the zeroWindAdjustment until your sensor reads about zero with the glass over it. 

const float zeroWindAdjustment =  .2; // negative numbers yield smaller wind speeds and vice versa.

int TMP_Therm_ADunits;  //temp termistor value from wind sensor
float RV_Wind_ADunits;    //RV output from wind sensor 
float RV_Wind_Volts;
unsigned long lastMillis;
int TempCtimes100;
float zeroWind_ADunits;
float zeroWind_volts;
float WindSpeed_MPH;

//******************************Rain Sensor**********************************//
int sensorValue = analogRead(A3); //Rain Sensor Input

//************************** MAIN CODE *****************************//
void setup() {
  Serial.begin(9600);
  Wire.begin(); // Initialize ardiono as master
  
 //*************************OPT3001 Light Sensor********************//
  Wire.beginTransmission(0x44);     // I2C address of OPT3001 = 0x44
  Wire.write(0xCE);
  Wire.write(0x10);
  Wire.endTransmission();
 

//**************************DFR O2 Sensor***************************//
  while(!Oxygen.begin(Oxygen_IICAddress)) {
    Serial.println("I2c device number error !");
    delay(1000);
  }
  Serial.println("I2c connect success !");

//***************************ADXL**********************************//
  xl.begin(10);                   // Setup SPI protocol, issue device soft reset
  xl.beginMeasure();              // Switch ADXL362 to measure mode  

}

void loop() {
  //********HUMID & TEMP SENSOR********//
  slaveSample(true, humidityAddr, 4, humidityT); //** SAMPLE RAW BYTES FROM SENSOR
  
  //** parse bytes from sensor into two 16-bit words, then convert words into accurate data.
  int humidityWord = (reading[0] << 8) | reading[1];    // shift byte0 up 8 bits and add byte1 to it   
  int tempWord = (reading[2] << 8) | reading[3];        // shift byte2 up 8 bits and add byte3 to it 
  
  float humidity = (((float)(humidityWord & 0x3FFF) / (16384 - 2)) * 100); // mask first two status bits and convert to RH
  float temp = (((float)(tempWord & 0x3FFF)) / (16384 - 2)) * 100 - 40;    // mask first unused bits and convert to (C)
  Serial.print("Humidity(%RH): "); Serial.println( humidity);               // print the reading
  Serial.print("Temp(C): "); Serial.println(temp);                          // print the reading
  //Serial.println(humidityWord);
 //********ARDUINO OPT3001 Light SENSOR********//
 slaveCommand(0x44, byte(0x00)); // step 1: instruct sensor to measure
  delay(opt3001T[0]);                   // step 2: wait for readings to happen 
 slaveSample(false, optAddr, 2, opt3001T); //** SAMPLE RAW BYTES FROM SENSOR
  
  int optWord = (reading[0] << 8) | reading[1];
    Serial.print("LUX: ");   // 
    float fLux = SensorOpt3001_convert(optWord);   // Calculate LUX from sensor data
    Serial.println(fLux);  //Print the received data
  
  //********ARDUINO UNO SPOOF SENSOR********//
  //slaveSample(false, unoAddr, 6, unoT);         //** SAMPLE RAW BYTES FROM SENSOR

  //** parse bytes from UNO
  // for(int i=0; i<= 6;i++ ){
   // Serial.print((char)reading[i]);    // print each byte as a character
  // }
   //Serial.println("");                 // print new line


//**************************DFR O2 Sensor***************************//
  float oxygenData = Oxygen.ReadOxygenData(COLLECT_NUMBER);
  Serial.print("O2: ");
  Serial.print(oxygenData);
  Serial.println(" %vol");
  //delay(1000);

//********************Wind Speed Sensor*****************************//

if (millis() - lastMillis > 200){      // read every 200 ms - printing slows this down further
    
    TMP_Therm_ADunits = analogRead(analogPinForTMP);
    RV_Wind_ADunits = analogRead(analogPinForRV);
    RV_Wind_Volts = (RV_Wind_ADunits *  0.0048828125);

    // these are all derived from regressions from raw data as such they depend on a lot of experimental factors
    // such as accuracy of temp sensors, and voltage at the actual wind sensor, (wire losses) which were unaccouted for.
    TempCtimes100 = (0.005 *((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;  

    zeroWind_ADunits = -0.0006*((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172;  //  13.0C  553  482.39

    zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;  

    // This from a regression from data in the form of 
    // Vraw = V0 + b * WindSpeed ^ c
    // V0 is zero wind at a particular temperature
    // The constants b and c were determined by some Excel wrangling with the solver.
    
   WindSpeed_MPH =  pow(((RV_Wind_Volts - zeroWind_volts) /.2300) , 2.7265);   
   
    //Serial.print("  TMP volts ");
    //Serial.print(TMP_Therm_ADunits * 0.0048828125);
    
    //Serial.print(" RV volts ");
    //Serial.print((float)RV_Wind_Volts);

  //  Serial.print("\t  TempC*100 ");
  //  Serial.print(TempCtimes100 );

   // Serial.print("   ZeroWind volts ");
   // Serial.print(zeroWind_volts);

    Serial.print("WindSpeed MPH: ");
    Serial.println((float)WindSpeed_MPH);
    lastMillis = millis();    
}

//**************************DFR CO2 Sensor**************************//
  //Read voltage
  int sensorValue = analogRead(sensorIn);

  // The analog signal is converted to a voltage
  float voltage = sensorValue*(3300/1024.0);
  if(voltage == 0)
  {
    Serial.println("Fault");
  }
  else if(voltage < 400)
  {
    Serial.println("preheating");
  }
  else
  {
    int voltage_diference=voltage-400;
    float concentration=voltage_diference*50.0/16.0;
    // Print Voltage
    //Serial.print("voltage:");
    //Serial.print(voltage);
    //Serial.println("mv");
    //Print CO2 concentration
    Serial.print("CO2: ");
    Serial.print(concentration);
    Serial.println("ppm");
  }

//******************************ADXL Sensor************************************//
// read all three axis in burst to ensure all measurements correspond to same sample time
  xl.readXYZTData(XValue, YValue, ZValue, Temperature);  
  Serial.print("XVALUE=");
  Serial.print(XValue);   
  Serial.print("\tYVALUE=");
  Serial.print(YValue);  
  Serial.print("\tZVALUE=");
  Serial.println(ZValue);  
 // Serial.print("\tTEMPERATURE=");
 // Serial.println(Temperature);   

//******************************Rain Sensor**********************************//
// read the input on analog pin 3:

  Serial.print("Rain Level: ");
  Serial.println(sensorValue);
  


}



//************************** SLAVE CALLING FUNCTION *****************************//
void slaveSample(bool command, int slavAddr, int byteNum, int timing[]) {
  
  if (command) {  //*** CHECK IF SLAVE NEEDS MEASURE REQUEST BEFORE READING
    slaveCommand(slavAddr, byte(0x00)); // step 1: instruct sensor to measure
    delay(timing[0]);                   // step 2: wait for readings to happen
    slaveCommand(slavAddr, byte(0x01)); // step 3: instruct sensor to return a particular echo reading
  }
  Wire.requestFrom(slavAddr, byteNum);  // step 4: request reading from sensor

  for(int i=0; i<= byteNum;i++ ){  // repeat iteration for the number of expected bytes
    if(Wire.available()){
    reading[i]= Wire.read();       // add each new byte into reading array then increment the array
    }
  }
  delay(timing[1]);               // wait a bit since people have to read the output :)

}

//************************** SLAVE HELPER FUNCTIONS *****************************//
void slaveCommand(int slvAddr, byte cmd) {

  Wire.beginTransmission(slvAddr); // transmit to slave address

  Wire.write(cmd);      // command BIT, 0x00= write, 0x01 read

  Wire.endTransmission(); // end transmission
}

int read2Bytes() {
  int wrd;
  wrd = Wire.read();  // receive high byte (overwrites previous reading)
  wrd = wrd << 8;     // shift high byte to be high 8 bits
  wrd |= Wire.read(); // receive low byte as lower 8 bits
  return wrd;
}

float SensorOpt3001_convert(uint16_t iRawData)
{
  uint16_t iExponent, iMantissa;
  iMantissa = iRawData & 0x0FFF;                 // Extract Mantissa
  iExponent = (iRawData & 0xF000) >> 12;         // Extract Exponent 
  return iMantissa * (0.01 * pow(2, iExponent)); // Calculate final LUX
}
