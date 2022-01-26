import pandas as pd
import numpy as np
import csv

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

# part a - 3 or more languliteracys
# part b - exactly 2
# part c - only 1


# dataframes for output files
literacy_india_df_1 = pd.DataFrame(columns=['state/ut', 'literacy-group-males', 'ratio-males', 'literacy-group-females', 'ratio-females'])
literacy_india_df_2 = pd.DataFrame(columns=['state/ut', 'literacy-group-males', 'ratio-males', 'literacy-group-females', 'ratio-females'])
literacy_india_df_3 = pd.DataFrame(columns=['state/ut', 'literacy-group-males', 'ratio-males', 'literacy-group-females', 'ratio-females'])


# data from C-19 POPULATION BY BILINGUALISM, TRILINGUALISM, EDUCATIONAL LEVEL AND SEX
literacy_df = pd.read_excel(INT_MED_DIR+'DDW2-C19-0000.xlsx', header = [0, 1])
literacy_df = literacy_df[['State code', 'Area Name', 'Total/Rural/Urban', 'Educational level','Number speaking second language', 'Number speaking third language']]
# get only total(residency) data
literacy_df = literacy_df[np.array(literacy_df['Total/Rural/Urban'] == 'Total')]


# C-8  EDUCATIONAL LEVEL BY AGE AND SEX FOR POPULATION AGE 7 AND ABOVE - 2011
pop_literacy_group_df = pd.read_excel(INT_MED_DIR+'DDW2-0000C-08.xlsx', header = [0,1,2])
pop_literacy_group_df = pop_literacy_group_df[['State Code', 'Area Name', 'Total/Rural/Urban', 'Age-group', 'Total','Illiterate','Literate','Educational level']]
# get only total(residency) and all ages data
pop_literacy_group_df = pop_literacy_group_df[np.array(pop_literacy_group_df['Total/Rural/Urban'] == 'Total')]
pop_literacy_group_df = pop_literacy_group_df[np.array(pop_literacy_group_df['Age-group'] == 'All ages')]


# get all state keys
state_keys = np.unique(literacy_df['Area Name'])

# create a mapping from state_keys to pop_state_keys
state_key_map = {}
pop_state_keys = np.unique(pop_literacy_group_df['Area Name'])
for state in pop_state_keys:
    if(state == 'INDIA'):
        state_orig = 'INDIA'
    else:
        state_orig = state[8:]
    state_key_map[state_orig] = state


# define columns for C-19
col_3_male = [('Number speaking third language', 'Males')]
col_3_female = [('Number speaking third language', 'Females')]
col_2_male = [('Number speaking second language', 'Males')]
col_2_female = [('Number speaking second language', 'Females')]

pop_male_col = [('Total', 'Males')]
pop_female_col = [('Total', 'Females')]


# define literacy groups for both dataframes
literacy_groups_list = ['Illiterate', 'Literate', 'Literate but below primary', 'Primary but below middle', 'Middle but below matric/secondary', 'Matric/Secondary but below graduate', 'Graduate and above']

pop_literacy_groups_list = [ 'Literate without educational level', 'Below primary', 'Primary', 'Middle', 'Matric/Secondary', 'Higher secondary/Intermediate/Pre-University/Senior secondary', 'Non-technical diploma or certificate not equal to degree', 'Technical diploma or certificate not equal to degree ', 'Graduate & above'] # 'Illiterate', 'Literate' left as they are columns on their own


