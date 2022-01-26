# Question-5
import pandas as pd
import numpy as np
from datetime import date, timedelta

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

cowin_file = INPUT_DIR+'cowin_vaccine_data_districtwise.csv'

cowin_df = pd.read_csv(cowin_file, header=[0,1])
cowin_df = cowin_df.fillna(0)
cowin_df = cowin_df.drop_duplicates(subset=cowin_df.loc[[],['District_Key']].columns)

start_date = date(2021, 1, 16)
end_date = date(2021, 8, 15)

# generates dates for all Sundays
weekly_dates = []
for n in range(int((end_date - start_date).days/7)):
    date_ = start_date + timedelta(n)*7
    date_ = date_.strftime("%d/%m/%Y")
    weekly_dates.append(date_)

# generates dates for all months
monthly_dates = []
m_dates = pd.date_range(start=start_date - pd.DateOffset(days=15) , end=end_date, freq='MS')+ pd.DateOffset(days=15)    
for date_ in m_dates:
    date_ = date_.strftime("%d/%m/%Y")
    monthly_dates.append(date_)


# district-wise data
dkey = np.unique(cowin_df['District_Key'])
d_week_df = pd.DataFrame(columns=['districtid', 'timeid', 'dose1', 'dose2'])
d_month_df = pd.DataFrame(columns=['districtid', 'timeid', 'dose1', 'dose2'])
d_overall_df = pd.DataFrame(columns=['districtid', 'timeid', 'dose1', 'dose2'])

for dist in dkey:
    dist_df = cowin_df[np.array(cowin_df['District_Key'] == dist)]
    dist_name = dist_df['District'].iloc[0]
    dist_name = dist_name[0]

    for i in range(len(weekly_dates)):
        date_c = weekly_dates[i]
        dose1_col = [(date_c, 'First Dose Administered')]
        dose2_col = [(date_c, 'Second Dose Administered')]
        dose1_df = dist_df[dose1_col]
        dose2_df = dist_df[dose2_col]
        dose1 = dose1_df.sum(axis=0)[0]
        dose2 = dose2_df.sum(axis=0)[0]
        d_week_df.loc[len(d_week_df.index)] = [dist, i+1, dose1, dose2]
    
    for i in range(len(monthly_dates)):
        date_c = monthly_dates[i]
        dose1_col = [(date_c, 'First Dose Administered')]
        dose2_col = [(date_c, 'Second Dose Administered')]
        dose1_df = dist_df[dose1_col]
        dose2_df = dist_df[dose2_col]
        dose1 = dose1_df.sum(axis=0)[0]
        dose2 = dose2_df.sum(axis=0)[0]
        d_month_df.loc[len(d_month_df.index)] = [dist, i+1, dose1, dose2]
    
    overall_date = end_date.strftime("%d/%m/%Y")
    dose1_col = [(overall_date, 'First Dose Administered')]
    dose2_col = [(overall_date, 'Second Dose Administered')]
    dose1_df = dist_df[dose1_col]
    dose2_df = dist_df[dose2_col]
    dose1 = dose1_df.sum(axis=0)[0]
    dose2 = dose2_df.sum(axis=0)[0]
    d_overall_df.loc[len(d_overall_df.index)] = [dist, overall_date, dose1, dose2]

d_week_df = d_week_df.sort_values(['districtid','timeid'], ascending=[True, True], axis=0)
d_month_df = d_month_df.sort_values(['districtid','timeid'], ascending=[True, True], axis=0)
d_overall_df = d_overall_df.sort_values(['districtid','timeid'], ascending=[True, True], axis=0)

d_week_filename = 'vaccinated-count-district-week.csv'
d_month_filename = 'vaccinated-count-district-month.csv'
d_overall_filename = 'vaccinated-count-district-overall.csv'

d_week_df.to_csv(OUTPUT_DIR+d_week_filename, index=False)
d_month_df.to_csv(OUTPUT_DIR+d_month_filename, index=False)
d_overall_df.to_csv(OUTPUT_DIR+d_overall_filename, index=False)

