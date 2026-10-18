
"""Send synthetic CAN traffic on vcan0 for local testing only."""

import time
import can


def main():
    bus = can.interface.Bus(
        channel="vcan0",
        interface="socketcan",
    )

    messages = [
        can.Message(
            arbitration_id=0x100,
            data=bytes([0x01, 0x00, 0xFF, 0xA2, 0x12, 0x44, 0x55, 0x66]),
            is_extended_id=False,
        ),
        can.Message(
            arbitration_id=0x321,
            data=bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]),
            is_extended_id=False,
        ),
        can.Message(
            arbitration_id=0x200,
            data=b"\xFF" * 8,
            is_extended_id=False,
        ),
    ]

    print("[+] Sending synthetic CAN messages on vcan0 for 15 seconds...")

    start = time.monotonic()

    try:
        while time.monotonic() - start < 15:
            for message in messages:
                bus.send(message)
                print(f"Sent ID: 0x{message.arbitration_id:03X}")
                time.sleep(0.5)
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
