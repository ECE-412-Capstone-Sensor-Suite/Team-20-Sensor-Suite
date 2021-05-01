

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


///////////////////////SMART MESH CLIB//////////////////////////////////////
// Additional single line code in SETUP and LOOP portions of code
#include <IpMtWrapper.h>
#include <dn_ipmt.h>
#include <Wire_CC.h>

IpMtWrapper       ipmtwrapper;
int arbitraryData; // this is the number used to test data sending via mote



//********************************** O2 Configuration *********************//
#define           OXYGEN_DATA_REGISTER      0x03           // Oxygen data register
#define           USER_SET_REGISTER         0x08           // user set key value
#define           AUTUAL_SET_REGISTER       0x09           // autual set key value
#define           GET_KEY_REGISTER          0x0A           // get key value
#define COLLECT_NUMBER    10             // collect number, the collection range is 1-100.

int O2addr = byte(0x73);
float  OxygenData[100] = {0.00};
//float key;
static uint8_t i = 0 , j = 0;
uint8_t Reg;
uint8_t pdata;
float _Key = 0.0;                          // oxygen key value
float    ReadOxygenData(uint8_t CollectNum);
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
int adxl345T[2] = {10, 0};

// reading variables
int reading1; // humidity reading
int reading2; // temperature reading
byte reading[32];
//***************************CO2*************************************//
int sensorIn = 6;//P4_0; // CO2 Sensor Input

//*******************ADXL Sensor ************************************//
float X_out, Y_out, Z_out;  // Outputs

//*****************************Wind Speed Sensor*******************//

#define analogPinForRV    0//P4_2   // change to pins you the analog pins are using
#define analogPinForTMP   0//P4_5

// to calibrate your sensor, put a glass over it, but the sensor should not be
// touching the desktop surface however.
// adjust the zeroWindAdjustment until your sensor reads about zero with the glass over it.

const float zeroWindAdjustment =  0.2; // negative numbers yield smaller wind speeds and vice versa.

int TMP_Therm_ADunits;  //temp termistor value from wind sensor
float RV_Wind_ADunits;    //RV output from wind sensor
float RV_Wind_Volts;
unsigned long lastMillis;
int TempCtimes100;
float zeroWind_ADunits;
float zeroWind_volts;
float WindSpeed_MPH;

//******************************Rain Sensor**********************************//
int sensorValue = analogRead(2); //P4_7); //Rain Sensor Input

//============================================================================================================//
//========================================  {INITIALIZE SENSORS} =============================================//
void setup() {

  pinMode(7, OUTPUT);

  Serial.begin(9600);

  //Serial.begin(9600);
  Serial.println("before");
  Wire.begin(); // Initialize ardiono as master
  Serial.println("After");
  //*************************OPT3001 Light Sensor********************//*
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
  while (!begin(O2addr)) {
    Serial.println("I2c device number error !");
    delay(1000);
  }
  Serial.println("I2c connect success !");
  
  ipmtwrapper.setup( // SET UP SMART MESH MOTE

    60000,                           // srcPort
    (uint8_t*)ipv6Addr_manager,      // destAddr
    61000,                           // destPort
    10000,                           // dataPeriod (ms)
    generateData                     // dataGenerator
  );
}
//============================================================================================================//
//==========================================  {MAIN LOOP} ====================================================//
void loop() {
  


  //digitalWrite(7, LOW);
  //********HUMID & TEMP SENSOR********//
  ///slaveSample template:
  //          {ADDRESS, 1ST WRITE, 2ND WRITE, WAIT TIMES , EXPECTED NO. OF  BYTES}
  slaveSample(humidityAddr, byte(0x00), byte(0x01), humidityT, 4); //** SAMPLE RAW BYTES FROM SENSOR

  //** parse bytes from sensor into two 16-bit words, then convert words into accurate data.
  int humidityWord = (reading[0] << 8) | reading[1];    // shift byte0 up 8 bits and add byte1 to it
  int tempWord = (reading[2] << 8) | reading[3];        // shift byte2 up 8 bits and add byte3 to it

  float humidity = (((float)(humidityWord & 0x3FFF) / (16384 - 2)) * 100); // mask first two status bits and convert to RH
  float temp = (((float)(tempWord & 0x3FFF)) / (16384 - 2)) * 100 - 40;    // mask first unused bits and convert to (C)
  Serial.print("\nSENSOR:                                       Humidity(%RH): "); Serial.println( humidity);               // print the reading
  Serial.print("SENSOR:                                       Temp(C): "); Serial.println(temp);                          // print the reading


  //********ARDUINO OPT3001 Light SENSOR********//
  //slaveSample template:
  //         {ADDRESS, 1ST WRITE, byte(0xFF) = DONT WRITE, WAIT TIMES , EXPECTED NO. OF  BYTES}
  slaveSample(optAddr, byte(0x00), byte(0xFF), opt3001T, 2); //** SAMPLE RAW BYTES FROM SENSOR
  /// inputting byte(0xFF) into a write word means you dont want to write any words

  int optWord = (reading[0] << 8) | reading[1];
  Serial.print("SENSOR:                                       LUX: ");                          //
  float fLux = SensorOpt3001_convert(optWord);    // Calculate LUX from sensor data
  Serial.println(fLux);                           //Print the received data

  //********ADXL345 Acceleramoter Sensor*********//
  // === Read acceleromter data === //
  Wire.beginTransmission(adxl345);
  Wire.write(0x32); // Start with register 0x32 (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(adxl345, 6, true); // Read 6 registers total, each axis value is stored in 2 registers

  X_out = ( Wire.read() | Wire.read() << 8); // X-axis value
  X_out = X_out / 256; //For a range of +-2g, we need to divide the raw values by 256, according to the datasheet
  Y_out = ( Wire.read() | Wire.read() << 8); // Y-axis value
  Y_out = Y_out / 256;
  Z_out = ( Wire.read() | Wire.read() << 8); // Z-axis value
  Z_out = Z_out / 256;
  
    Serial.print("SENSOR:                                       Xa= ");
    Serial.print(X_out);
    Serial.print("   Ya= ");
    Serial.print(Y_out);
    Serial.print("   Za= ");
    Serial.println(Z_out);

  //**************************DFR O2 Sensor***************************//
  float oxygenData = ReadOxygenData(COLLECT_NUMBER);
  Serial.print("SENSOR:                                       O2 concentration: ");
  Serial.print(oxygenData);
  Serial.println(" %vol");

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
    //Serial.println((float)RV_Wind_Volts);

    //  Serial.print("\t  TempC*100 ");
    //  Serial.print(TempCtimes100 );

    // Serial.print("   ZeroWind volts ");
    // Serial.print(zeroWind_volts);

    Serial.print("SENSOR:                                       WindSpeed MPH: ");
    Serial.println((float)WindSpeed_MPH);
    //lastMillis = millis();
  }

  //**************************DFR CO2 Sensor**************************//
  //Read voltage
  int sensorValue = analogRead(sensorIn);

  // The analog signal is converted to a voltage
  float voltage = sensorValue * (3300 / 1024.0);
  if (voltage == 0)
  {
    Serial.println("SENSOR:                                       Fault");
  }
  else if (voltage < 400)
  {
    Serial.println("SENSOR:                                       preheating");
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
     Serial.print("SENSOR:                                       CO2: ");
     Serial.print(concentration);
     Serial.println("ppm");
  }



  //******************************Rain Sensor**********************************//
  // read the input on analog pin 3:

  //Serial.print("Rain Level: ");
  //Serial.println(sensorValue);
  digitalWrite(7, LOW);
  ipmtwrapper.loop(); // SMART MESH LOOP
}

