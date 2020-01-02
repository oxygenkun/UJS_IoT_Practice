#include <ArduinoJson.h>
#include "DHT.h"
#define LEDPIN  2
#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
bool powerValue;
String inputString;
DynamicJsonDocument inputJson(200);


void setup() {
  // initialize equipment's properties
  powerValue = 0;

  // initialize
  Serial.begin(9600);
  dht.begin();
  
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {
  digitalWrite(LEDPIN, powerValue);
  
  delay(1000);
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
  else if (cmd == "ps") {
    long val = inputJson["par"];
    powerSet(val);
  }
  else if (cmd == "dht") {
    readTempAndHumi();
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
    String stringOne = F("Power set: ");
    String stringTwo = stringOne + powerValue;
    Serial.println(stringTwo);
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
  dataJson["humi"] = h;
  dataJson["temp"] = t;
  returnJson["data"] = dataJson;
  serializeJson(returnJson, Serial);
}

/*
    ERROR report
*/
void errorReport(String err) {
  String stringOne = "ERROR:";
  String stringTwo = stringOne + err;
  Serial.println(stringTwo);
}
