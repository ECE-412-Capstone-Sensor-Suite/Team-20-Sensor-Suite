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


#include <Wire_CC.h>
//#include <DFRobot_OxygenSensor.h>
//#include "DFRobot_OxygenSensor.h"

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
int adxl345 = 0x53; // The ADXL345 sensor I2C address

// chain sampling periods
int humidityT[2] = {10, 5}; // timing characteristics: {WAIT AFTER WRITE 1, WAIT AFTER WRITE2}
int unoT[2] = {0, 10};
int opt3001T[2] = {100, 0};
int adxl345T[2] = {10,0};

// reading variables
int reading1; // humidity reading
int reading2; // temperature reading
byte reading[32];
//***************************CO2*************************************//
int sensorIn = 6; // CO2 Sensor Input

//*******************ADXL Sensor ************************************//
float X_out, Y_out, Z_out;  // Outputs

//******************************O2**********************************//
//DFRobot_OxygenSensor Oxygen;

//*****************************Wind Speed Sensor*******************//

#define analogPinForRV    60   // change to pins you the analog pins are using
#define analogPinForTMP   58

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
int sensorValue = analogRead(2); //Rain Sensor Input

//============================================================================================================//
//========================================  {INITIALIZE SENSORS} =============================================//
void setup() {
  Serial.begin(9600);
  Wire.begin(); // Initialize ardiono as master

  //*************************OPT3001 Light Sensor********************//
  Wire.beginTransmission(0x44);     // I2C address of OPT3001 = 0x44
  Wire.write(0x01);
  Wire.write(0xCE);
  Wire.write(0x10);
  Wire.endTransmission();
  // Set ADXL345 in measuring mode
  Wire.beginTransmission(adxl345); // Start communicating with the device 
  Wire.write(0x2D); // Access/ talk to POWER_CTL Register - 0x2D
  // Enable measurement
  Wire.write(8); // (8dec -> 0000 1000 binary) Bit D3 High for measuring enable 

  
  Wire.endTransmission();


  //**************************DFR O2 Sensor***************************//
//  while (!Oxygen.begin(Oxygen_IICAddress)) {
 //   Serial.println("I2c device number error !");
 //   delay(1000);
  }
 // Serial.println("I2c connect success !");


