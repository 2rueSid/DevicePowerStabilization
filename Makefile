run_json:
	poetry run python3 ./src/main.py devices_list.csv --basis_percentage 0.4 --output_format json

run_csv:
	poetry run python3 ./src/main.py devices_list.csv --basis_percentage 0.43 --output_format csv

create_plot:
	poetry run python3 ./src/plot.py