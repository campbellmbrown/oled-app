#include "led.h"
#include "oled.h"
#include "serial_protocol.h"

#include <Arduino.h>
#include <Wire.h>

void setup(void)
{
  Wire.begin();
  Serial.begin(115200);
  led_set_color(COLOR_GREEN);
  oled_init();
}

void loop(void)
{
  serial_protocol_process();
  delay(1);
}
