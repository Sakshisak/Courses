import numpy as np
import pandas as pd

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

s_last_week_dose1 = pd.read_csv(INT_MED_DIR+'5-9-state-dose1.csv')
state_ratio_df = pd.read_csv(OUTPUT_DIR+'vaccinated-dose-ratio-state.csv')

# This is the rate of vaccination of first dose (No.of People/Week) in the last week
rate_df = s_last_week_dose1

state_ratio_df = state_ratio_df
state_ratio_df['populationleft'] = state_ratio_df['Total Population'] * (1 - state_ratio_df['vaccinateddose1ratio'])
state_ratio_df['rateofvaccination'] = state_ratio_df.apply(lambda row: (rate_df['rate'].values[rate_df['stateid']==row.stateid])[0], axis=1)

# people/day : converting people/week to people/day
state_ratio_df['rateofvaccination'] = state_ratio_df['rateofvaccination']/7

state_ratio_df['time'] = state_ratio_df['populationleft']/state_ratio_df['rateofvaccination']
state_ratio_df['time'] = state_ratio_df['time'].apply(np.ceil)

start_date = "15/08/2021"
start_date_pandas = pd.to_datetime(start_date)
state_ratio_df['date'] = state_ratio_df.apply(lambda row: start_date_pandas + pd.DateOffset(days=row.time), axis=1)

# getting columns of our interest
col = ['stateid', 'populationleft', 'rateofvaccination','date'] 
state_ratio_df = state_ratio_df[col]

output_filename = 'complete-vaccination.csv'

state_ratio_df.to_csv(OUTPUT_DIR+output_filename, index=False)