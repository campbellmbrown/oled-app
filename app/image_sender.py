import logging

import serial
from PySide6.QtGui import QPixmap

from app.img_to_pixels import img_to_pixels
from app.protocol import create_packet


def send_image(image_path: str, serial_port: str) -> None:
    """Send an image to the device over the specified serial port."""

    logging.info(f"Sending image {image_path} to port {serial_port}")
    pixmap = QPixmap(image_path)
    payload = img_to_pixels(pixmap)
    packet = create_packet(payload)

    try:
        ser = serial.Serial(serial_port, baudrate=115200, timeout=2)
        if not ser.is_open:
            ser.open()

        ser.write(packet)
        ser.flush()
        ser.close()
        logging.info("Packet sent to device.")
    except serial.SerialException as e:
        logging.error(f"Serial error: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")
