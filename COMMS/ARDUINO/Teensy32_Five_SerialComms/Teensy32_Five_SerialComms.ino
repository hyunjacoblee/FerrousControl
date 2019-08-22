/*
  LiquidCrystal Library - Hello World

  Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
  library works with all LCD displays that are compatible with the
  Hitachi HD44780 driver. There are many of them out there, and you
  can usually tell them by the 16-pin interface.

  This sketch prints "Hello World!" to the LCD
  and shows the time.

  The circuit:
   LCD RS pin to digital pin 12
   LCD Enable pin to digital pin 11
   LCD D4 pin to digital pin 5
   LCD D5 pin to digital pin 4
   LCD D6 pin to digital pin 3
   LCD D7 pin to digital pin 2
   LCD R/W pin to ground
   LCD VSS pin to ground
   LCD VCC pin to 5V
   10K resistor:
   ends to +5V and ground
   wiper to LCD VO pin (pin 3)

  Library originally added 18 Apr 2008
  by David A. Mellis
  library modified 5 Jul 2009
  by Limor Fried (http://www.ladyada.net)
  example added 9 Jul 2009
  by Tom Igoe
  modified 22 Nov 2010
  by Tom Igoe
  modified 7 Nov 2016
  by Arturo Guadalupi

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/LiquidCrystalHelloWorld

*/

// include the library code:
#include <LiquidCrystal.h>

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
//int byteBuffer[packetSize];
//int buffer_1[320];
//int buffer_2[320];
//int buffer_3[320];
//int buffer_4[320];
//int buffer_5[320];
uint32_t packetCount = 0;
uint32_t byteCount = 0;
uint16_t checksum = 0;

uint8_t checkByte = 0;

//LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(1000000);
  Serial1.begin(115200);
  //  Serial1.begin(1000000);
  //  Serial2.begin(115200);
  //  Serial3.begin(115200);
  //  Serial4.begin(115200);
  //  Serial5.begin(115200);

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
  //lcd.setCursor(4,0);
  uint8_t charIndex = 4;
  uint8_t rowIndex = 0;
  if (Serial.available()) {
    // wait a bit for the entire message to arrive
    delay(24);
    while (Serial.available() > 0) {
      uint8_t inByte = Serial.read();

      if (inByte == 255) {
        Serial1.write(byteBuffer, 320);
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
