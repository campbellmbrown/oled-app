#include "serial_protocol.h"

#include "crc16.h"
#include "oled.h"

#include <Arduino.h>
#include <assert.h>

#define HEADER_1 (0xAA)
#define HEADER_2 (0x55)
#define MAX_PAYLOAD_SIZE (OLED_BUFFER_SIZE)
#define ACK (0x06)
#define NACK (0x15)

typedef enum
{
    RECIEVE_STATE_HEADER_LSB,
    RECIEVE_STATE_HEADER_MSB,
    RECIEVE_STATE_LENGTH_LSB,
    RECIEVE_STATE_LENGTH_MSB,
    RECIEVE_STATE_DATA,
    RECIEVE_STATE_CRC_LSB,
    RECIEVE_STATE_CRC_MSB,
} receive_state_t;

typedef struct
{
    receive_state_t state;
    uint16_t expected_len;
    uint16_t received_len;
    uint16_t crc;
    uint8_t payload[MAX_PAYLOAD_SIZE];
} serial_protocol_t;

static serial_protocol_t protocol;

static void send_ack(void);
static void send_nack(void);

void serial_protocol_init(void)
{
    protocol.state = RECIEVE_STATE_HEADER_LSB;
}

void serial_protocol_process(void)
{
    while (Serial.available())
    {
        uint8_t rx_byte = Serial.read();

        switch (protocol.state)
        {
        case RECIEVE_STATE_HEADER_LSB:
            if (rx_byte == HEADER_1)
            {
                protocol.state = RECIEVE_STATE_HEADER_MSB;
            }
            break;
        case RECIEVE_STATE_HEADER_MSB:
            if (rx_byte == HEADER_2)
            {
                protocol.state = RECIEVE_STATE_LENGTH_LSB;
            }
            else
            {
                // Incorrectly assumed header, go back to looking for first byte
                protocol.state = RECIEVE_STATE_HEADER_LSB;
            }
            break;
        case RECIEVE_STATE_LENGTH_LSB:
            protocol.expected_len = rx_byte;
            protocol.state = RECIEVE_STATE_LENGTH_MSB;
            break;
        case RECIEVE_STATE_LENGTH_MSB:
            protocol.expected_len |= (uint16_t)rx_byte << 8;
            if (protocol.expected_len > MAX_PAYLOAD_SIZE)
            {
                protocol.state = RECIEVE_STATE_HEADER_LSB;
            }
            else
            {
                protocol.received_len = 0;
                protocol.state = RECIEVE_STATE_DATA;
            }
            break;
        case RECIEVE_STATE_DATA:
            protocol.payload[protocol.received_len] = rx_byte;
            protocol.received_len++;
            if (protocol.received_len >= protocol.expected_len)
                protocol.state = RECIEVE_STATE_CRC_LSB;
            break;
        case RECIEVE_STATE_CRC_LSB:
            protocol.crc = rx_byte;
            protocol.state = RECIEVE_STATE_CRC_MSB;
            break;
        case RECIEVE_STATE_CRC_MSB:
            protocol.crc |= (uint16_t)rx_byte << 8;
            uint16_t calc = crc16(protocol.payload, protocol.expected_len);
            protocol.state = RECIEVE_STATE_HEADER_LSB;
            if (calc == protocol.crc)
            {
                oled_set_image_ret_t ret = oled_set_image(protocol.payload, protocol.expected_len);
                if (ret == OLED_SET_IMAGE_SUCCESS)
                {
                    send_ack();
                }
                else
                {
                    send_nack();
                }
            }
            else
            {
                send_nack();
            }
            break;
        }
    }
}

static void send_ack(void)
{
    Serial.write(ACK);
    Serial.flush();
}

static void send_nack(void)
{
    Serial.write(NACK);
    Serial.flush();
}
