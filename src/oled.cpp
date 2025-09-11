#include "oled.h"

#include <U8g2lib.h>

static U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* clock */ SCL, /* data */ SDA, /* reset */ U8X8_PIN_NONE);

void oled_init()
{
    u8g2.begin();
    u8g2.clearBuffer();
    u8g2.setFont(u8g2_font_ncenB12_tr);
}

oled_set_image_ret_t oled_set_image(const uint8_t *image_data, size_t length)
{
    if (length != OLED_BUFFER_SIZE)
    {
        return OLED_SET_IMAGE_INVALID_LENGTH;
    }
    u8g2.drawXBMP(0, 0, OLED_WIDTH, OLED_HEIGHT, image_data);
    u8g2.sendBuffer();
    return OLED_SET_IMAGE_SUCCESS;
}
