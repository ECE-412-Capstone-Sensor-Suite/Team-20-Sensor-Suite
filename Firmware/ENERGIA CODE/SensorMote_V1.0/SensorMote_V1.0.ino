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



#include <IpMtWrapper.h>
#include <dn_ipmt.h>
#include <prcm.h>
#include <Wire_CC.h>

IpMtWrapper       ipmtwrapper;


//=======================================  Global Variables  ===============================================//
#define           OXYGEN_DATA_REGISTER      0x03            // Oxygen data register
#define           USER_SET_REGISTER         0x08            // user set key value
#define           AUTUAL_SET_REGISTER       0x09            // autual set key value
#define           GET_KEY_REGISTER          0x0A            // get key value
#define           COLLECT_NUMBER            10              // collect number, the collection range is 1-100.
#define           HUMIDITY_ADDR             0x27            // temperature humidity address (0x27)
#define           OPT_ADDR                  0x44            // OPT3001 light address (0x44)
#define           O2_ADDR                   0x73            // O2 ADDRESS
#define           ADXL_ADDR                 0x53            // O2 ADDRESS
#define           analogPinForRV            0               // change to pins you the analog pins are using
#define           analogPinForTMP           0               // P4_5 
#define           CO2_IN                    6               // CO2 Sensor Input pin
#define           RAIN_INPUT                2               // rain input pin
#define           CC3200_LPDS_CLK           32768           // rain input pin

float  OxygenData[100] = {0.00};
//float key;
static uint8_t i = 0 , j = 0;
uint8_t Reg;
uint8_t pdata;
float _Key = 0.0;                          // oxygen key value
float    ReadOxygenData(uint8_t CollectNum);
float oxygenData;

// chain sampling periods
int humidityT[2] = {10, 5}; // timing characteristics: {WAIT AFTER WRITE 1, WAIT AFTER WRITE2}
int opt3001T[2] = {100, 0};
byte reading[5];            // for I2C reading
float X_out, Y_out, Z_out;  // ADXL Outputs
float humidity;
float temp;
float fLux;
const float zeroWindAdjustment =  0.2; // negative numbers yield smaller wind speeds and vice versa.
float WindSpeed_MPH; int LastPrint;
int rainValue = analogRead(2);        //Rain Sensor Input
float concentration;

//=================================  {Sending data VIA Smartmesh} ============================================//

int sensorData[10] = {0}; // global array to hold all the sensor values
uint8_t MOTESTATE = 1;
bool SENSOR_TRIGGER, SLEEP_TRIGGER = false;
int lastTIME, millisATsend, SleepDuration;
int confirm_num = 9999; //  number used to confrim that smart mesh is sending appropriatly
void generateData(uint16_t* returnVal) { // this is were data is assinged to be sent via mote
  returnVal[0] = (int)(temp * 100);          // payload[1,2] = temp
  returnVal[1] = (int)(humidity * 100);      // payload[3,4] = humidity
  returnVal[2] = (int)(fLux * 100) ;          // payload[5,6] = light sensitivity
  returnVal[3] = (int)(oxygenData * 100) ;    // payload[7,8] = oxygen
  returnVal[4] = (int)(concentration * 100) ; // payload[9,10] = CO2 Concentration
  returnVal[5] = (int)(X_out * 100) ;         // payload[11,12] = Acceloromter C
  returnVal[6] = (int)(Y_out * 100) ;         // payload[13,14] = Acceloromter Y
  returnVal[7] = (int)(Z_out * 100) ;         // payload[15,16] = Acceloromter Z
  returnVal[8] = (int)(WindSpeed_MPH * 100); // payload[17,18] = Windspeed
  returnVal[9] = rainValue;                  // payload[19,20] =
  //memcpy(returnVal, sensorData, sizeof(returnVal)); // assign sensor data array to return val
  Serial.print("\nINFO:          SENT FIRST VALUE:");     Serial.println(returnVal[0]);
  Serial.println("INFO:          SENT LAST VALUE:");      Serial.println(returnVal[9]);

  SLEEP_TRIGGER = true; // set sleep state true after sending value
  millisATsend = millis();
}

