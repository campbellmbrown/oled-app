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
    packet.append(crc & 0xFF)
    packet.append((crc >> 8) & 0xFF)

    return packet
