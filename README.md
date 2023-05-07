# Backend Engineer Coding Challenge
## Description
You are working for a company which controls electric devices. The company has a pool of 250 devices, each with the
attributes listed below. All attribute values are fixed for a given device. The company has provided you with a CSV
containing the attributes of all 250 devices (device_list.csv).

```
Rated power: 5-15 kW
Capacity: 60-210 min
Priority: 1-10 (10 = highest)
```

Your job is to maximize the combined total electric power of these devices over a period of 4 hours. Since no device has
enough capacity to run at its rated power for the full duration of 4 hours, you’ll have to implement an algorithm that
controls when which device runs (=is activated). The resulting list of devices with their respective activation times is
called a device activation schedule. There are 2 further constraints:

1. The combined total electric power has to be kept within a +/-3% bound at all times.
2. Devices have to be activated for a minimum time of 30 minutes per activation.

Bonus: The devices do not start utilizing power instantly, can’t hold power perfectly at their rated power level, and take
some time to shut down. We’ve included a time series of a real device that is activated for one hour (power curve, see
plot below). Please use this power curve to simulate the real-world behavior of each device. Make sure that the simulated
activated devices also fulfill the 2 constraints listed above. Of course, you’re allowed to modify your previously created
device activation schedule.
