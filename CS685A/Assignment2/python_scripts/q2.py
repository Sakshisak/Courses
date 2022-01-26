import pandas as pd
import numpy as np
from scipy import stats

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

# part a - only 1
# part b - exactly 2
# part c - 3 or more languliteracys 

# define output file dataframes
percent_1 = pd.DataFrame(columns=['state/ut', 'male-percentage', 'female-percentage', 'p-value'])
percent_2 = pd.DataFrame(columns=['state/ut', 'male-percentage', 'female-percentage', 'p-value'])
percent_3 = pd.DataFrame(columns=['state/ut', 'male-percentage', 'female-percentage', 'p-value'])

# population dataframe
census_df = pd.read_excel(INPUT_DIR+'DDW_PCA0000_2011_Indiastatedist_updated.xlsx')
census_df = census_df[['Level', 'Name', 'TRU', 'TOT_P','TOT_F', 'TOT_M']]
census_df = census_df[((census_df['Level'] == 'STATE') | (census_df['Level'] == 'India'))]
census_df = census_df[(census_df['TRU'] == 'Total')]


# C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX 
language_df = pd.read_excel(INT_MED_DIR+'DDW2-C19-0000.xlsx', header = [0, 1])
language_df = language_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Educational level', 'Number speaking second language', 'Number speaking third language']]
language_df = language_df[np.array(language_df['Total/Rural/Urban'] == 'Total')]
language_df = language_df[np.array(language_df['Educational level'] == 'Total')]

# define cols for C-19
col_2_male = [('Number speaking second language', 'Males')]
col_2_female = [('Number speaking second language', 'Females')]
col_3_male = [('Number speaking third language', 'Males')]
col_3_female = [('Number speaking third language', 'Females')]

# get all state keys
state_keys = np.unique(census_df['Name'])

# p-value list of all states
pv_s_1 = {}
pv_s_2 = {}
pv_s_3 = {}
expected_v = {}

for state in state_keys:
    state_name = state
    if state == 'India':
        state_name = 'INDIA'
    
    state_census_df = census_df[np.array(census_df['Name'] == state)]
    state_language_df = language_df[np.array(language_df['Area Name'] == state_name)]

    tot_pop_male = state_census_df['TOT_M']
    tot_pop_male = tot_pop_male.sum(axis=0)
    tot_pop_female = state_census_df['TOT_F']
    tot_pop_female = tot_pop_female.sum(axis=0)

    pop_2_male = state_language_df[col_2_male]
    pop_2_male = pop_2_male.sum(axis=0)[0]
    pop_2_female = state_language_df[col_2_female]
    pop_2_female = pop_2_female.sum(axis=0)[0]

    pop_3_male = state_language_df[col_3_male]
    pop_3_male = pop_3_male.sum(axis=0)[0]
    pop_3_female = state_language_df[col_3_female]
    pop_3_female = pop_3_female.sum(axis=0)[0]

    p_1_male = tot_pop_male - pop_2_male
    p_2_male = pop_2_male - pop_3_male
    p_3_male = pop_3_male

    p_1_female = tot_pop_female - pop_2_female
    p_2_female = pop_2_female - pop_3_female
    p_3_female = pop_3_female

    per_1_m = 100*(p_1_male)/tot_pop_male
    per_2_m = 100*(p_2_male)/tot_pop_male
    per_3_m = 100*(p_3_male)/tot_pop_male
    per_1_f = 100*(p_1_female)/tot_pop_female
    per_2_f = 100*(p_2_female)/tot_pop_female
    per_3_f = 100*(p_3_female)/tot_pop_female

    expected = tot_pop_male/tot_pop_female

    ratio_1 = per_1_m/per_1_f
    ratio_2 = per_2_m/per_2_f
    ratio_3 = per_3_m/per_3_f

    exp = [expected]*3
    rat = [ratio_1,ratio_2,ratio_3]
    
    statistic, p_value = stats.ttest_ind(exp,rat)

    percent_1.loc[len(percent_1.index)] = [state, per_1_m, per_1_f, p_value]
    percent_2.loc[len(percent_2.index)] = [state, per_2_m, per_2_f, p_value]
    percent_3.loc[len(percent_3.index)] = [state, per_3_m, per_3_f, p_value]


# ---------- 3 or more -----------#
percent_3 = percent_3.sort_values(['state/ut'], ascending=True, axis=0)

percent_3_filename = 'gender-india-c.csv'

percent_3.to_csv(OUTPUT_DIR+percent_3_filename, index=False)

# ---------- exaclty 2 -----------#
percent_2 = percent_2.sort_values(['state/ut'], ascending=True, axis=0)

percent_2_filename = 'gender-india-b.csv'

percent_2.to_csv(OUTPUT_DIR+percent_2_filename, index=False)

# ---------- only 1 -----------#
percent_1 = percent_1.sort_values(['state/ut'], ascending=True, axis=0)

percent_1_filename = 'gender-india-a.csv'

percent_1.to_csv(OUTPUT_DIR+percent_1_filename, index=False)
