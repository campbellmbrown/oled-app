from PySide6.QtGui import QImage, QTransform

from app import oled
from app.image_settings import ImageSettings


def adjust_pixel(pixel: int, image_settings: ImageSettings) -> int:
    brightness = -image_settings.brightness if image_settings.invert else image_settings.brightness
    pixel = int((pixel - 128) * (1 + image_settings.contrast) + 128 + brightness)
    return max(0, min(255, pixel))  # clamp to [0, 255]


def dither_pixel(pixel: int, x: int, y: int) -> int:
    # 4x4 Bayer matrix (values scaled 0-15)
    bayer4 = [
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5],
    ]

    # choose matrix cell
    threshold_map_value = bayer4[y % 4][x % 4]

    # scale Bayer value (0-15) to 0-255
    bayer_threshold = (threshold_map_value + 0.5) * (255 / 16)

    return 1 if pixel < bayer_threshold else 0


def img_to_pixels(image_path: str, image_settings: ImageSettings) -> bytearray:
    image = QImage(image_path).convertToFormat(QImage.Format.Format_Grayscale8)
    if image_settings.invert:
        image.invertPixels()

    if image.width() == oled.HEIGHT:
        # Image is rotated 90 degrees. Let's fix that.
        image = image.transformed(QTransform().rotate(90))

    assert image.width() == oled.WIDTH
    assert image.height() == oled.HEIGHT
    byte_array = bytearray()

    for y in range(image.height()):
        byte = 0
        for x in range(image.width()):
            pixel = image.pixelColor(x, y).value()  # 0-255 grayscale
            pixel = adjust_pixel(pixel, image_settings)
            bit = dither_pixel(pixel, x, y)
            byte = (byte << 1) | bit
            if (x + 1) % 8 == 0:
                # Bit reversal for correct display orientation
                swapped_byte = int(f"{byte:08b}"[::-1], 2)
                byte_array.append(swapped_byte)
                byte = 0

    return byte_array
