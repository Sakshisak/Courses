import pandas as pd
import numpy as np
from scipy import stats

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

# part a - only 1
# part b - exactly 2
# part c - 3 or more languages 

# define output file dataframes
geo_1 = pd.DataFrame(columns=['state/ut', 'urban-percentage', 'rural-percentage', 'p-value'])
geo_2 = pd.DataFrame(columns=['state/ut', 'urban-percentage', 'rural-percentage', 'p-value'])
geo_3 = pd.DataFrame(columns=['state/ut', 'urban-percentage', 'rural-percentage', 'p-value'])

# population dataframe
census_df = pd.read_excel(INPUT_DIR+'DDW_PCA0000_2011_Indiastatedist_updated.xlsx')
census_df = census_df[['Level', 'Name', 'TRU', 'TOT_P']]
census_df = census_df[((census_df['Level'] == 'STATE') | (census_df['Level'] == 'India'))]


# C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX 
language_df = pd.read_excel(INT_MED_DIR+'DDW2-C19-0000.xlsx', header = [0, 1])
language_df = language_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Educational level', 'Number speaking second language', 'Number speaking third language']]
language_df = language_df[np.array(language_df['Educational level'] == 'Total')]
language_df = language_df[np.array(language_df['Total/Rural/Urban'] != 'Total')]

# define cols for C-19
col_2 = [('Number speaking second language', 'Persons')]
col_3 = [('Number speaking third language', 'Persons')]

# get all state keys
state_keys = np.unique(census_df['Name'])

for state in state_keys:
    state_name = state
    if state == 'India':
        state_name = 'INDIA'
    
    state_census_df = census_df[np.array(census_df['Name'] == state)]
    state_language_df = language_df[np.array(language_df['Area Name'] == state_name)]
    state_language_rural_df = state_language_df[np.array(state_language_df['Total/Rural/Urban'] == 'Rural')]
    state_language_urban_df = state_language_df[np.array(state_language_df['Total/Rural/Urban'] == 'Urban')]

    tot_pop_rural_df = state_census_df[(state_census_df['TRU'] == 'Rural')]
    tot_pop_rural_df = tot_pop_rural_df['TOT_P']
    tot_pop_rural = tot_pop_rural_df.sum(axis=0)

    tot_pop_urban_df = state_census_df[(state_census_df['TRU'] == 'Urban')]
    tot_pop_urban_df = tot_pop_urban_df['TOT_P']
    tot_pop_urban = tot_pop_urban_df.sum(axis=0)
    
    tot_pop_df = state_census_df['TOT_P']

    pop_2_rural = state_language_rural_df[col_2]
    pop_2_rural = pop_2_rural.sum(axis=0)[0]
    pop_2_urban = state_language_urban_df[col_2]
    pop_2_urban = pop_2_urban.sum(axis=0)[0]

    pop_3_rural = state_language_rural_df[col_3]
    pop_3_rural = pop_3_rural.sum(axis=0)[0]
    pop_3_urban = state_language_urban_df[col_3]
    pop_3_urban = pop_3_urban.sum(axis=0)[0]

    p_1_rural = tot_pop_rural - pop_2_rural
    p_2_rural = pop_2_rural - pop_3_rural
    p_3_rural = pop_3_rural

    p_1_urban = tot_pop_urban - pop_2_urban
    p_2_urban = pop_2_urban - pop_3_urban
    p_3_urban = pop_3_urban

    per_1_r = 100*(p_1_rural)/tot_pop_rural
    per_2_r = 100*(p_2_rural)/tot_pop_rural
    per_3_r = 100*(p_3_rural)/tot_pop_rural
    per_1_u = 100*(p_1_urban)/tot_pop_urban
    per_2_u = 100*(p_2_urban)/tot_pop_urban
    per_3_u = 100*(p_3_urban)/tot_pop_urban

    expected = tot_pop_urban/tot_pop_rural

    ratio_1 = per_1_u/per_1_r
    ratio_2 = per_2_u/per_2_r
    ratio_3 = per_3_u/per_3_r

    exp = [expected]*3
    rat = [ratio_1,ratio_2,ratio_3]
    
    statistic, p_value = stats.ttest_ind(exp,rat)

    geo_1.loc[len(geo_1.index)] = [state, per_1_u, per_1_r, p_value]
    geo_2.loc[len(geo_2.index)] = [state, per_2_u, per_2_r, p_value]
    geo_3.loc[len(geo_3.index)] = [state, per_3_u, per_3_r, p_value]



# ---------- 3 or more -----------#
geo_3 = geo_3.sort_values(['state/ut'], ascending=True, axis=0)

geo_3_filename = 'geography-india-c.csv'

geo_3.to_csv(OUTPUT_DIR+geo_3_filename, index=False)

# ---------- exaclty 2 -----------#
geo_2 = geo_2.sort_values(['state/ut'], ascending=True, axis=0)

geo_2_filename = 'geography-india-b.csv'

geo_2.to_csv(OUTPUT_DIR+geo_2_filename, index=False)

# ---------- only 1 -----------#
geo_1 = geo_1.sort_values(['state/ut'], ascending=True, axis=0)

geo_1_filename = 'geography-india-a.csv'

geo_1.to_csv(OUTPUT_DIR+geo_1_filename, index=False)