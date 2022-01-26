from numpy.core.numeric import outer
import pandas as pd
import numpy as np

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

daily_cases_df = pd.read_csv(INT_MED_DIR+'3-4-daily_cases_df.csv')
month_df = pd.read_csv(INT_MED_DIR+'3-4-month_df.csv')

sunday_start_week_df = daily_cases_df.copy()

for index, row in sunday_start_week_df.iterrows():
    if row['Day'] == 'Sunday':
        break
    sunday_start_week_df.drop(index, inplace=True)

thursday_start_week_df = daily_cases_df.copy()

for index, row in thursday_start_week_df.iterrows():
    if row['Day'] == 'Thursday':
        break
    thursday_start_week_df.drop(index, inplace=True)

n = 7
non_overlap_sun_week_df = sunday_start_week_df.groupby(sunday_start_week_df.reset_index().index // n).sum()
non_overlap_thu_week_df = thursday_start_week_df.groupby(thursday_start_week_df.reset_index().index // n).sum()

non_overlap_sun_week_df.index = 2*non_overlap_sun_week_df.index + 1
non_overlap_thu_week_df.index = non_overlap_thu_week_df.index + 1
non_overlap_thu_week_df.index = 2*non_overlap_thu_week_df.index
overlap_week_df = pd.concat([non_overlap_sun_week_df, non_overlap_thu_week_df], sort=False).sort_index()

# state wise week
df_T = overlap_week_df.T
df_T['State'] =  df_T.index
df_T['State'] = df_T['State'].apply(lambda x : x.split('_')[0])
df_T = df_T.groupby('State').sum()
s_week_df = df_T.T

# state wise month
df_T = month_df.T
df_T['State'] =  df_T.index

dkey = np.unique(df_T['State'])

df_T['State'] = df_T['State'].apply(lambda x : x.split('_')[0])

skey = np.unique(df_T['State'])

df_T = df_T.groupby('State').sum()
s_month_df = df_T.T
# s_month_df.drop(['Unknown'], axis = 1, inplace=True)

# overall data
overall_month_df = pd.DataFrame()
overall_month_df['overall']= s_month_df.sum(axis=1)

overall_week_df = pd.DataFrame()
overall_week_df['overall']= s_week_df.sum(axis=1)

# finding split month and week = ((8 Feb 2021 - 26 April 2020)/7) * 2
week_split = 82 
month_split = 11

# overall
wave_1_week_overall = overall_week_df.iloc[0:week_split].idxmax()
wave_2_week_overall = overall_week_df.iloc[week_split:].idxmax()

wave_1_month_overall = overall_month_df.iloc[0:month_split].idxmax()
wave_2_month_overall = overall_month_df.iloc[month_split:].idxmax()

overall_df = pd.DataFrame(columns=['overall', 'wave1 − weekid', 'wave2 − weekid', 'wave1 − monthid', 'wave2 − monthid'])

overall_df[0] = ['Overall', wave_1_week_overall, wave_2_week_overall, wave_1_month_overall, wave_2_month_overall]

# state wise
wave_1_week_state = s_week_df.iloc[0:week_split].idxmax()
wave_2_week_state = s_week_df.iloc[week_split:].idxmax()

wave_1_month_state = s_month_df.iloc[0:month_split].idxmax()
wave_2_month_state = s_month_df.iloc[month_split:].idxmax()

state_df = pd.DataFrame(columns=['districtid', 'wave1 − weekid', 'wave2 − weekid', 'wave1 − monthid', 'wave2 − monthid'])

for state in skey:
    wave_1_week = wave_1_week_state[state]
    wave_2_week = wave_2_week_state[state]
    wave_1_month = wave_1_month_state[state]
    wave_2_month = wave_2_month_state[state]
    state_df[len(state_df.index)] = [state, wave_1_week, wave_2_week, wave_1_month, wave_2_month]

# district wise
wave_1_week_district = overlap_week_df.iloc[0:week_split].idxmax()
wave_2_week_district = overlap_week_df.iloc[week_split:].idxmax()

wave_1_month_district = month_df.iloc[0:month_split].idxmax()
wave_2_month_district = month_df.iloc[month_split:].idxmax()

district_df = pd.DataFrame(columns=['stateid', 'wave1 − weekid', 'wave2 − weekid', 'wave1 − monthid', 'wave2 − monthid'])

for dist in dkey:
    wave_1_week = wave_1_week_district[dist]
    wave_2_week = wave_2_week_district[dist]
    wave_1_month = wave_1_month_district[dist]
    wave_2_month = wave_2_month_district[dist]
    state_df[len(state_df.index)] = [state, wave_1_week, wave_2_week, wave_1_month, wave_2_month]

district_filename = 'peaks-district.csv'
state_filename = 'peaks-state.csv'
overall_filename = 'peaks-overall.csv'

district_df.to_csv(OUTPUT_DIR+district_filename, index=False)
state_df.to_csv(OUTPUT_DIR+state_filename, index=False)
overall_df.to_csv(OUTPUT_DIR+overall_filename, index=False)
