/*
  

*/

#define VERSION 3.20
#define DATA_DIR_PIN_1  2
#define DATA_DIR_PIN_2  6
#define DATA_DIR_PIN_3  11
#define DATA_DIR_PIN_4  30
#define DATA_DIR_PIN_5  35

#define RS485_TRANSMIT  HIGH
#define RS485_RECEIVE   LOW

#define TEENSY_SEGMENT  0

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 36, en = 37, d4 = 38, d5 = 39, d6 = 14, d7 = 15;

const uint16_t packetSize = 320;
uint8_t byteBuffer[packetSize];
uint32_t packetCount = 0;
uint32_t byteCount = 0;
uint16_t checksum = 0;

uint8_t checkByte = 0;

void setup() {
  Serial.begin(1000000);
  Serial1.begin(250000);
  //  Serial1.begin(1000000);


  pinMode(DATA_DIR_PIN_1, OUTPUT);
  digitalWrite(DATA_DIR_PIN_1, RS485_TRANSMIT);
  pinMode(DATA_DIR_PIN_2, OUTPUT);
  digitalWrite(DATA_DIR_PIN_2, RS485_TRANSMIT);
  pinMode(DATA_DIR_PIN_3, OUTPUT);
  digitalWrite(DATA_DIR_PIN_3, RS485_TRANSMIT);
  pinMode(DATA_DIR_PIN_4, OUTPUT);
  digitalWrite(DATA_DIR_PIN_4, RS485_TRANSMIT);
  pinMode(DATA_DIR_PIN_5, OUTPUT);
  digitalWrite(DATA_DIR_PIN_5, RS485_TRANSMIT);
}

void loop() {

  if (Serial.available()) {
    // wait a bit for the entire message to arrive
    //    delay(24);
    while (Serial.available() > 0) {
      uint8_t inByte = Serial.read();

      if (inByte == 255) {
        Serial1.write(byteBuffer, 320);
        Serial1.write(255);
        Serial1.flush(); // block until sent
        byteCount = 0;
      }

      else if (byteCount < packetSize)
      {
        if (inByte > 127) {
          inByte = 127;
        }
        else if (inByte < 0) {
          inByte = 0;
        }

        byteBuffer[byteCount] = inByte;
        ++byteCount;
      }
    }
  }
}
