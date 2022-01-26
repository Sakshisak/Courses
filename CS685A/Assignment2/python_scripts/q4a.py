import pandas as pd
import numpy as np

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

ratio_df = pd.DataFrame(columns=['state-name','3-to-2-ratio'])


# C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX 
language_df = pd.read_excel(INT_MED_DIR+'DDW2-C19-0000.xlsx', header = [0, 1])
language_df = language_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Educational level', 'Number speaking second language', 'Number speaking third language']]
language_df = language_df[np.array(language_df['Total/Rural/Urban'] == 'Total')]
language_df = language_df[np.array(language_df['Educational level'] == 'Total')]

state_ratio_map = {}

# define cols for C-19
col_2 = [('Number speaking second language', 'Persons')]
col_3 = [('Number speaking third language', 'Persons')]

# get all state keys
state_keys = np.unique(language_df['Area Name'])


for state in state_keys:
    state_language_df = language_df[np.array(language_df['Area Name'] == state)]

    pop_2 = state_language_df[col_2]
    pop_2 = pop_2.sum(axis=0)[0]
    pop_3 = state_language_df[col_3]
    pop_3 = pop_3.sum(axis=0)[0]

    ratio = pop_3/pop_2

    state_ratio_map[state] = ratio


state_ratio_map = dict(sorted(state_ratio_map.items(), key=lambda item: item[1]))
# print(state_ratio_map)
key_list = list(state_ratio_map.keys())

ratio_df.loc[len(ratio_df.index)] = [key_list[-1], state_ratio_map[key_list[-1]]]
ratio_df.loc[len(ratio_df.index)] = [key_list[-2], state_ratio_map[key_list[-2]]]
ratio_df.loc[len(ratio_df.index)] = [key_list[-3], state_ratio_map[key_list[-3]]]
ratio_df.loc[len(ratio_df.index)] = [key_list[0], state_ratio_map[key_list[0]]]
ratio_df.loc[len(ratio_df.index)] = [key_list[1], state_ratio_map[key_list[1]]]
ratio_df.loc[len(ratio_df.index)] = [key_list[2], state_ratio_map[key_list[2]]]


state_ratio_filename = '3-to-2-ratio.csv'
ratio_df.to_csv(OUTPUT_DIR+state_ratio_filename, index=False)
