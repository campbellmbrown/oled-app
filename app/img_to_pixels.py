from PySide6.QtGui import QImage

from app import oled
from app.image_settings import ImageSettings


def img_to_pixels(image_path: str, image_settings: ImageSettings) -> bytearray:
    image = QImage(image_path).convertToFormat(QImage.Format.Format_Grayscale8)
    if image_settings.invert:
        image.invertPixels()

    assert image.width() == oled.WIDTH
    assert image.height() == oled.HEIGHT

    byte_array = bytearray()

    for y in range(image.height()):
        byte = 0
        for x in range(image.width()):
            pixel = image.pixelColor(x, y).value()  # 0-255 grayscale
            bit = 1 if pixel < image_settings.threshold else 0
            byte = (byte << 1) | bit
            if (x + 1) % 8 == 0:
                swapped_byte = int(f"{byte:08b}"[::-1], 2)  # optional bit reversal
                byte_array.append(swapped_byte)
                byte = 0

    return byte_array