//============================================================================================================//
//========================================  {INITIALIZE SENSORS} =============================================//
void setup() {

  ipmtwrapper.setup( // SET UP SMART MESH MOTE
    60000,                            // srcPort
    (uint8_t*)ipv6Addr_manager,       // destAddr
    61000,                            // destPort
    200,                              // dataPeriod (ms)
    generateData                      // dataGenerator
  );

  SleepDuration = 32768 * 3;         // 30 second sleep durtion, 10 minute sleep duration for final deployment
  pinMode(RED_LED, OUTPUT);
  Wire.begin(); // Initialize ardiono as master

  //*************************OPT3001 Light Sensor********************//
  Wire.beginTransmission(0x44);     // I2C address of OPT3001 = 0x44
  Wire.write(0x01);
  Wire.write(0xCE);
  Wire.write(0x10);
  Wire.endTransmission();
  // Set ADXL_ADDR in measuring mode
  Wire.beginTransmission(ADXL_ADDR); // Start communicating with the device
  Wire.write(0x2D); // Access/ talk to POWER_CTL Register - 0x2D
  // Enable measurement
  Wire.write(8); // (8dec -> 0000 1000 binary) Bit D3 High for measuring enable

  Wire.endTransmission();

  //**************************DFR O2 Sensor***************************//
  while (!begin(O2_ADDR)) {
    Serial.println("I2c device number error !");
    delay(1000);
  }
  Serial.println("I2c connect success !");
}

//============================================================================================================//
//==========================================  {MAIN} =========================================================//
void loop() {
  if (SLEEP_TRIGGER && SENSOR_TRIGGER && ((millis() - millisATsend) > 100) ) {        // IF SLEEP and SENSORS have been triggered wait 100ms and then go to sleep
    digitalWrite(RED_LED, LOW);    // turn the LED off by making the voltage LOW
    Serial.println("Entering low-power Deep Sleep");
    delay(25);                                //wait for serial monitor to print
    PRCMLPDSWakeupSourceEnable(0x00000001);   // set timer as sleep mode interrupt
    PRCMLPDSIntervalSet(SleepDuration);       // set sleep mode interval
    PRCMLPDSEnter();
  }
  
  //---------------------------------------------------------------------------------
  ipmtwrapper.loop(&MOTESTATE);                               // SMART MESH STATE MACHINE LOOP, RETURNS MOTE STATE
  //---------------------------------------------------------------------------------
  if ((millis() - lastTIME) > 1000) {
        Serial.println(MOTESTATE);  lastTIME = millis();                             // Print mote state number every second
   }
  
  /* MOTESTATE = MOTE_STATE_OPERATIONAL; //*/       // <-- UNCOMMENET IF YOU WANT SENSOR TO SAMPLE WITHOUT JOINING NETWORK*/
  if (!SENSOR_TRIGGER) {                            // DONT ENTER IF PREIVOUSLY SAMPLED
    int SampleBeginT = millis();
    int CollectingPeriod = 1 * 1000; /// 1 seconds

    while ((MOTESTATE == MOTE_STATE_OPERATIONAL) && ((millis() - SampleBeginT) < CollectingPeriod)) { // GO INTO LOOP AND COLLECT SENSOR SAMPLES
      digitalWrite(RED_LED, HIGH);   // turn the LED on (HIGH is the voltage level)
      SENSOR_TRIGGER = true;
      HUMID_READ();                         // HUMIDITY AND TEMP SENSOR
      Serial.print("SENSOR:                                 Humidity(%RH): "); Serial.println(humidity);       // print the reading
      Serial.print("SENSOR:                                 Temp(C): ");       Serial.println(temp);           // print the reading
      delay(5);         // Wait between readings

      OPT_READ();                           // ARDUINO OPT3001 LIGHT SENSOR
      Serial.print("SENSOR:                                 LUX: ");
      Serial.println(fLux);                           //Print the received data

      ADXL_READ();                          // ACCELOROMETER SENSOR
      Serial.print("SENSOR:                                 Xa= "); Serial.print(X_out);
      Serial.print("   Ya= "); Serial.print(Y_out);  Serial.print("   Za= "); Serial.println(Z_out);

      ReadOxygenData(COLLECT_NUMBER);       // O2 SENSOR
      Serial.print("SENSOR:                                 Oxygen concentration is ");
      Serial.print(oxygenData); Serial.println(" %vol");

      if (millis() - LastPrint > 200) {     // read every 200 ms - printing slows this down further
        WIND_READ();                        // WIND SENSOR
        Serial.print("SENSOR:                                 WindSpeed MPH: "); Serial.println((float)WindSpeed_MPH);
        LastPrint = millis();
      }

      CO2_READ();                           // CO2 SENSOR
      Serial.print("SENSOR:                                 CO2: "); Serial.print(concentration); Serial.println("ppm");

      rainValue = analogRead(2);            //Rain Sensor Input
      Serial.print("SENSOR:                                 Rain Level: "); Serial.println(rainValue);
    }
  }
}

//==========================================  {END OF MAIN} ====================================================//
//============================================================================================================//







//===========================================================================================================//
//========================================  {Sensor Functions} ==============================================//

