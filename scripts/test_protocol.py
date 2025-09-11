from PIL import Image
import numpy as np
import serial
import logging

HEADER_1 = 0xAA
HEADER_2 = 0x55


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def create_packet(image_data: bytes) -> bytearray:
    packet = bytearray()

    # Header
    packet.append(HEADER_1)
    packet.append(HEADER_2)
    # Length
    length = len(image_data)
    packet.append(length & 0xFF)
    packet.append((length >> 8) & 0xFF)
    # Payload
    packet.extend(image_data)
    # CRC
    crc = crc16(image_data)
    logging.info("CRC: %04X", crc)
    packet.append(crc & 0xFF)
    packet.append((crc >> 8) & 0xFF)

    return packet

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Open image
logging.info("Opening image...")
img = Image.open("test.png").convert("L")

# Threshold to binary
threshold = 128
binary_img = img.point(lambda p: 1 if p < threshold else 0, '1')

# Convert to numpy array
arr = np.array(binary_img, dtype=np.uint8)

logging.info("Image shape: %dx%d", arr.shape[0], arr.shape[1])

byte_array = bytearray()
for row in arr:
    byte = 0
    for i, pixel in enumerate(row):
        byte = (byte << 1) | pixel
        if (i + 1) % 8 == 0:
            swapped_byte = int('{:08b}'.format(byte)[::-1], 2)
            byte_array.append(swapped_byte)
            byte = 0

logging.info("Opening serial port...")
ser = serial.Serial("COM3", 9600, timeout=1, write_timeout=1)

logging.info("Creating packet...")
packet = create_packet(byte_array)
logging.info("Packet length: %d", len(packet))

logging.info("Sending packet...")
ser.write(packet)

logging.info("Waiting for response...")
response = ser.read(1)
logging.info("Response: %02X", response[0])
