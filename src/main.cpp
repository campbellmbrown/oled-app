#include "oled_driver.h"
#include "serial_protocol.h"

#include <Arduino.h>
#include <Wire.h>

void setup(void)
{
  Wire.begin();
  Serial.begin(9600);

  oled_driver_init();
}

void loop(void)
{
  serial_protocol_process();
  delay(1);
}
