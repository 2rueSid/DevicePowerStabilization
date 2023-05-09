import argparse
import os

from device import get_devices, get_average_rated_power, get_total_rated_power
from process import create_schedule
from utils import sort_devices, save_to_json, save_to_csv
from constants import (
    TOTAL_POWER_BASIS_PERCENTAGE,
    TOTAL_DURATION,
    DEVICES_CSV_FILE_PATH,
)


# Command-line argument parser
parser = argparse.ArgumentParser(
    description="Create device schedule from a given device_list.csv file"
)
parser.add_argument(
    "input_file",
    type=str,
    default=DEVICES_CSV_FILE_PATH,
    help="Path to the device_list.csv file",
)
parser.add_argument(
    "--basis_percentage",
    type=float,
    default=TOTAL_POWER_BASIS_PERCENTAGE,
    help="The percentage of total power to be used as the basis",
)
parser.add_argument(
    "--output_format",
    type=str,
    choices=["csv", "json"],
    default="json",
    help="Output file format: 'csv' or 'json'",
)

args = parser.parse_args()

if not os.path.exists(args.input_file):
    print(f"Input file {args.input_file} not found.")
    exit(1)

running_devices = get_devices(args.input_file)

average_rated_power = get_average_rated_power(running_devices)
sorted_devices = sort_devices(running_devices, average_rated_power, TOTAL_DURATION)

total_power = get_total_rated_power(sorted_devices)
schedule = create_schedule(sorted_devices, total_power * args.basis_percentage)


if args.output_format == "json":
    stats = schedule.get_stats_json()
    save_to_json(stats)
elif args.output_format == "csv":
    stats = schedule.get_stats_csv()
    save_to_csv(stats)
