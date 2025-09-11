#include "oled_driver.h"

#include <U8g2lib.h>

static U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* clock=*/ SCL, /* data=*/ SDA, /* reset=*/ U8X8_PIN_NONE);

#define OLED_WIDTH           (128)
#define OLED_HEIGHT          (64)
#define OLED_PIXELS          (OLED_WIDTH * OLED_HEIGHT)
#define OLED_PIXELS_PER_BYTE (8)
#define OLED_BUFFER_SIZE     (OLED_PIXELS / OLED_PIXELS_PER_BYTE)

static uint8_t my_image[OLED_BUFFER_SIZE] PROGMEM = { 0x00 };

void oled_driver_init()
{
    u8g2.begin();
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_ncenB12_tr);
}

static int byte_index = 0;

void oled_driver_loop()
{
    my_image[byte_index] = 0x00;
    byte_index = (byte_index + 1) % OLED_BUFFER_SIZE;
    my_image[byte_index] |= 0xFF;

    u8g2.drawXBMP(0, 0, 128, 64, my_image);
    u8g2.sendBuffer();
}