void generateData(uint16_t* returnVal) { // this is were data is assinged to be sent via mote
  arbitraryData = (arbitraryData + 1) % 10;
  returnVal[0] =  arbitraryData;   // return value is a 16 bit per element array to be sent via mote
  returnVal[1] =  arbitraryData * 2;
  returnVal[2] =  arbitraryData * 3;
  returnVal[3] =  arbitraryData * 4;
  returnVal[4] =  arbitraryData * 5;
  returnVal[5] =  arbitraryData * 6;
  returnVal[6] =  arbitraryData * 7;
  returnVal[7] =  arbitraryData * 8;
  returnVal[8] =  arbitraryData * 9;
  returnVal[9] =  arbitraryData * 10;
  Serial.print("INFO:          SENT FIRST VALUE:");     Serial.println(returnVal[0]);
  Serial.println("INFO:          RETURNED LAST VALUE:");  Serial.println(returnVal[9]);
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
//**************************DFR O2 Sensor***************************//
void ReadFlash() {

  uint8_t value = 0;
  Wire.beginTransmission(O2addr);
  Wire.write(GET_KEY_REGISTER);
  Wire.endTransmission();
  delay(50);
  Wire.requestFrom(O2addr, (uint8_t)1);
  while (Wire.available())
    value = Wire.read();
  if (value == 0) {
    _Key = 20.9 / 120.0;
  } else {
    _Key = (float)value / 1000.0;
  }
}

/* Reading oxygen concentration */
float ReadOxygenData(uint8_t CollectNum)
{
  uint8_t rxbuf[10] = {0}, k = 0;
  static uint8_t i = 0 , j = 0;
  ReadFlash();
  if (CollectNum > 0) {
    for (j = CollectNum - 1;  j > 0; j--) {
      OxygenData[j] = OxygenData[j - 1];
    }
    Wire.beginTransmission(O2addr);
    Wire.write(OXYGEN_DATA_REGISTER);
    Wire.endTransmission();
    delay(100);
    Wire.requestFrom(O2addr, (uint8_t)3);
    while (Wire.available())
      rxbuf[k++] = Wire.read();
    OxygenData[0] = ((_Key) * (((float)rxbuf[0]) + ((float)rxbuf[1] / 10.0) + ((float)rxbuf[2] / 100.0)));
    if (i < CollectNum) i++;
    return getAverageNum(OxygenData, i);
  } else {
    return -1.0;
  }
}

/* Write data to the i2c register  */
void i2cWrite(uint8_t Reg , uint8_t pdata)
{
  Wire.beginTransmission(O2addr);
  Wire.write(Reg);
  Wire.write(pdata);
  Wire.endTransmission();
}

/* Get the average data */
float getAverageNum(float bArray[], uint8_t iFilterLen)
{
  uint8_t i = 0;
  double bTemp = 0;
  for (i = 0; i < iFilterLen; i++) {
    bTemp += bArray[i];
  }
  return bTemp / (float)iFilterLen;
}
/* join i2c bus (address optional for master) */
bool begin(uint8_t addr)
{
  O2addr = addr;              // Set the host address
  Wire.begin();                     // connecting the i2c bus
  Wire.beginTransmission(O2addr);
  Wire.write(1);
  if (Wire.endTransmission() == 0) {
    return true;
  }
  return false;
}
