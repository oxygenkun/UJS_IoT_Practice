bool powerValue;
String inputString;
int ledPin = 2; 
void setup() {
  // initialize equipment's properties
  powerValue = 0;
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
  inputString = Serial.readString();
  if (inputString.startsWith("PS:") ) {
    powerSet(inputString);
  }
  else
    errorReport("Wrong Command!");
}

/*

*/
void powerSet(String inputString) {
  int val = inputString.charAt(3) - '0';
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
