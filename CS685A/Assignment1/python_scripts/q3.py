from typing import overload
import pandas as pd
import numpy as np
import datetime

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

# convert date field type from string to datetime object
districts_modified_file = INT_MED_DIR+'districts-modified.csv'
districts_modified_df = pd.read_csv(districts_modified_file)
districts_modified_df['Tested'] = districts_modified_df['Tested'].replace(np.nan, 0)
districts_modified_df.drop(districts_modified_df.index[districts_modified_df['District'] == "Unknown"], inplace=True)

first_date = datetime.datetime.strptime('2020-04-26', "%Y-%m-%d").date()
district_list = districts_modified_df['District_Id'].unique()

district_dict = {}
for district in district_list:
    district_df = districts_modified_df[districts_modified_df['District_Id'] == district]
    time_dict = {}
    time_dict[0] = 0
    for index, row in district_df.iterrows():
        time_dict[row['Date']] = row['Confirmed']
    district_dict[district] = time_dict

daily_cases_df = pd.DataFrame(district_dict)
daily_cases_df = daily_cases_df.fillna(0)
daily_cases_df = daily_cases_df.diff()
daily_cases_df = daily_cases_df.dropna()
# replace negative values  with zeroes
daily_cases_df[daily_cases_df < 0] = 0

d_week_df = pd.DataFrame(columns=['districtid', 'timeid', 'cases'])
d_month_df = pd.DataFrame(columns=['districtid', 'timeid', 'cases'])
d_overall_df = pd.DataFrame(columns=['districtid', 'timeid', 'cases'])

# overall data
overall_df = daily_cases_df.sum()
for dist in district_list:
    cases = overall_df[dist]
    d_overall_df.loc[len(d_overall_df.index)] = [dist, 1, cases]

# non-overlap weekly cases
n = 7
week_df = daily_cases_df.groupby(daily_cases_df.reset_index().index // n).sum()
week_df.index = week_df.index + 1

for dist in district_list:
    cases_row = week_df[dist]
    for index in range(len(cases_row)):
        cases = cases_row[index+1]
        d_week_df.loc[len(d_week_df.index)] = [dist, index+1, cases]


# monthly cases data
daily_cases_df['Date'] = daily_cases_df.index
daily_cases_df['Date'] = pd.to_datetime(daily_cases_df['Date'])
daily_cases_df['Day'] = daily_cases_df['Date'].dt.day_name()
daily_cases_df.to_csv(INT_MED_DIR+'3-4-daily_cases_df.csv', index=False)

# create monthid
daily_cases_df['month_id'] = 1
ctr = 1
for i, row in daily_cases_df.iterrows():
    daily_cases_df.at[i,'month_id'] = ctr
    if row['Date'].day == 14:
        ctr+=1
month_df = daily_cases_df.groupby('month_id').sum()

month_df.to_csv(INT_MED_DIR+'3-4-month_df.csv', index=False)

for dist in district_list:
    cases_row = month_df[dist]
    for index in range(len(cases_row)):
        cases = cases_row[index+1]
        d_month_df.loc[len(d_month_df.index)] = [dist, index+1, cases]

# sorting final dataframes based on district_id
d_week_df = d_week_df.sort_values(['districtid','timeid'], ascending=[True, True], axis=0)
d_month_df = d_month_df.sort_values(['districtid','timeid'], ascending=[True, True], axis=0)
d_overall_df = d_overall_df.sort_values(['districtid','timeid'], ascending=[True, True], axis=0)

# writing dataframes to csv

week_filename = 'cases-week.csv'
month_filename = 'cases-month.csv'
overall_filename = 'cases-overall.csv'


d_week_df.to_csv(OUTPUT_DIR+week_filename, index=False)
d_month_df.to_csv(OUTPUT_DIR+month_filename, index=False)
d_overall_df.to_csv(OUTPUT_DIR+overall_filename, index=False)