# Device Power Stabilization

## Structure:
```
- /src
-- constants.py
-- device.py # pydantic model to work with device
-- interfaces.py # default interfaces
-- main.py # functions to run program
-- plot.py # plot generation
-- process.py # main algorithm to create schedule
-- utils.py
```

## How To Setup

Install dependencies
```bash
$ poetry install
```

## How to test

### Run manually

Available start parameters
```bash
$ poetry run python3 ./src/main.py -h

usage: main.py [-h] [--basis_percentage BASIS_PERCENTAGE] [--output_format {csv,json}] input_file

Create device schedule from a given device_list.csv file

positional arguments:
  input_file            Path to the device_list.csv file

options:
  -h, --help            show this help message and exit
  --basis_percentage BASIS_PERCENTAGE
                        The percentage of total power to be used as the basis
  --output_format {csv,json}
                        Output file format: 'csv' or 'json'
```
Example:

- To create create schedule csv file:
```bash
$ poetry run python3 ./src/main.py devices_list.csv --basis_percentage 0.43 --output_format csv
```

- To create plot base on schedule:
```bash
$ poetry run python3 ./src/plot.py
```

### Run with makefile
- Create schedule
```
$ make run csv
```

- Create plot
```
$ make run create_plot
```

## Documentation

Basically all the logic is described inside functions.

But need to mention about `basis_percentage` parameter.
This is a value between `0.0...1 - 1`. This value represent percentage of total `rated_power` of all devices.

It's used to decide hom many devices should be run instantly, and what value will be basic stable total rated power. 
