/*
  Dual Servo Gate Control System
  Controls two servo motors for Hostel and Library gates
  
  Hardware Connections:
  - Hostel Gate Servo Signal -> Pin 9
  - Library Gate Servo Signal -> Pin 10
  - Both Servos GND -> Arduino GND
  - Both Servos VCC -> 5V (external power recommended)
  
  Serial Commands:
  - "OPEN_HOSTEL" -> Opens hostel gate for 10 seconds
  - "OPEN_LIBRARY" -> Opens library gate for 10 seconds
*/

#include <Servo.h>

// Pin Definitions
const int HOSTEL_SERVO_PIN = 9;
const int LIBRARY_SERVO_PIN = 10;

// Servo Objects
Servo hostelGate;
Servo libraryGate;

// Gate Positions (in degrees)
const int GATE_CLOSED = 0;
const int GATE_OPEN = 90;

// Timing
const unsigned long GATE_OPEN_DURATION = 10000; // 10 seconds in milliseconds

void setup() {
  Serial.begin(9600);
  
  // Attach servos to pins
  hostelGate.attach(HOSTEL_SERVO_PIN);
  libraryGate.attach(LIBRARY_SERVO_PIN);
  
  // Initialize both gates to closed position
  hostelGate.write(GATE_CLOSED);
  libraryGate.write(GATE_CLOSED);
  
  Serial.println("Dual Servo Gate Control System Ready");
  Serial.println("Commands: OPEN_HOSTEL, OPEN_LIBRARY");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove whitespace and newline characters
    
    if (command == "OPEN_HOSTEL") {
      openHostelGate();
    } 
    else if (command == "OPEN_LIBRARY") {
      openLibraryGate();
    }
    else {
      Serial.println("Unknown command: " + command);
    }
  }
}

void openHostelGate() {
  Serial.println("Opening Hostel Gate...");
  hostelGate.write(GATE_OPEN);
  Serial.println("Hostel Gate OPEN");
  delay(GATE_OPEN_DURATION);
  hostelGate.write(GATE_CLOSED);
  Serial.println("Hostel Gate CLOSED");
}

void openLibraryGate() {
  Serial.println("Opening Library Gate...");
  libraryGate.write(GATE_OPEN);
  Serial.println("Library Gate OPEN");
  delay(GATE_OPEN_DURATION);
  libraryGate.write(GATE_CLOSED);
  Serial.println("Library Gate CLOSED");
}