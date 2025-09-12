#ifndef LED_H
#define LED_H

typedef enum
{
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_YELLOW,
    COLOR_CYAN,
    COLOR_MAGENTA,
    COLOR_WHITE,
    COLOR_OFF,
} color_t;

void led_set_color(color_t color);

#endif // LED_H
