import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


from portfolio import Portfolio



forecast_data = pd.read_excel('data.xlsx', sheet_name = 'Forecasted Consumption')
rates = pd.read_excel('data.xlsx', sheet_name='Rates')
rates = rates.fillna(np.inf)
meter_list = pd.read_excel('data.xlsx', sheet_name='Meter List')

exit_zone = rates['Exit Zone'].unique() #Fetch unique exit zones

portfolio = Portfolio(5)

#meters = portfolio.generate_meters(length = n)
start = datetime(2020,10,1)
end = datetime(2022,10,1)
#consumption = generate_consumption(meters, start, end)
total = portfolio.calculate_total(forecast_data, meter_list, rates)
print(total)
