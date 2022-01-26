import pandas as pd
import numpy as np

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'


age_india_df = pd.DataFrame(columns=['state/ut', 'age-group', 'percentage'])

age_df = pd.read_excel(INT_MED_DIR+'DDW2-C18-0000.xlsx', header = [0, 1])
age_df = age_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Age-group', 'Number speaking third language']]

state_keys = np.unique(age_df['Area Name'])
col_age_three_or_more = [('Number speaking third language', 'Persons')]

age_groups_list = ['5-9', '10-14', '15-19', '20-24', '25-29', '30-49', '50-69', '70+']

for state in state_keys:
    state_age_df = age_df[np.array(age_df['Area Name'] == state)]

    # get total population for the state
    state_age_df = state_age_df[np.array(state_age_df['Total/Rural/Urban'] == 'Total')]
    total_age_df = state_age_df[np.array(state_age_df['Age-group'] == 'Total')]
    # print(state_age_df)
    total_three_or_more_df = total_age_df[col_age_three_or_more]
    # print("total_three_or_more_df",total_three_or_more_df)
    total_three_or_more = total_three_or_more_df.sum(axis=0)[0]

    age_dict = {}
    for age_group in age_groups_list:
        age_group_df = state_age_df[np.array(state_age_df['Age-group'] == age_group)]
        # print(state_age_df)
        age_group_three_or_more_df = age_group_df[col_age_three_or_more]
        # print("age_group", age_group)
        # print("age_group_three_or_more_df",age_group_three_or_more_df)
        age_group_three_or_more = age_group_three_or_more_df.sum(axis=0)[0]
        age_dict[age_group] = 100*age_group_three_or_more/total_three_or_more
    
    sorted_age_dict = {k: v for k, v in sorted(age_dict.items(), key=lambda item: item[1], reverse = True)}
    key_list = list(sorted_age_dict.keys())
    # print(key_list)
    age_india_df.loc[len(age_india_df.index)] = [state, key_list[0], sorted_age_dict[key_list[0]]]

age_india_df = age_india_df.sort_values(['state/ut'], ascending=True, axis=0)

age_india_filename = 'age-india.csv'

age_india_df.to_csv(OUTPUT_DIR+age_india_filename, index=False)


    
