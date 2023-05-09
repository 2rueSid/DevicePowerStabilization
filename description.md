## Attributes
- Rated power (5-15 kW): The rated power of a device is the maximum continuous power output it can provide, measured in kilowatts (kW). Devices have a rated power between 5 kW and 15 kW.
- Capacity (60-210 min): The capacity of a device is the total amount of time it can operate at its rated power before running out of energy, measured in minutes. Devices have capacities ranging from 60 to 210 minutes.
- Priority (1-10, 10 = highest): The priority attribute represents the importance of a device. Devices with a higher priority should be activated before devices with a lower priority, ensuring the most important devices receive power first. Priority values range from 1 (lowest) to 10 (highest).

## Prerequisites
Your job is to maximize the combined total electric power of these devices over a period of 4 hours. Since no device has enough capacity to run at its rated power for the full duration of 4 hours, you’ll have to implement an algorithm that controls when which device runs (=is activated). The resulting list of devices with their respective activation times is called a device activation schedule. There are 2 further constraints:
1. The combined total electric power has to be kept within a +/-3% bound at all times.
2. Devices have to be activated for a minimum time of 30 minutes per activation.

### In depth description of the task
If we turned on all of them at once, we would have maximum power at first. but over time, as the capacitate progresses, some devices will start to turn off, and by the 240th minute, the maximum power will be zero because most devices will start to turn off.
Priority should be taken into account when you need to turn off a device when its battery life is about to expire. and to avoid turning off a device with a high priority and replacing it with a device with a low priority.

conditions:
- combined power should be stable -+ 3%. `throttle_percent = 0.03`
- device should be active for a minimum of 30 minutes. `minimum_processing_time = 30`
- each device can be switched on and off, the number of switching on can be calculated by the formula `(device.capacity - minimum_processing_time) > 0`
- full duration for which we creating this schedule is 240 minutes (4 hours). `total_duration = 240`