//}
//============================================================================================================//
//==========================================  {MAIN LOOP} ====================================================//
void loop() {
  
  //********HUMID & TEMP SENSOR********//
  ///slaveSample template: 
  //          {ADDRESS, 1ST WRITE, 2ND WRITE, WAIT TIMES , EXPECTED NO. OF  BYTES}
  slaveSample(humidityAddr, byte(0x00), byte(0x01), humidityT, 4); //** SAMPLE RAW BYTES FROM SENSOR


  //** parse bytes from sensor into two 16-bit words, then convert words into accurate data.
  int humidityWord = (reading[0] << 8) | reading[1];    // shift byte0 up 8 bits and add byte1 to it
  int tempWord = (reading[2] << 8) | reading[3];        // shift byte2 up 8 bits and add byte3 to it

  float humidity = (((float)(humidityWord & 0x3FFF) / (16384 - 2)) * 100); // mask first two status bits and convert to RH
  float temp = (((float)(tempWord & 0x3FFF)) / (16384 - 2)) * 100 - 40;    // mask first unused bits and convert to (C)
  Serial.print("Humidity(%RH): "); Serial.println( humidity);               // print the reading
  Serial.print("Temp(C): "); Serial.println(temp);                          // print the reading


  //********ARDUINO OPT3001 Light SENSOR********//
  //slaveSample template: 
  //         {ADDRESS, 1ST WRITE, byte(0xFF) = DONT WRITE, WAIT TIMES , EXPECTED NO. OF  BYTES}
  slaveSample(optAddr, byte(0x00), byte(0xFF), opt3001T, 2); //** SAMPLE RAW BYTES FROM SENSOR
  /// inputting byte(0xFF) into a write word means you dont want to write any words

  int optWord = (reading[0] << 8) | reading[1];
  Serial.print("LUX: ");                          //
  float fLux = SensorOpt3001_convert(optWord);    // Calculate LUX from sensor data
  Serial.println(fLux);                           //Print the received data

  //********ADXL345 Acceleramoter Sensor*********//
  // === Read acceleromter data === //
  Wire.beginTransmission(adxl345);
  Wire.write(0x32); // Start with register 0x32 (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(adxl345, 6, true); // Read 6 registers total, each axis value is stored in 2 registers

  X_out = ( Wire.read()| Wire.read() << 8); // X-axis value
  X_out = X_out/256; //For a range of +-2g, we need to divide the raw values by 256, according to the datasheet
  Y_out = ( Wire.read()| Wire.read() << 8); // Y-axis value
  Y_out = Y_out/256;
  Z_out = ( Wire.read()| Wire.read() << 8); // Z-axis value
  Z_out = Z_out/256;

  Serial.print("Xa= ");
  Serial.print(X_out);
  Serial.print("   Ya= ");
  Serial.print(Y_out);
  Serial.print("   Za= ");
  Serial.println(Z_out);


  //**************************DFR O2 Sensor***************************//
  /*float oxygenData = Oxygen.ReadOxygenData(COLLECT_NUMBER);
  Serial.print("O2: ");
  Serial.print(oxygenData);
  Serial.println(" %vol");
  //delay(1000);*/
  //************************** O2 using I2C chain fxn***************************//
  int O2addr = byte(0x70);
  int O2_Timing[2] = {100,0};
  int O2_readflashT[2] = {50,0};
  int O2_Exptd_bytes = 3;
  int o2_num_read = 10;                   // collectnum
  float  OxygenData[100] = {0.00f};
  float key;
  static uint8_t i = 0 ,j = 0;
      
  //** READFLASH() : has to be done before reading new data
  slaveSample(O2addr, byte(0x0A), byte(0xFF), O2_readflashT, 1); // read from flash at 0x0A
  if(reading[0] == 0) {
    key = 20.9 / 120.0;
  }else {
    key = (float)reading[0] / 1000.0;
  }
  
  //** ReadOxygenData() : reading new data
  if(o2_num_read > 0) {
    for(j = o2_num_read - 1;  j > 0; j--) {  OxygenData[j] = OxygenData[j-1]; }
    slaveSample(O2addr, byte(0x03), byte(0xFF), O2_Timing, O2_Exptd_bytes); //** read from oxygen data regester 0x03
    OxygenData[0] = ((key) * (((float)reading[0]) + ((float)reading[1] / 10.0) + ((float)reading[2] / 100.0)));
    if(i < o2_num_read) i++;
    Serial.print("O2: ");
    Serial.print(getAverageNum(OxygenData, i));
    Serial.println(" %vol");
  }else {
    Serial.print("error");
  }

  //********************Wind Speed Sensor*****************************//

  if (millis() - lastMillis > 200) {     // read every 200 ms - printing slows this down further

    TMP_Therm_ADunits = analogRead(analogPinForTMP);
    RV_Wind_ADunits = analogRead(analogPinForRV);
    RV_Wind_Volts = (RV_Wind_ADunits *  0.0048828125);

    // these are all derived from regressions from raw data as such they depend on a lot of experimental factors
    // such as accuracy of temp sensors, and voltage at the actual wind sensor, (wire losses) which were unaccouted for.
    TempCtimes100 = (0.005 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;

    zeroWind_ADunits = -0.0006 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172; //  13.0C  553  482.39

    zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;

    // This from a regression from data in the form of
    // Vraw = V0 + b * WindSpeed ^ c
    // V0 is zero wind at a particular temperature
    // The constants b and c were determined by some Excel wrangling with the solver.

    WindSpeed_MPH =  pow(((RV_Wind_Volts - zeroWind_volts) / .2300) , 2.7265);

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
  float voltage = sensorValue * (3300 / 1024.0);
  if (voltage == 0)
  {
    Serial.println("Fault");
  }
  else if (voltage < 400)
  {
    Serial.println("preheating");
  }
  else
  {
    int voltage_diference = voltage - 400;
    float concentration = voltage_diference * 50.0 / 16.0;
    // Print Voltage
    //Serial.print("voltage:");
    //Serial.print(voltage);
    //Serial.println("mv");
    //Print CO2 concentration
    Serial.print("CO2: ");
    Serial.print(concentration);
    Serial.println("ppm");
  }



  //******************************Rain Sensor**********************************//
  // read the input on analog pin 3:

  Serial.print("Rain Level: ");
  Serial.println(sensorValue);



}



//************************** SLAVE CALLING FUNCTION *****************************//
void slaveSample(int slavAddr, byte word1, byte word2, int wait[] , int byteNum) {

  if (word1 != byte(0xFF)) {  //*** CHECK IF SLAVE NEEDS MEASURE REQUEST BEFORE READING
    slaveCommand(slavAddr, word1);  // step 1: instruct sensor to measure
    delay(wait[0]);                   // step 2: wait for readings to happen
  }
  
  if (word2 != byte(0xFF)) {  //*** CHECK IF SLAVE NEEDS MEASURE REQUEST BEFORE READING
    slaveCommand(slavAddr, word2);  // step 3: instruct sensor to return a reading
    delay(wait[1]);                 // wait before reading
    
  }

  Wire.requestFrom(slavAddr, byteNum);  // step 4: request reading from sensor

  for (int i = 0; i <= byteNum; i++ ) { // repeat iteration for the number of expected bytes
    if (Wire.available()) {
      reading[i] = Wire.read();      // add each new byte into reading array then increment the array
    }
  }


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
float getAverageNum(float bArray[], uint8_t iFilterLen) 
{
  uint8_t i = 0;
  double bTemp = 0;
  for(i = 0; i < iFilterLen; i++) {
    bTemp += bArray[i];
  }
  return bTemp / (float)iFilterLen;
}
