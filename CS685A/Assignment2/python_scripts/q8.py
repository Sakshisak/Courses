import pandas as pd
import numpy as np
import csv

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

# part a - 3 or more languages
# part b - exactly 2
# part c - only 1


# dataframes for output files
age_india_df_1 = pd.DataFrame(columns=['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
age_india_df_2 = pd.DataFrame(columns=['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])
age_india_df_3 = pd.DataFrame(columns=['state/ut', 'age-group-males', 'ratio-males', 'age-group-females', 'ratio-females'])

# data from C-18 Population By Bilingualism, Trilingualism, Age And Sex
age_df = pd.read_excel(INT_MED_DIR+'DDW2-C18-0000.xlsx', header = [0, 1])
age_df = age_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Age-group','Number speaking second language', 'Number speaking third language']]

# age group population data from DDW2-0000C-14.xls
pop_age_group_df = pd.read_excel(INT_MED_DIR+'DDW2-0000C-14.xls', header = [0, 1])
pop_age_group_df = pop_age_group_df[['State Code', 'Area Name', 'Age-group', 'Total']]

# create a mapping from state_keys to pop_state_keys
state_key_map = {}
pop_state_keys = np.unique(pop_age_group_df['Area Name'])
for state in pop_state_keys:
    if(state == 'India'):
        state_orig = 'INDIA'
    else:
        state_orig = state[8:]
        state_orig = state_orig[:-5]
    state_key_map[state_orig] = state

# print(state_key_map)

# get all state keys
state_keys = np.unique(age_df['Area Name'])

col_3_male = [('Number speaking third language', 'Males')]
col_3_female = [('Number speaking third language', 'Females')]
col_2_male = [('Number speaking second language', 'Males')]
col_2_female = [('Number speaking second language', 'Females')]

pop_male_col = [('Total', 'Males')]
pop_female_col = [('Total', 'Females')]

age_groups_list = ['5-9', '10-14', '15-19', '20-24', '25-29', '30-49', '50-69', '70+']
pop_age_groups_list = ['5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39','40-44', '45-49','50-54', '55-59','60-64', '65-69','70-74', '75-79','80+']

for state in state_keys:
    state_age_df = age_df[np.array(age_df['Area Name'] == state)]

    # get total population for the state
    state_age_df = state_age_df[np.array(state_age_df['Total/Rural/Urban'] == 'Total')]
    total_age_df = state_age_df[np.array(state_age_df['Age-group'] == 'Total')]
    # print(state_age_df)
    total_3_male_df = total_age_df[col_3_male]
    total_3_female_df = total_age_df[col_3_female]
    total_3_male = total_3_male_df.sum(axis=0)[0]
    total_3_female = total_3_female_df.sum(axis=0)[0]

    total_2_male_df = total_age_df[col_2_male]
    total_2_female_df = total_age_df[col_2_female]
    total_2_male = total_2_male_df.sum(axis=0)[0]
    total_2_female = total_2_female_df.sum(axis=0)[0]

    # get population of all age-groups in this state
    state_name = state_key_map[state]

    state_pop_age_df = pop_age_group_df[np.array(pop_age_group_df['Area Name'] == state_name)]
    
    total_pop_age_df = state_pop_age_df[np.array(state_pop_age_df['Age-group'] == 'All ages')]

    # total population for each state all age groups
    pop_male_total = total_pop_age_df[pop_male_col]
    pop_female_total = total_pop_age_df[pop_female_col]
    total_1_male = pop_male_total.sum(axis=0)[0]
    total_1_female = pop_female_total.sum(axis=0)[0]

    # population for each age group in the state
    pop_ag_state_male_dict = {}
    pop_ag_state_female_dict = {}

    for age_g in pop_age_groups_list:
        ag_pop_age_df = state_pop_age_df[np.array(state_pop_age_df['Age-group'] == age_g)] 

        pop_male_ag = ag_pop_age_df[pop_male_col]
        pop_female_ag = ag_pop_age_df[pop_female_col]
        pop_male_ag = pop_male_ag.sum(axis=0)[0]
        pop_female_ag = pop_female_ag.sum(axis=0)[0]
        pop_ag_state_male_dict[age_g] = pop_male_ag
        pop_ag_state_female_dict[age_g] = pop_female_ag
    
    age_group_state_male_dict = {}
    age_group_state_female_dict = {}

    # getting age-group data for original age-groups
    age_group_state_male_dict['5-9'] = pop_ag_state_male_dict['5-9']
    age_group_state_male_dict['10-14'] = pop_ag_state_male_dict['10-14']
    age_group_state_male_dict['15-19'] = pop_ag_state_male_dict['15-19']
    age_group_state_male_dict['20-24'] = pop_ag_state_male_dict['20-24']
    age_group_state_male_dict['25-29'] = pop_ag_state_male_dict['25-29']
    age_group_state_male_dict['30-49'] = pop_ag_state_male_dict['30-34'] + pop_ag_state_male_dict['35-39'] + pop_ag_state_male_dict['40-44'] + pop_ag_state_male_dict['45-49']
    age_group_state_male_dict['50-69'] = pop_ag_state_male_dict['50-54'] + pop_ag_state_male_dict['55-59'] + pop_ag_state_male_dict['60-64'] + pop_ag_state_male_dict['65-69']
    age_group_state_male_dict['70+'] = pop_ag_state_male_dict['70-74'] + pop_ag_state_male_dict['75-79'] + pop_ag_state_male_dict['80+'] 

    age_group_state_female_dict['5-9'] = pop_ag_state_female_dict['5-9']
    age_group_state_female_dict['10-14'] = pop_ag_state_female_dict['10-14']
    age_group_state_female_dict['15-19'] = pop_ag_state_female_dict['15-19']
    age_group_state_female_dict['20-24'] = pop_ag_state_female_dict['20-24']
    age_group_state_female_dict['25-29'] = pop_ag_state_female_dict['25-29']
    age_group_state_female_dict['30-49'] = pop_ag_state_female_dict['30-34'] + pop_ag_state_female_dict['35-39'] + pop_ag_state_female_dict['40-44'] + pop_ag_state_female_dict['45-49']
    age_group_state_female_dict['50-69'] = pop_ag_state_female_dict['50-54'] + pop_ag_state_female_dict['55-59'] + pop_ag_state_female_dict['60-64'] + pop_ag_state_female_dict['65-69']
    age_group_state_female_dict['70+'] = pop_ag_state_female_dict['70-74'] + pop_ag_state_female_dict['75-79'] + pop_ag_state_female_dict['80+']


    # dict of age-group & ratio for each category
    age_dict_3_male = {}
    age_dict_3_female = {}
    age_dict_2_male = {}
    age_dict_2_female = {}
    age_dict_1_male = {}
    age_dict_1_female = {}

    for age_group in age_groups_list:
        age_group_df = state_age_df[np.array(state_age_df['Age-group'] == age_group)]

        # ---------- 3 or more -----------#
        age_group_3_male_df = age_group_df[col_3_male]
        age_group_3_female_df = age_group_df[col_3_female]

        age_group_3_male = age_group_3_male_df.sum(axis=0)[0]
        age_dict_3_male[age_group] = age_group_3_male/total_3_male
        age_group_3_female = age_group_3_female_df.sum(axis=0)[0]
        age_dict_3_female[age_group] = age_group_3_female/total_3_female

        # ---------- exaclty 2 -----------#
        age_group_2_male_df = age_group_df[col_2_male]
        age_group_2_female_df = age_group_df[col_2_female]

        age_group_2_male_orig = age_group_2_male_df.sum(axis=0)[0]
        age_group_2_male = age_group_2_male_orig - age_group_3_male
        age_dict_2_male[age_group] = age_group_2_male/(total_2_male-total_3_male)
        age_group_2_female_orig = age_group_2_female_df.sum(axis=0)[0]
        age_group_2_female = age_group_2_female_orig - age_group_3_female
        age_dict_2_female[age_group] = age_group_2_female/(total_2_female-total_3_female)

        # ---------- only 1 --------------#
        age_dict_1_male[age_group] = (age_group_state_male_dict[age_group]-age_group_2_male_orig)/(total_1_male-total_2_male)
        age_dict_1_female[age_group] = (age_group_state_female_dict[age_group]-age_group_2_female_orig)/(total_1_female-total_2_female)
    
    # ---------- 3 or more -----------#
    sorted_age_dict_3_male = {k: v for k, v in sorted(age_dict_3_male.items(), key=lambda item: item[1], reverse = True)}
    sorted_age_dict_3_female = {k: v for k, v in sorted(age_dict_3_female.items(), key=lambda item: item[1], reverse = True)}
    key_list_3_male = list(sorted_age_dict_3_male.keys())
    key_list_3_female = list(sorted_age_dict_3_female.keys())

    age_india_df_3.loc[len(age_india_df_3.index)] = [state, key_list_3_male[0], sorted_age_dict_3_male[key_list_3_male[0]], key_list_3_female[0], sorted_age_dict_3_female[key_list_3_female[0]]]

    # ---------- exaclty 2 -----------#
    sorted_age_dict_2_male = {k: v for k, v in sorted(age_dict_2_male.items(), key=lambda item: item[1], reverse = True)}
    sorted_age_dict_2_female = {k: v for k, v in sorted(age_dict_2_female.items(), key=lambda item: item[1], reverse = True)}
    key_list_2_male = list(sorted_age_dict_2_male.keys())
    key_list_2_female = list(sorted_age_dict_2_female.keys())

    age_india_df_2.loc[len(age_india_df_2.index)] = [state, key_list_2_male[0], sorted_age_dict_2_male[key_list_2_male[0]], key_list_2_female[0], sorted_age_dict_2_female[key_list_2_female[0]]]

    # ---------- only 1 -----------#
    sorted_age_dict_1_male = {k: v for k, v in sorted(age_dict_1_male.items(), key=lambda item: item[1], reverse = True)}
    sorted_age_dict_1_female = {k: v for k, v in sorted(age_dict_1_female.items(), key=lambda item: item[1], reverse = True)}
    key_list_1_male = list(sorted_age_dict_1_male.keys())
    key_list_1_female = list(sorted_age_dict_1_female.keys())

    age_india_df_1.loc[len(age_india_df_1.index)] = [state, key_list_1_male[0], sorted_age_dict_1_male[key_list_1_male[0]], key_list_1_female[0], sorted_age_dict_1_female[key_list_1_female[0]]]


# ---------- 3 or more -----------#
age_india_df_3 = age_india_df_3.sort_values(['state/ut'], ascending=True, axis=0)

age_india_3_filename = 'age-gender-a.csv'

age_india_df_3.to_csv(OUTPUT_DIR+age_india_3_filename, index=False)

# ---------- exaclty 2 -----------#
age_india_df_2 = age_india_df_2.sort_values(['state/ut'], ascending=True, axis=0)

age_india_2_filename = 'age-gender-b.csv'

age_india_df_2.to_csv(OUTPUT_DIR+age_india_2_filename, index=False)

# ---------- only 1 -----------#
age_india_df_1 = age_india_df_1.sort_values(['state/ut'], ascending=True, axis=0)

age_india_1_filename = 'age-gender-c.csv'

age_india_df_1.to_csv(OUTPUT_DIR+age_india_1_filename, index=False)