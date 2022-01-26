import pandas as pd
import numpy as np

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

literacy_india_df = pd.DataFrame(columns=['state/ut', 'literacy-group', 'percentage'])

literacy_df = pd.read_excel(INT_MED_DIR+'DDW2-C19-0000.xlsx', header = [0, 1])
literacy_df = literacy_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Educational level','Number speaking third language']]


state_keys = np.unique(literacy_df['Area Name'])

col_literacy_three_or_more = [('Number speaking third language', 'Persons')]

literacy_groups_list = ['Illiterate', 'Literate', 'Literate but below primary', 'Primary but below middle', 'Middle but below matric/secondary', 'Matric/Secondary but below graduate', 'Graduate and above']

for state in state_keys:
    state_literacy_df = literacy_df[np.array(literacy_df['Area Name'] == state)]

    # get total population for the state
    state_literacy_df = state_literacy_df[np.array(state_literacy_df['Total/Rural/Urban'] == 'Total')]
    total_literacy_df = state_literacy_df[np.array(state_literacy_df['Educational level'] == 'Total')]
    # print(state_literacy_df)
    total_three_or_more_df = total_literacy_df[col_literacy_three_or_more]
    # print("total_three_or_more_df",total_three_or_more_df)
    total_three_or_more = total_three_or_more_df.sum(axis=0)[0]

    literacy_dict = {}
    for literacy_group in literacy_groups_list:
        literacy_group_df = state_literacy_df[np.array(state_literacy_df['Educational level'] == literacy_group)]
        # print(state_literacy_df)
        literacy_group_three_or_more_df = literacy_group_df[col_literacy_three_or_more]
        # print("literacy_group", literacy_group)
        literacy_group_three_or_more = literacy_group_three_or_more_df.sum(axis=0)[0]
        # print("literacy_group_three_or_more",literacy_group_three_or_more)
        literacy_dict[literacy_group] = 100*literacy_group_three_or_more/total_three_or_more
    
    sorted_literacy_dict = {k: v for k, v in sorted(literacy_dict.items(), key=lambda item: item[1], reverse = True)}
    key_list = list(sorted_literacy_dict.keys())
    # print(key_list)
    literacy_india_df.loc[len(literacy_india_df.index)] = [state, key_list[0], sorted_literacy_dict[key_list[0]]]



literacy_india_df = literacy_india_df.sort_values(['state/ut'], ascending=True, axis=0)

literacy_india_filename = 'literacy-india.csv'

literacy_india_df.to_csv(OUTPUT_DIR+literacy_india_filename, index=False)