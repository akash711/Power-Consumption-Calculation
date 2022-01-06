# Power-Consumption-Calculation

Data processing script to calculate total consumption from a given list of meters

- All operations are vectorized
- Performance benchmarking done using line profiler

Dataset : data.xlsx

- Contains 3 sheets: Forecasted Consumption, Meter List and Rates
- Forecasted Consumption table consists of power forecast for a list of meters for a given period.
- Meter List holds information about each meter (Exit Zones and Annual Quantity)
- Rates table contains rates corresponding to exit zone and annual quantity


File Organization:
- portfolio.py: contains Portfolio class with all required functions
- main.py: driver code to instantiate Portfolio for given data
- bencharmking_script.ipynb: Jupyer notebook with visualization and benchmarking for execution speed