# state-wise data
skey = np.unique(cowin_df['State_Code'])
s_week_df = pd.DataFrame(columns=['stateid', 'timeid', 'dose1', 'dose2'])
s_month_df = pd.DataFrame(columns=['stateid', 'timeid', 'dose1', 'dose2'])
s_overall_df = pd.DataFrame(columns=['stateid', 'timeid', 'dose1', 'dose2'])

for state in skey:
    state_df = cowin_df[np.array(cowin_df['State_Code'] == state)]
    state_name = state_df['State'].iloc[0]
    state_name = state_name[0]
    for i in range(len(weekly_dates)):
        date_c = weekly_dates[i]
        dose1_col = [(date_c, 'First Dose Administered')]
        dose2_col = [(date_c, 'Second Dose Administered')]
        dose1_df = state_df[dose1_col]
        dose2_df = state_df[dose2_col]
        dose1 = dose1_df.sum(axis=0)[0]
        dose2 = dose2_df.sum(axis=0)[0]
        s_week_df.loc[len(s_week_df.index)] = [state, i+1, dose1, dose2]
    
    for i in range(len(monthly_dates)):
        date_c = monthly_dates[i]
        dose1_col = [(date_c, 'First Dose Administered')]
        dose2_col = [(date_c, 'Second Dose Administered')]
        dose1_df = state_df[dose1_col]
        dose2_df = state_df[dose2_col]
        dose1 = dose1_df.sum(axis=0)[0]
        dose2 = dose2_df.sum(axis=0)[0]
        s_month_df.loc[len(s_month_df.index)] = [state, i+1, dose1, dose2]
        
    overall_date = end_date.strftime("%d/%m/%Y")
    dose1_col = [(overall_date, 'First Dose Administered')]
    dose2_col = [(overall_date, 'Second Dose Administered')]
    dose1_df = state_df[dose1_col]
    dose2_df = state_df[dose2_col]
    dose1 = dose1_df.sum(axis=0)[0]
    dose2 = dose2_df.sum(axis=0)[0]
    s_overall_df.loc[len(s_overall_df.index)] = [state, overall_date, dose1, dose2]

s_week_df = s_week_df.sort_values(['stateid','timeid'], ascending=[True, True], axis=0)
s_month_df = s_month_df.sort_values(['stateid','timeid'], ascending=[True, True], axis=0)
s_overall_df = s_overall_df.sort_values(['stateid','timeid'], ascending=[True, True], axis=0)

s_week_filename = 'vaccinated-count-state-week.csv'
s_month_filename = 'vaccinated-count-state-month.csv'
s_overall_filename = 'vaccinated-count-state-overall.csv'

s_week_df.to_csv(OUTPUT_DIR+s_week_filename, index=False)
s_month_df.to_csv(OUTPUT_DIR+s_month_filename, index=False)
s_overall_df.to_csv(OUTPUT_DIR+s_overall_filename, index=False)

# below data is required for Q9
## Q9: Statewise last week vaccination count for dose1:
s_last_week_dose1 = pd.DataFrame(columns=['stateid', 'rate'])

for state in skey:
    state_df = cowin_df[np.array(cowin_df['State_Code'] == state)]
    date_1 = weekly_dates[len(weekly_dates)-1]
    date_2 = weekly_dates[len(weekly_dates)-2]
    date1_col = [(date_1, 'First Dose Administered')]
    date2_col = [(date_2, 'First Dose Administered')]
    date1_df = state_df[date1_col]
    date2_df = state_df[date2_col]
    date1_count = date1_df.sum(axis=0)[0]
    date2_count = date2_df.sum(axis=0)[0]
    s_last_week_dose1.loc[len(s_last_week_dose1.index)] = [state, date1_count-date2_count]

# print(s_last_week_dose1)
s_last_week_dose1.to_csv(INT_MED_DIR+'5-9-state-dose1.csv', index=False)