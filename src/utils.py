import json
import csv
from typing import List, Dict

import pandas as pd

from interfaces import DeviceI


def sort_devices(devices: List[DeviceI], avg_rp: float, total_duration: int):
    """
    Sort devices by priority and stability.
    """

    def get_score(device: DeviceI):
        priority_weight = 0.5
        stability_weight = 0.6

        stability = (
            ((device.rated_power * device.capacity) / total_duration) / avg_rp
        ) * stability_weight

        priority = priority_weight * device.priority

        return stability + priority

    return sorted(devices, key=get_score, reverse=True)


def save_to_json(data: List[Dict]):
    with open("./res.json", "+w") as ff:
        ff.write(json.dumps(data, indent=4))


def save_to_csv(data: List[Dict]):
    with open("./res.csv", "w", newline="") as csvfile:
        fieldnames = ["minute", "total_power", "stability"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for minute_data in data:
            writer.writerow(minute_data)


def get_power_curve(file_path: str = "power_curve.csv"):
    power_curve_raw = pd.read_csv(file_path)

    start_bounce = []
    golden_era = []
    end_bounce = []

    start_bounce_total_seconds = 140
    end_bounce_total_seconds = 3600

    for _, row in power_curve_raw.iterrows():
        if row["total_seconds"] < start_bounce_total_seconds:
            start_bounce.append(row["normalized_power_level"])
        elif (
            row["total_seconds"] > start_bounce_total_seconds
            and row["total_seconds"] < end_bounce_total_seconds
        ):
            golden_era.append(row["normalized_power_level"])
        elif row["total_seconds"] > end_bounce_total_seconds:
            end_bounce.append(row["normalized_power_level"])

    return start_bounce, golden_era, end_bounce
