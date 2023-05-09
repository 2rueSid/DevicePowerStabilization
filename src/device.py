from typing import List

import pandas as pd

from interfaces import DeviceI


class Device(DeviceI):
    @staticmethod
    def build(device_id: int, rated_power: int, capacity: float, priority: float):
        return Device(
            device_id=device_id,
            rated_power=rated_power,
            capacity=capacity,
            priority=priority,
            capacity_left=capacity,
        )


def get_total_rated_power(devices: List[Device]):
    return sum(device.rated_power for device in devices)


def get_average_rated_power(devices: List[Device]):
    return get_total_rated_power(devices) / len(devices)


def get_devices(file_path: str):
    devices_raw = pd.read_csv(file_path)

    return [
        Device.build(
            device_id=row["device_id"],
            rated_power=row["rated_power"],
            capacity=row["capacity"],
            priority=row["priority"],
        )
        for _, row in devices_raw.iterrows()
    ]
