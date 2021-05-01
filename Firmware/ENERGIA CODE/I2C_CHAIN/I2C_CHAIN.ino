#include <Wire.h>


//************************** Global Variables *****************************//
// Slave Addresses:
int humidityAddr = 39; // temperature humidity address (0x27)
int unoAddr = 8; // temperature humidity address (0x08)

// chain sampling periods
int humidityT[2] = {10, 100}; // timing characteristics: {measure request - read request, resampling period}
int unoT[2] = {0, 10};

// reading variables
int reading1; // humidity reading
int reading2; // temperature reading
byte reading[10];

//************************** MAIN CODE *****************************//
void setup() {
  Serial.begin(9600);
  Wire.begin(); // Initialize ardiono as master
}

void loop() {
  //********HUMID & TEMP SENSOR********//
  slaveSample(true, humidityAddr, 4, humidityT); //** SAMPLE RAW BYTES FROM SENSOR
  
  //** parse bytes from sensor into two 16-bit words, then convert words into accurate data.
  int humidityWord = (reading[0] << 8) | reading[1];    // shift byte0 up 8 bits and add byte1 to it   
  int tempWord = (reading[2] << 8) | reading[3];        // shift byte2 up 8 bits and add byte3 to it 
  
  float humidity = (((float)(humidityWord & 0x3FFF) / (16384 - 2)) * 100); // mask first two status bits and convert to RH
  float temp = (((float)(tempWord & 0x3FFF)) / (16384 - 2)) * 100 - 40;    // mask first unused bits and convert to (C)
  Serial.print("humidity(%RH) "); Serial.println( humidity);               // print the reading
  Serial.print("temp(C) "); Serial.println(temp);                          // print the reading
  
  //********ARDUINO UNO SPOOF SENSOR********//
  slaveSample(false, unoAddr, 6, unoT);         //** SAMPLE RAW BYTES FROM SENSOR

  //** parse bytes from UNO
   for(int i=0; i<= 6;i++ ){
    Serial.print((char)reading[i]);    // print each byte as a character
   }
   Serial.println("");                 // print new line
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
