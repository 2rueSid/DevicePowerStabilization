from typing import List

from interfaces import DeviceOutputI, DeviceI, MinuteInSchedule
from constants import MINIMUM_PROCESSING_TIME, BOUNCE_PERCENTAGE, TOTAL_DURATION


def create_schedule(devices: List[DeviceI], total_power_basis: float):
    """
    Create running device schedule.

    Params:
        devices - List of Device

        total_power_basis - A baseline that determines the value to which devices should be launched.
    """
    schedule_response = DeviceOutputI(schedule=[])

    # iterate over full cycle of TOTAL_DURATION.
    for minute in range(TOTAL_DURATION + 1):
        if len(schedule_response.schedule) <= 0:
            current_minute = initialize_starting_minute(devices, total_power_basis)
            schedule_response.schedule.append(current_minute)
            continue

        prev_minute = get_prev_minute(minute, schedule_response)

        if not prev_minute:
            break

        current_minute = initialize_current_minute(
            prev_minute, minute, total_power_basis
        )

        current_stability = current_minute.stability

        total_power_current_minute = current_minute.total_rp_per_minute

        # total_power_prev_minute = prev_minute.total_rp_per_minute

        # devices are stable
        if (
            current_stability >= 1 - BOUNCE_PERCENTAGE
            and current_stability <= 1 + BOUNCE_PERCENTAGE
        ):
            schedule_response.schedule.append(current_minute)
            continue
        # need to reduce activity
        elif current_stability < 1 - BOUNCE_PERCENTAGE:
            running_devices_sorted = sort_by_priority_asc(
                current_minute.running_devices
            )

            for running_device in running_devices_sorted:
                # if not capacity_enough_for_activation(running_device.capacity_left):
                #     continue

                if total_power_current_minute > total_power_basis:
                    current_minute.running_devices = remove_from_list(
                        current_minute.running_devices, running_device.device_id
                    )

                    total_power_current_minute = (
                        get_device_power_for_minute(running_device)
                        - total_power_current_minute
                    )

                    current_minute.inactive_devices.append(running_device)

        # need to enlarge activity
        elif current_stability > 1 + BOUNCE_PERCENTAGE:
            inactive_list = sort_by_rp_desc(current_minute.inactive_devices)

            for inactive_devise in inactive_list:
                if not capacity_enough_for_activation(inactive_devise.capacity_left):
                    continue

                if total_power_current_minute < total_power_basis:
                    current_minute.running_devices.append(inactive_devise)

                    total_power_current_minute = (
                        get_device_power_for_minute(inactive_devise)
                        + total_power_current_minute
                    )

                    # remove it from not yet running list
                    current_minute.inactive_devices = remove_from_list(
                        current_minute.inactive_devices, inactive_devise.device_id
                    )

        current_minute.total_rp_per_minute = get_devices_total_rated_power(
            current_minute.running_devices
        )

        current_minute.stability = get_stability(
            total_power_basis, current_minute.total_rp_per_minute
        )

        schedule_response.schedule.append(current_minute)

    return schedule_response


def initialize_current_minute(
    prev_minute: MinuteInSchedule, minute: int, total_power_basis: float
):
    """
    Current minute initialization.

    After initialization, copy from the previous minute running devices, inactive devices;
    Turn of devices that are run out of capacity;
    Decrease capacity for running devices by 1;
    Calculate current stability and total rated power.
    """
    current_minute = MinuteInSchedule.initialize(minute)
    running_devices = prev_minute.running_devices
    current_minute.running_devices = []

    current_minute.inactive_devices = prev_minute.inactive_devices

    for running_device in running_devices:
        capacity_left = running_device.capacity_left
        if capacity_left <= 0:
            continue
        else:
            running_device.capacity_left = decrease_capacity(capacity_left)

        current_minute.running_devices.append(running_device)

    total_power_current_minute = get_devices_total_rated_power(
        current_minute.running_devices
    )

    current_stability = get_stability(total_power_basis, total_power_current_minute)

    current_minute.stability = current_stability
    current_minute.total_rp_per_minute = total_power_current_minute

    return current_minute


def initialize_starting_minute(devices: List[DeviceI], total_power_basis: float):
    """
    Initialize starting minute and run devices till they reach total_power_basis.

    After total power of active devices reach total_power_basis, save others in inactive state.
    """
    current_minute = MinuteInSchedule.initialize(0)
    for device in devices:
        if capacity_enough_for_activation(device.capacity):
            if current_minute.total_rp_per_minute <= total_power_basis:
                current_minute.running_devices.append(device)

                current_minute.total_rp_per_minute = (
                    device.rated_power + current_minute.total_rp_per_minute
                )
            else:
                current_minute.inactive_devices.append(device)
    return current_minute


def remove_from_list(devices: List[DeviceI], device_id: int) -> List[DeviceI]:
    """Remove item from the list of devices by id"""
    return [device for device in devices if device.device_id != device_id]


def decrease_capacity(capacity_left: float) -> float:
    """Decrease device capacity by 1"""
    return capacity_left - 1


def sort_by_priority_asc(devices: List[DeviceI]):
    """Sort devices by priority (ASC)"""
    return sorted(devices, key=lambda device: device.priority)


def sort_by_rp_desc(devices: List[DeviceI]):
    """Sort devices by priority (ASC)"""
    return sorted(devices, key=lambda device: device.rated_power, reverse=True)


def get_devices_total_rated_power(devices: List[DeviceI]) -> float:
    """Calculate total rated power for minute"""
    return sum(get_device_power_for_minute(device) for device in devices)


def get_stability(param1: float, param2: float) -> float:
    """Calculate stability"""
    if param1 and param2:
        return round(
            param1 / param2,
            3,
        )
    return 0


def get_prev_minute(minute: int, schedule: DeviceOutputI):
    """Get previous minute from the schedule list"""
    if minute > 0 and len(schedule.schedule) > minute - 1:
        return schedule.schedule[minute - 1]
    else:
        return None


def capacity_enough_for_activation(capacity_left):
    """Check if capacity is satisfying minimum capacity for start constraint"""
    if capacity_left + 1 > MINIMUM_PROCESSING_TIME:
        return True

    return False


def get_device_power_for_minute(device: DeviceI) -> float:
    return device.rated_power