for state in state_keys:
    state_literacy_df = literacy_df[np.array(literacy_df['Area Name'] == state)]

    # get total population for the state
    total_literacy_df = state_literacy_df[np.array(state_literacy_df['Educational level'] == 'Total')]
    # print(state_literacy_df)
    total_3_male_df = total_literacy_df[col_3_male]
    total_3_female_df = total_literacy_df[col_3_female]
    total_3_male = total_3_male_df.sum(axis=0)[0]
    total_3_female = total_3_female_df.sum(axis=0)[0]

    total_2_male_df = total_literacy_df[col_2_male]
    total_2_female_df = total_literacy_df[col_2_female]
    total_2_male = total_2_male_df.sum(axis=0)[0]
    total_2_female = total_2_female_df.sum(axis=0)[0]

    # get population of all age-groups in this state
    state_name = state_key_map[state]

    state_pop_literacy_df = pop_literacy_group_df[np.array(pop_literacy_group_df['Area Name'] == state_name)]


    # total population for each state all age groups
    pop_male_total = state_pop_literacy_df.loc[:, (['Total'],slice(None),['Males'])]
    pop_female_total = state_pop_literacy_df.loc[:, (['Total'],slice(None),['Females'])]
    total_1_male = pop_male_total.sum(axis=0)[0]
    total_1_female = pop_female_total.sum(axis=0)[0]
    # print(state, total_1_male, total_1_female)

    # population for each educational group in the state
    pop_el_state_male_dict = {}
    pop_el_state_female_dict = {}

    # for Literate , Illiterate
    pop_male_literate = state_pop_literacy_df.loc[:, (['Literate'], slice(None),['Males'])]
    pop_female_literate = state_pop_literacy_df.loc[:, (['Literate'], slice(None),['Females'])]
    pop_male_literate = pop_male_literate.sum(axis=0)[0]
    pop_female_literate = pop_female_literate.sum(axis=0)[0]

    pop_el_state_male_dict['Literate'] = pop_male_literate
    pop_el_state_female_dict['Literate'] = pop_female_literate

    pop_male_illiterate = state_pop_literacy_df.loc[:, (['Illiterate'], slice(None),['Males'])]
    pop_female_illiterate = state_pop_literacy_df.loc[:, (['Illiterate'], slice(None),['Females'])]
    pop_male_illiterate = pop_male_illiterate.sum(axis=0)[0]
    pop_female_illiterate = pop_female_illiterate.sum(axis=0)[0]

    pop_el_state_male_dict['Illiterate'] = pop_male_illiterate
    pop_el_state_female_dict['Illiterate'] = pop_female_illiterate

    for education_level in pop_literacy_groups_list:
        pop_male_el = state_pop_literacy_df.loc[:, (['Educational level'], [education_level],['Males'])].iloc[0]
        pop_female_el = state_pop_literacy_df.loc[:, (['Educational level'], [education_level],['Females'])].iloc[0]
        pop_male_el = pop_male_el.sum(axis=0)
        pop_female_el = pop_female_el.sum(axis=0)
        pop_el_state_male_dict[education_level] = pop_male_el
        pop_el_state_female_dict[education_level] = pop_female_el
    # print(pop_el_state_male_dict)
    # print(pop_el_state_female_dict)
    
    education_level_state_male_dict = {}
    education_level_state_female_dict = {}

    # getting literacy data for original literacy groups
    education_level_state_male_dict['Illiterate'] = pop_el_state_male_dict['Illiterate']
    education_level_state_male_dict['Literate'] = pop_el_state_male_dict['Literate']
    education_level_state_male_dict['Literate but below primary'] = pop_el_state_male_dict['Literate without educational level']+ pop_el_state_male_dict['Below primary']
    education_level_state_male_dict['Primary but below middle'] = pop_el_state_male_dict['Primary']
    education_level_state_male_dict['Middle but below matric/secondary'] = pop_el_state_male_dict['Middle']
    education_level_state_male_dict['Matric/Secondary but below graduate'] = pop_el_state_male_dict['Matric/Secondary'] + pop_el_state_male_dict['Higher secondary/Intermediate/Pre-University/Senior secondary'] + pop_el_state_male_dict['Non-technical diploma or certificate not equal to degree'] + pop_el_state_male_dict['Technical diploma or certificate not equal to degree ']
    education_level_state_male_dict['Graduate and above'] = pop_el_state_male_dict['Graduate & above']

    education_level_state_female_dict['Illiterate'] = pop_el_state_female_dict['Illiterate']
    education_level_state_female_dict['Literate'] = pop_el_state_female_dict['Literate']
    education_level_state_female_dict['Literate but below primary'] = pop_el_state_female_dict['Literate without educational level']+ pop_el_state_female_dict['Below primary']
    education_level_state_female_dict['Primary but below middle'] = pop_el_state_female_dict['Primary']
    education_level_state_female_dict['Middle but below matric/secondary'] = pop_el_state_female_dict['Middle']
    education_level_state_female_dict['Matric/Secondary but below graduate'] = pop_el_state_female_dict['Matric/Secondary'] + pop_el_state_female_dict['Higher secondary/Intermediate/Pre-University/Senior secondary'] + pop_el_state_female_dict['Non-technical diploma or certificate not equal to degree'] + pop_el_state_female_dict['Technical diploma or certificate not equal to degree ']
    education_level_state_female_dict['Graduate and above'] = pop_el_state_female_dict['Graduate & above']

    # print(education_level_state_male_dict)
    # print(education_level_state_female_dict)

    # dict of educational level & ratio for each category
    literacy_dict_3_male = {}
    literacy_dict_3_female = {}
    literacy_dict_2_male = {}
    literacy_dict_2_female = {}
    literacy_dict_1_male = {}
    literacy_dict_1_female = {}

    for literacy_group in literacy_groups_list:
        literacy_group_df = state_literacy_df[np.array(state_literacy_df['Educational level'] == literacy_group)]

        # ---------- 3 or more -----------#
        literacy_group_3_male_df = literacy_group_df[col_3_male]
        literacy_group_3_female_df = literacy_group_df[col_3_female]

        literacy_group_3_male = literacy_group_3_male_df.sum(axis=0)[0]
        literacy_dict_3_male[literacy_group] = literacy_group_3_male/total_3_male
        literacy_group_3_female = literacy_group_3_female_df.sum(axis=0)[0]
        literacy_dict_3_female[literacy_group] = literacy_group_3_female/total_3_female

        # ---------- exaclty 2 -----------#
        literacy_group_2_male_df = literacy_group_df[col_2_male]
        literacy_group_2_female_df = literacy_group_df[col_2_female]

        literacy_group_2_male_orig = literacy_group_2_male_df.sum(axis=0)[0]
        literacy_group_2_male = literacy_group_2_male_orig - literacy_group_3_male
        literacy_dict_2_male[literacy_group] = literacy_group_2_male/(total_2_male-total_3_male)
        literacy_group_2_female_orig = literacy_group_2_female_df.sum(axis=0)[0]
        literacy_group_2_female = literacy_group_2_female_orig - literacy_group_3_female
        literacy_dict_2_female[literacy_group] = literacy_group_2_female/(total_2_female-total_3_female)

        # ---------- only 1 --------------#
        literacy_dict_1_male[literacy_group] = (education_level_state_male_dict[literacy_group]-literacy_group_2_male_orig)/(total_1_male-total_2_male)
        literacy_dict_1_female[literacy_group] = (education_level_state_female_dict[literacy_group]-literacy_group_2_female_orig)/(total_1_female-total_2_female)
    
    # ---------- 3 or more -----------#
    sorted_literacy_dict_3_male = {k: v for k, v in sorted(literacy_dict_3_male.items(), key=lambda item: item[1], reverse = True)}
    sorted_literacy_dict_3_female = {k: v for k, v in sorted(literacy_dict_3_female.items(), key=lambda item: item[1], reverse = True)}
    key_list_3_male = list(sorted_literacy_dict_3_male.keys())
    key_list_3_female = list(sorted_literacy_dict_3_female.keys())

    literacy_india_df_3.loc[len(literacy_india_df_3.index)] = [state, key_list_3_male[0], sorted_literacy_dict_3_male[key_list_3_male[0]], key_list_3_female[0], sorted_literacy_dict_3_female[key_list_3_female[0]]]

    # ---------- exaclty 2 -----------#
    sorted_literacy_dict_2_male = {k: v for k, v in sorted(literacy_dict_2_male.items(), key=lambda item: item[1], reverse = True)}
    sorted_literacy_dict_2_female = {k: v for k, v in sorted(literacy_dict_2_female.items(), key=lambda item: item[1], reverse = True)}
    key_list_2_male = list(sorted_literacy_dict_2_male.keys())
    key_list_2_female = list(sorted_literacy_dict_2_female.keys())

    literacy_india_df_2.loc[len(literacy_india_df_2.index)] = [state, key_list_2_male[0], sorted_literacy_dict_2_male[key_list_2_male[0]], key_list_2_female[0], sorted_literacy_dict_2_female[key_list_2_female[0]]]

    # ---------- only 1 -----------#
    sorted_literacy_dict_1_male = {k: v for k, v in sorted(literacy_dict_1_male.items(), key=lambda item: item[1], reverse = True)}
    sorted_literacy_dict_1_female = {k: v for k, v in sorted(literacy_dict_1_female.items(), key=lambda item: item[1], reverse = True)}
    key_list_1_male = list(sorted_literacy_dict_1_male.keys())
    key_list_1_female = list(sorted_literacy_dict_1_female.keys())

    literacy_india_df_1.loc[len(literacy_india_df_1.index)] = [state, key_list_1_male[0], sorted_literacy_dict_1_male[key_list_1_male[0]], key_list_1_female[0], sorted_literacy_dict_1_female[key_list_1_female[0]]]

    
# ---------- 3 or more -----------#
literacy_india_df_3 = literacy_india_df_3.sort_values(['state/ut'], ascending=True, axis=0)

literacy_india_3_filename = 'literacy-gender-a.csv'

literacy_india_df_3.to_csv(OUTPUT_DIR+literacy_india_3_filename, index=False)

# ---------- exaclty 2 -----------#
literacy_india_df_2 = literacy_india_df_2.sort_values(['state/ut'], ascending=True, axis=0)

literacy_india_2_filename = 'literacy-gender-b.csv'

literacy_india_df_2.to_csv(OUTPUT_DIR+literacy_india_2_filename, index=False)

# ---------- only 1 -----------#
literacy_india_df_1 = literacy_india_df_1.sort_values(['state/ut'], ascending=True, axis=0)

literacy_india_1_filename = 'literacy-gender-c.csv'

literacy_india_df_1.to_csv(OUTPUT_DIR+literacy_india_1_filename, index=False)