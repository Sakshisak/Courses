import numpy as np
import pandas as pd

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

cowin_df = pd.read_csv(INPUT_DIR+'cowin_vaccine_data_districtwise.csv', header = [0, 1])

cowin_df = cowin_df.fillna(0)

# columns for covishield and covaxin
col_covishield = [('14/08/2021', 'CoviShield (Doses Administered)')]
col_covaxin = [('14/08/2021', 'Covaxin (Doses Administered)')]

district_key = np.unique(cowin_df['District_Key'])
dist_ratio_df = pd.DataFrame(columns=['districtid', 'vaccineratio'])

# district wise data

for district in district_key:
    dist_vac_df = cowin_df[np.array(cowin_df['District_Key'] == district)]
    
    covaxin_row = dist_vac_df[col_covaxin]
    covaxin_sum = covaxin_row.sum(axis=0)[0]
    covishield_row = dist_vac_df[col_covishield]
    covishield_sum = covishield_row.sum(axis=0)[0]

    if covaxin_sum != 0:
        vac_ratio = covishield_sum/covaxin_sum

    if covaxin_sum != 0:
        dist_ratio_df.loc[len(dist_ratio_df.index)] = [district, vac_ratio]
    else:
        dist_ratio_df.loc[len(dist_ratio_df.index)] = [district, np.nan]

dist_ratio_df = dist_ratio_df.sort_values('vaccineratio', axis = 0)


# state-wise data
state_keys = np.unique(cowin_df['State'])
state_ratio_df = pd.DataFrame(columns=['stateid', 'vaccineratio'])

for state in state_keys:
    state_vaccine_data = cowin_df[np.array(cowin_df['State'] == state)]
    covaxin_row = state_vaccine_data[col_covaxin]
    covaxin_sum = covaxin_row.sum(axis=0)[0]
    covishield_row = state_vaccine_data[col_covishield]
    covishield_sum = covishield_row.sum(axis=0)[0]
    if covaxin_sum == 0:
        vac_ratio = 'NA'
    else:
        vac_ratio = covishield_sum/covaxin_sum

    if covaxin_sum != 0:
        state_ratio_df.loc[len(state_ratio_df.index)] = [state, vac_ratio]
    else:
        state_ratio_df.loc[len(state_ratio_df.index)] = [state, np.nan]

state_ratio_df = state_ratio_df.sort_values('vaccineratio', axis = 0)


# overall data
country = 'India'
overall_ratio_df = pd.DataFrame(columns=['countryid', 'vaccineratio'])
overall_vac_r = cowin_df
covaxin_row = overall_vac_r[col_covaxin]
covaxin_sum = covaxin_row.sum(axis=0)[0]
covishield_row = overall_vac_r[col_covishield]
covishield_sum = covishield_row.sum(axis=0)[0]
vac_ratio = covishield_sum/covaxin_sum

overall_ratio_df.loc[len(overall_ratio_df.index)] = [country, vac_ratio]


# printing to csv files
district_filename = 'vaccine-type-ratio-district.csv'
state_filename = 'vaccine-type-ratio-state.csv'
overall_filename = 'vaccine-type-ratio-overall.csv'

dist_ratio_df.to_csv(OUTPUT_DIR+district_filename, index=False)
state_ratio_df.to_csv(OUTPUT_DIR+state_filename, index=False)
overall_ratio_df.to_csv(OUTPUT_DIR+overall_filename, index=False)