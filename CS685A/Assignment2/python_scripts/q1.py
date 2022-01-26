import pandas as pd
import numpy as np

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

# define output dataframe
state_percent = pd.DataFrame(columns=['state-name','percent-one', 'percent-two', 'percent-three'])


# population dataframe
census_df = pd.read_excel(INPUT_DIR+'DDW_PCA0000_2011_Indiastatedist_updated.xlsx')
census_df = census_df[['Level', 'Name', 'TRU', 'TOT_P']]
census_df = census_df[((census_df['Level'] == 'STATE') | (census_df['Level'] == 'India'))]
census_df = census_df[(census_df['TRU'] == 'Total')]


# C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX 
language_df = pd.read_excel(INT_MED_DIR+'DDW2-C19-0000.xlsx', header = [0, 1])
language_df = language_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Educational level', 'Number speaking second language', 'Number speaking third language']]
language_df = language_df[np.array(language_df['Total/Rural/Urban'] == 'Total')]
language_df = language_df[np.array(language_df['Educational level'] == 'Total')]

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

    tot_pop = state_census_df['TOT_P']
    tot_pop = tot_pop.sum(axis=0)

    pop_2 = state_language_df[col_2]
    pop_2 = pop_2.sum(axis=0)[0]
    pop_3 = state_language_df[col_3]
    pop_3 = pop_3.sum(axis=0)[0]

    p_1 = 100*(tot_pop - pop_2)/tot_pop
    p_2 = 100*(pop_2 - pop_3)/tot_pop
    p_3 = 100*pop_3/tot_pop

    state_percent.loc[len(state_percent.index)] = [state, p_1, p_2, p_3]

state_percent = state_percent.sort_values(['state-name'], ascending=True, axis=0)

state_percent_filename = 'percent-india.csv'

state_percent.to_csv(OUTPUT_DIR+state_percent_filename, index=False)

