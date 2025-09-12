from PySide6.QtGui import QImage, QPixmap

THRESHOLD = 128


def img_to_pixels(pixmap: QPixmap) -> bytearray:
    img = pixmap.toImage().convertToFormat(QImage.Format.Format_Grayscale8)

    width = img.width()
    height = img.height()

    byte_array = bytearray()

    for y in range(height):
        byte = 0
        for x in range(width):
            pixel = img.pixelColor(x, y).value()  # 0-255 grayscale
            bit = 1 if pixel < THRESHOLD else 0
            byte = (byte << 1) | bit
            if (x + 1) % 8 == 0:
                swapped_byte = int(f"{byte:08b}"[::-1], 2)  # optional bit reversal
                byte_array.append(swapped_byte)
                byte = 0

        # leftover pixels at end of row
        leftover = width % 8
        if leftover != 0:
            byte <<= 8 - leftover
            swapped_byte = int(f"{byte:08b}"[::-1], 2)
            byte_array.append(swapped_byte)

    return byte_array
