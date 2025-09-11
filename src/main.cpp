#include "oled_driver.h"

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
  oled_driver_loop();
  delay(1000);
}
