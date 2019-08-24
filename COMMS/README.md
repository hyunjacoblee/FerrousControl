# FerrousControl
Ferrofluid controlled through an electromagnetic array

## COMMS
Requirements:
- Python 3.6.2
- PySerial
- [Robust Serial Library](https://github.com/araffin/arduino-robust-serial)

## ARDUINO
Requirements:
- [Teensyduino](https://www.pjrc.com/teensy/teensyduino.html)

Both current design codes, just spit out what they received on the serial line to the LCD.  LCD output may need to change to some status message, or timing measure, or some other feedback that might be more useful. Current design is to send to five (5) separate Teensies each tasked with communicating to five (5) Arduino boards for a total of 25 boards. The hub layout on the newhumans Mac Mini is two Teensies each on the USB-C hubs and one on a USB-A 3.0 port

### TO DO
- Test timing with a full 1600 values of information
- Test with increase packet size (Arduino has a default of 64 bytes, Teensy 512 bytes)
- NOTE: Increased Arduino serial buffer defaults is possible as done below:
- [Serial buffer increase](http://www.hobbytronics.co.uk/arduino-serial-buffer-size)
- On newhumans Mac Mini, there has been added 256, 320, and 512 serial buffer increase options, but the above serial buffer increase directions must be followed for any other installation of Arduino and it is highly discouraged to use above 256 bytes for the serial buffer
- Troubleshoot/Fix the RS485 communications between the Teensy and Arduino

### Resources
- [USB Serial Communication](https://www.pjrc.com/teensy/td_serial.html)
- [Serial Benchmark](https://www.pjrc.com/teensy/benchmark_usb_serial_receive.html)
