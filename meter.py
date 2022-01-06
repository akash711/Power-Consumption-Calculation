import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from timeit import default_timer as timer
import warnings
warnings.filterwarnings("ignore")

class Portfolio:

    def __init__(self, length: int):
        #No. of meters
        if length > 0:
            self.length = length
        else: 
            raise Exception('Enter positive value for length')

    
    def generate_meters(self):
        """
        Function to generate valid meters of given length
        Returns meter table with Meter ID, Exit Zone and Annual Quantity in kWh
        """
        exit_zone = ['SC1', 'EM2', 'NW1']
        self.meters = pd.DataFrame(index=range(self.length), columns=['Meter ID', 'Exit Zone', 'Annual Quantity (kWh)'])
        self.meters['Meter ID'] = [np.random.randint(0,100000) for i in range(self.length)]
        self.meters['Exit Zone'] = [exit_zone[np.random.randint(0,len(exit_zone))] for i in range(self.length)]
        self.meters['Annual Quantity (kWh)'] = [np.random.randint(0, 1000000) for i in range(self.length)]
        return self.meters
    
    def generate_consumption(self, start, end):


        """ 
        Function to generate mock consumption data for a given meter list, start and end date
        Takes a list of meters, annual consumption per meter and generates valid consumption data in appropriate ranges

        """

        n_days = (end - start).days
        self.consumption_data = pd.DataFrame(index = range(len(self.meters)*n_days), columns = ['Date', 'Meter ID', 'kWh'])
        dates = []
        
        for i in range(len(self.meters)):
            dates += [start + timedelta(days=x) for x in range(n_days)]

        self.consumption_data['Date'] = dates

        meter_id = []
        for i in range(len(self.meters)):
            meter_id += [self.meters['Meter ID'][i] for j in range(n_days)]
        
        self.consumption_data['Meter ID'] = meter_id
        kWh = []
        for i in range(len(self.meters)):
            daily_avg = self.meters['Annual Quantity (kWh)'][i]/365
            kWh += [ daily_avg + (np.random.randint(-5,5)*0.1*daily_avg) for j in range(n_days) ]

        self.consumption_data['kWh'] = kWh

        return self.consumption_data

    def calculate_total(self, consumption, meters, rates):
    
        """
        Function to calculate total Transportation Costs given a list of meters, consumption data and rate table

        Returns DataFrame with MeterID, total consumption for entire period (kWh) and total cost (GBP)
        """
        
        
        temp = consumption.merge(meters, on = 'Meter ID', how = 'left')

        
        periods = rates['Date'].unique()
        aq_range = rates['Annual Quantity (Min)'].unique()

        cond = [(aq_range[0] <= temp['Annual Quantity (kWh)'].values) & (temp['Annual Quantity (kWh)'].values < aq_range[1]),
        (aq_range[1] <= temp['Annual Quantity (kWh)'].values) & (temp['Annual Quantity (kWh)'].values < aq_range[2]),
        (temp['Annual Quantity (kWh)'].values > aq_range[2])]
        choice = aq_range

        
        temp['Annual Quantity (Min)'] = np.select(cond, choice)

        for i in range(len(periods)-1):
            temp['Date'][np.where((periods[i] <= temp['Date']) & (temp['Date'] < periods[i+1]))[0]] = periods[i]

        
        total_cost = temp.merge(rates, how = 'left')
        total_cost['Cost in GBP'] = (total_cost['kWh'] * total_cost['Rate (p/kWh)']) * 0.01

        #Return Total Consumption and Cost in GBP for all meters
        return total_cost[['Meter ID', 'kWh','Cost in GBP']].groupby('Meter ID').sum().round(2)