void HUMID_READ() {
  //********HUMID & TEMP SENSOR********//
  ///slaveSample template:
  //          {ADDRESS, 1ST WRITE, 2ND WRITE, WAIT TIMES , EXPECTED NO. OF  BYTES}
  slaveSample(HUMIDITY_ADDR, byte(0x00), byte(0x01), humidityT, 4); //** SAMPLE RAW BYTES FROM SENSOR

  //** parse bytes from sensor into two 16-bit words, then convert words into accurate data.
  int humidityWord = (reading[0] << 8) | reading[1];    // shift byte0 up 8 bits and add byte1 to it
  int tempWord = (reading[2] << 8) | reading[3];        // shift byte2 up 8 bits and add byte3 to it

  humidity = (((float)(humidityWord & 0x3FFF) / (16384 - 2)) * 100); // mask first two status bits and convert to RH
  temp = (((float)(tempWord & 0x3FFF)) / (16384 - 2)) * 100 - 40;    // mask first unused bits and convert to (C)
}

void OPT_READ() {
  //slaveSample template:
  //         {ADDRESS, 1ST WRITE, byte(0xFF) = DONT WRITE, WAIT TIMES , EXPECTED NO. OF  BYTES}
  slaveSample(OPT_ADDR, byte(0x00), byte(0xFF), opt3001T, 2); //** SAMPLE RAW BYTES FROM SENSOR

  int optWord = (reading[0] << 8) | reading[1];
  uint16_t iExponent, iMantissa;
  iMantissa = optWord & 0x0FFF;                 // Extract Mantissa
  iExponent = (optWord & 0xF000) >> 12;         // Extract Exponent
  fLux = iMantissa * (0.01 * pow(2, iExponent)); // Calculate final LUX
}

void ADXL_READ() {
  // === Read acceleromter data === //
  Wire.beginTransmission(ADXL_ADDR);
  Wire.write(0x32); // Start with register 0x32 (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(ADXL_ADDR, 6, true); // Read 6 registers total, each axis value is stored in 2 registers

  X_out = ( Wire.read() | Wire.read() << 8); // X-axis value
  X_out = X_out / 256; //For a range of +-2g, we need to divide the raw values by 256, according to the datasheet
  Y_out = ( Wire.read() | Wire.read() << 8); // Y-axis value
  Y_out = Y_out / 256;
  Z_out = ( Wire.read() | Wire.read() << 8); // Z-axis value
  Z_out = Z_out / 256;
}

void WIND_READ() {
  int TMP_Therm_ADunits = analogRead(analogPinForTMP);  //temp termistor value from wind sensor
  float RV_Wind_ADunits = analogRead(analogPinForRV);   //RV output from wind sensor
  float RV_Wind_Volts = (RV_Wind_ADunits *  0.0048828125);

  float TempCtimes100 = (0.005 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;

  float zeroWind_ADunits = -0.0006 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172; //  13.0C  553  482.39

  float zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;

  WindSpeed_MPH =  pow(((RV_Wind_Volts - zeroWind_volts) / .2300) , 2.7265);
}

void CO2_READ() {
  //Read voltage
  int CO2_analogRead = analogRead(CO2_IN);
  // The analog signal is converted to a voltage
  float voltage = CO2_analogRead * (3300 / 1024.0);
  if (voltage == 0) {
    Serial.println("Fault");
  }
  else if (voltage < 400) {
    Serial.println("preheating");
  }
  else {
    int voltage_diference = voltage - 400;
    concentration = voltage_diference * 50.0 / 16.0;
  }
}


//===========================================================================================================//
//========================================  {HELPER Functions} ==============================================//
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
//**************************DFR O2 Sensor***************************//
void ReadFlash() {

  uint8_t value = 0;
  Wire.beginTransmission(O2_ADDR);
  Wire.write(GET_KEY_REGISTER);
  Wire.endTransmission();
  delay(50);
  Wire.requestFrom(O2_ADDR, (uint8_t)1);
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
    Wire.beginTransmission(O2_ADDR);
    Wire.write(OXYGEN_DATA_REGISTER);
    Wire.endTransmission();
    delay(100);
    Wire.requestFrom(O2_ADDR, (uint8_t)3);
    while (Wire.available())
      rxbuf[k++] = Wire.read();
    OxygenData[0] = ((_Key) * (((float)rxbuf[0]) + ((float)rxbuf[1] / 10.0) + ((float)rxbuf[2] / 100.0)));
    if (i < CollectNum) i++;
    oxygenData = getAverageNum(OxygenData, i);
  } else {
    oxygenData = -1.0;
  }
}

/* Write data to the i2c register  */
void i2cWrite(uint8_t Reg , uint8_t pdata)
{
  Wire.beginTransmission(O2_ADDR);
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
  Wire.beginTransmission(addr);
  Wire.write(1);
  if (Wire.endTransmission() == 0) {
    return true;
  }
  return false;
}
