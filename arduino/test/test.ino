#include <ArduinoJson.h>
#include "DHT.h"
#define LEDPIN  2
#define DHTPIN 4
#define DHTTYPE DHT11
#define MTOTRPIN 6

DHT dht(DHTPIN, DHTTYPE);
bool powerValue;
int motorSpeed;

String inputString;
DynamicJsonDocument inputJson(200);

String cmd_ps = "ps";
String cmd_dht = "dht";
String cmd_mot = "mot";

void setup() {
  // initialize equipment's properties
  powerValue = 0;
  motorSpeed = 0;
  // initialize
  Serial.begin(9600);
  dht.begin();

  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {
  digitalWrite(LEDPIN, powerValue);
  analogWrite(MTOTRPIN, motorSpeed);
  delay(30);
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  String inputString = Serial.readString();
  DeserializationError error = deserializeJson(inputJson, inputString);

  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }

  const char* cmd_char = inputJson["cmd"];
  String cmd = String(cmd_char);

  if (cmd == NULL)
    errorReport(F("No Command!"));
  else if (cmd == cmd_ps) {
    long val = inputJson["par"];
    powerSet(val);
  }
  else if (cmd == cmd_dht) {
    readTempAndHumi();
  }
  else if (cmd == cmd_mot) {
    long val = inputJson["par"];
    motorSet(val);
  }
  else
    errorReport(F("Wrong Command!"));
}

/*
   set power
*/
void powerSet(int val) {
  if (val == 0 || val == 1) {
    powerValue = val;

    DynamicJsonDocument returnJson(50);
    returnJson["cmd"] = cmd_ps;
    returnJson["data"] = powerValue;
    String returnString ;
    serializeJson(returnJson, returnString);
    Serial.println(returnString);
  } else
    errorReport("Wrong Power Set Parameters!");
}

/*
   read temperature and humidity
*/
void readTempAndHumi() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again)
  if (isnan(h) || isnan(t)) {
    errorReport(F("Failed to read from DHT sensor!"));
    return;
  }

  DynamicJsonDocument returnJson(50);
  DynamicJsonDocument dataJson(25);
  returnJson["cmd"] = "dht";
  dataJson["Humi"] = h;
  dataJson["Temp"] = t;
  returnJson["data"] = dataJson;
  String returnString ;
  serializeJson(returnJson, returnString);
  Serial.println(returnString);

}

void motorSet(int val) {
  if (val >= 0 && val <= 255)
    motorSpeed = val;
  else if (val < 0)
    motorSpeed = 0;
  else
    motorSpeed = 255;
  DynamicJsonDocument returnJson(50);
  returnJson["cmd"] = cmd_mot;
  returnJson["data"] = motorSpeed;
  String returnString ;
  serializeJson(returnJson, returnString);
  Serial.println(returnString);
}


/*
    ERROR report
*/
void errorReport(String err) {
  String stringOne = F("ERROR:");
  String stringTwo = stringOne + err;
  Serial.println(stringTwo);
}
