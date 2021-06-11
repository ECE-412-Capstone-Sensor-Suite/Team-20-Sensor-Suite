
#define analogPinForRV 1 // change to pins you the analog pins are using
#define analogPinForTMP 0
const float zeroWindAdjustment = .2; // negative numbers yield smaller wind speeds and vice versa.
int TMP_Therm_ADunits;               //temp termistor value from wind sensor
float RV_Wind_ADunits;               //RV output from wind sensor
float RV_Wind_Volts;
unsigned long lastMillis;
int TempCtimes100;
float zeroWind_ADunits;
float zeroWind_volts;
float WindSpeed_MPH;

float maxWindSpeed = 50.00; // <---------------------- ieraksti maximālo vēju ātrumu ar komatu piem: 63.55, 50.0;
int speed_ = 0;
int highestValue = 0;
bool newHighValue = true;
int slowDownValue = 1;
int lowestSpeedValue = 1;

// ----------- //

unsigned long lastMillis_readSensor;
unsigned long lastMillis_checkHiVal;
unsigned long lastMillis_buildNewSpeed;
unsigned long lastMillis_spinningFans;

int sensorValue = 0;
int currentValue = 0;
int minimalValue = 1;              // treshol value so smal curent changes dosn't start SetUpNewSpeed(); function
float timeToBuildUpNewSpeed = 2.5; // change this value to increase the time, so the fans can reach the highes sensor value
bool newhigGestValue = false;
bool firstFrameSetupSpeed = false;
bool fansAreSpinning = false;

void setup()
{
    Serial.begin(57600);
    Serial.println("start");

    // ----------- //

    pinMode(A2, INPUT);    // GND pin
    pinMode(A3, INPUT);    // VCC pin
    digitalWrite(A3, LOW); // turn off pullups
}

void loop()
{
    ReadSensor();
    CheckHighestValue();
    if (newhigGestValue)
    {
        SetupNewSpeed();
    }
    if (fansAreSpinning)
    {
        SpinningFans();
    }
}

void SpinningFans()
{
    if (millis() - lastMillis_spinningFans > 3000)
    {
        fansAreSpinning = false;
        currentValue = 0;
        analogWrite(9, currentValue);
        Serial.println("stop");
    }
}

void SetupNewSpeed()
{
    // functions Setup
    if (firstFrameSetupSpeed)
    {
        Serial.println("firstFrameSetupSpeed");
        lastMillis_buildNewSpeed = millis();
        firstFrameSetupSpeed = false;
        newhigGestValue = false;
        analogWrite(9, currentValue);
    }

    // time to finish building up the new speed
    if (millis() - lastMillis_buildNewSpeed > 2500)
    {
        highestValue = false;
        fansAreSpinning = true;
        lastMillis_spinningFans = millis();
    }
}

void CheckHighestValue()
{
    if (sensorValue > highestValue)
    {
        highestValue = sensorValue;
    }

    // register if ther's a new higest value in 1000 milliseconds
    if (millis() - lastMillis_checkHiVal > 1000)
    {
        if (highestValue > minimalValue)
        {
            newhigGestValue = true;
            firstFrameSetupSpeed = true;
            currentValue = highestValue;
            Serial.println("new REAL highestValue: " + sensorValue);
        }else
        {
            newhigGestValue=false;
        }
        
        lastMillis_checkHiVal = millis();
    }
}

void ReadSensor()
{
    if (millis() - lastMillis_readSensor > 200)
    {
        lastMillis_readSensor = millis();

        TMP_Therm_ADunits = analogRead(analogPinForTMP);
        RV_Wind_ADunits = analogRead(analogPinForRV);
        RV_Wind_Volts = (RV_Wind_ADunits * 0.0048828125);
        TempCtimes100 = (0.005 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;
        zeroWind_ADunits = -0.0006 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172; //  13.0C  553  482.39
        zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;
        WindSpeed_MPH = pow(((RV_Wind_Volts - zeroWind_volts) / .2300), 2.7265);

        sensorValue = map(WindSpeed_MPH, 0, maxWindSpeed, 0, 255);
        sensorValue = constrain(sensorValue, 0, 255);
        Serial.println(sensorValue);
        //PrintStuff();

        lastMillis_readSensor = millis();
    }
}

void PrintStuff()
{
    Serial.print("  TMP volts ");
    Serial.print(TMP_Therm_ADunits * 0.0048828125);
    Serial.print(" RV volts ");
    Serial.print((float)RV_Wind_Volts);
    Serial.print("\t  TempC*100 ");
    Serial.print(TempCtimes100);
    Serial.print("   ZeroWind volts ");
    Serial.print(zeroWind_volts);
    Serial.print("   WindSpeed MPH ");
    Serial.println((float)WindSpeed_MPH);
}
