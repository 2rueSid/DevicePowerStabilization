from typing import List

from pydantic import BaseModel


class DeviceI(BaseModel):
    device_id: int
    rated_power: int
    capacity: float
    priority: float
    capacity_left: float


class MinuteInSchedule(BaseModel):
    minute: int
    running_devices: List[DeviceI]
    total_rp_per_minute: float
    stability: float
    inactive_devices: List[DeviceI] = []

    @staticmethod
    def initialize(minute: int):
        return MinuteInSchedule(
            running_devices=[],
            total_rp_per_minute=float(0),
            stability=float(1),
            minute=minute,
            inactive_devices=[],
        )


class DeviceOutputI(BaseModel):
    schedule: List[MinuteInSchedule]

    def get_stats_json(self):
        stats = []
        for minute in self.schedule:
            running_devices = []
            for device in minute.running_devices:
                running_devices.append(device.device_id)
            stats.append(
                {
                    minute.minute: {
                        "total_power": minute.total_rp_per_minute,
                        "stability": minute.stability,
                        "running_devices": running_devices,
                    }
                }
            )
        return stats

    def get_stats_csv(self):
        data = []

        for minute in self.schedule:
            data.append(
                {
                    "minute": minute.minute,
                    "total_power": minute.total_rp_per_minute,
                    "stability": minute.stability,
                }
            )
        return data
