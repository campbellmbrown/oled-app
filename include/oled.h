#ifndef OLED_H
#define OLED_H

#include <stdint.h>
#include <stddef.h>

#define OLED_WIDTH (128)
#define OLED_HEIGHT (64)
#define OLED_PIXELS (OLED_WIDTH * OLED_HEIGHT)
#define OLED_PIXELS_PER_BYTE (8)
#define OLED_BUFFER_SIZE (OLED_PIXELS / OLED_PIXELS_PER_BYTE)

typedef enum
{
    OLED_SET_IMAGE_SUCCESS,
    OLED_SET_IMAGE_INVALID_LENGTH,
} oled_set_image_ret_t;

void oled_init();
oled_set_image_ret_t oled_set_image(const uint8_t *image_data, size_t length);

#endif // OLED_H
