#include <Wire.h>


//************************** Global Variables *****************************//
// Slave Addresses:
int humidityAddr = 39; // temperature humidity address (0x27)
int unoAddr = 8; // temperature humidity address (0x08)

// chain sampling periods
int humidityT[2] = {2, 8}; // timing characteristics: {measure request - read request, resampling period}
int unoT[2] = {0, 5};

// reading variables
int reading1; // humidity reading
int reading2; // temperature reading

//************************** MAIN CODE *****************************//
void setup() {
  Serial.begin(9600);
  Wire.begin(); // Initialize ardiono as master
}

void loop() {
  slaveSample(true, humidityAddr, 4, false, humidityT);
  slaveSample(false, unoAddr, 6, true, unoT);
}



//************************** SLAVE CALLING FUNCTION *****************************//
void slaveSample(bool command, int slavAddr, int byteNum, bool isStream, int timing[]) {
  if (command) {

    slaveCommand(slavAddr, byte(0x00)); // step 1: instruct sensor to measure
    delay(timing[0]);                   // step 2: wait for readings to happen
    slaveCommand(slavAddr, byte(0x01)); // step 3: instruct sensor to return a particular echo reading
  }

  Wire.requestFrom(slavAddr, byteNum);  // step 4: request reading from sensor
  

  while (Wire.available()) {            // step 5: receive reading from sensor
    if (isStream) {
      char c = Wire.read(); // receive a byte as character
      Serial.print(c);      // print the character
    }
    else {
      reading1 = read2Bytes();
      reading2 = read2Bytes();
    }
  }
  if (!isStream) {
    float humidity = (((float)(reading1 & 0x3FFF) / (16384 - 2)) * 100);
    float temp = (((float)(reading2 & 0x3FFF)) / (16384 - 2)) * 100 - 40;
    Serial.print("humidity(%RH) "); Serial.println( humidity);  // print the reading
    Serial.print("temp(C) "); Serial.println(temp);  // print the reading
  }
  else{
    Serial.println("");
  }
  delay(timing[1]);                  // wait a bit since people have to read the output :)

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
  wrd = wrd << 8;    // shift high byte to be high 8 bits
  wrd |= Wire.read(); // receive low byte as lower 8 bits
  return wrd;
}
