#include <ArduinoJson.h>
bool powerValue;
int ledPin = 2;
String inputString;
DynamicJsonDocument inputJson(200);
DynamicJsonDocument propertiesJson(200);

void setup() {
  // initialize equipment's properties
  powerValue = 0;
  propertiesJson["powerValue"] = powerValue;

  // initialize serial:
  Serial.begin(9600);

  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {
  digitalWrite(ledPin, powerValue);
  delay(1000);
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  String inputString = Serial.readString();
  Serial.println(inputString);
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
    errorReport("Wrong Command!");
  else
    if(cmd == "ps"){
      Serial.println(cmd);
      long val = inputJson["par"];
      powerSet(val);
    }
}

/*

*/
void powerSet(int val) {
  if (val == 0 || val == 1) {
    powerValue = val;
    String stringOne = "Power set: ";
    String stringTwo = stringOne + powerValue;
    Serial.println(stringTwo);
  } else
    errorReport("Wrong Power Set Parameters!");
}

/*
    ERROR report
*/
void errorReport(String err) {
  String stringOne = "ERROR:";
  String stringTwo = stringOne + err;
  Serial.println(stringTwo);
}
