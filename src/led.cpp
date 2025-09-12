#include "led.h"

#include <Arduino.h>

#define LED_ON (LOW)
#define LED_OFF (HIGH)

void led_set_color(color_t color)
{
    switch (color)
    {
    case COLOR_RED:
        digitalWrite(LED_RED, LED_ON);
        digitalWrite(LED_GREEN, LED_OFF);
        digitalWrite(LED_BLUE, LED_OFF);
        break;
    case COLOR_GREEN:
        digitalWrite(LED_RED, LED_OFF);
        digitalWrite(LED_GREEN, LED_ON);
        digitalWrite(LED_BLUE, LED_OFF);
        break;
    case COLOR_BLUE:
        digitalWrite(LED_RED, LED_OFF);
        digitalWrite(LED_GREEN, LED_OFF);
        digitalWrite(LED_BLUE, LED_ON);
        break;
    case COLOR_YELLOW:
        digitalWrite(LED_RED, LED_ON);
        digitalWrite(LED_GREEN, LED_ON);
        digitalWrite(LED_BLUE, LED_OFF);
        break;
    case COLOR_CYAN:
        digitalWrite(LED_RED, LED_OFF);
        digitalWrite(LED_GREEN, LED_ON);
        digitalWrite(LED_BLUE, LED_ON);
        break;
    case COLOR_MAGENTA:
        digitalWrite(LED_RED, LED_ON);
        digitalWrite(LED_GREEN, LED_OFF);
        digitalWrite(LED_BLUE, LED_ON);
        break;
    case COLOR_WHITE:
        digitalWrite(LED_RED, LED_ON);
        digitalWrite(LED_GREEN, LED_ON);
        digitalWrite(LED_BLUE, LED_ON);
        break;
    case COLOR_OFF:
    default:
        digitalWrite(LED_RED, LED_OFF);
        digitalWrite(LED_GREEN, LED_OFF);
        digitalWrite(LED_BLUE, LED_OFF);
        break;
    }
}
