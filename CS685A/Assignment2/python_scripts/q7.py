import pandas as pd
import numpy as np
from itertools import chain

INPUT_DIR = '../input_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../output_files/'

# define output dataframe
data_a = pd.DataFrame(columns=['region','language-1', 'language-2', 'language-3'])
data_b = pd.DataFrame(columns=['region','language-1', 'language-2', 'language-3'])

# define intermediate dataframe
data_int_med = pd.DataFrame(columns=['state', 'lang', 'pop_lang_1', 'pop_lang_2', 'pop_lang_3'])


languages_list = ['ASSAMESE', 'BENGALI', 'BODO', 'DOGRI', 'GUJARATI', 'HINDI', 'KANNADA', 'KASHMIRI', 'KONKANI','MAITHILI', 'MALAYALAM','MANIPURI','MARATHI', 'NEPALI', 'ODIA','PUNJABI','SANSKRIT','SANTALI','SINDHI','TAMIL','TELUGU','URDU','ADI','AFGHANI/KABULI/PASHTO','ANAL','ANGAMI','AO','ARABIC/ARBI','BALTI','BHILI/BHILODI','BHOTIA','BHUMIJ','BISHNUPURIYA','CHAKHESANG','CHAKRU/CHOKRI','CHANG','COORGI/KODAGU','DEORI','DIMASA','ENGLISH','GADABA','GANGTE','GARO','GONDI','HALABI','HALAM','HMAR','HO','JATAPU','JUANG','KABUI','KARBI/MIKIR','KHANDESHI','KHARIA','KHASI','KHEZHA']

# C-17-0000 India Languages dataframe
lang_df = pd.read_excel(INT_MED_DIR+'DDW2-C17-0000.xlsx', header=[0,1])
lang_df = lang_df[['State name', 'Total speakers of languages', '1st language', '2nd language']]


# cols for C-17 series
col_lang_1 = [('Total speakers of languages', 'Name')]
col_lang_2 = [('1st language', 'Name')]
col_lang_3 = [('2nd language', 'Name')]

col_1 = ('Total speakers of languages', 'Persons')
col_2 = ('1st language', 'Persons')
col_3 = ('2nd language', 'Persons')

# extract list of languages
languages_set = set(languages_list)

lang_1_df = lang_df[col_lang_1]
lang_2_df = lang_df[col_lang_2]
lang_3_df = lang_df[col_lang_3]

lang_1_df = lang_1_df.dropna()
lang_2_df = lang_2_df.dropna()
lang_3_df = lang_3_df.dropna()

list_ini_1 = lang_1_df[col_lang_1].values
flatten_list_1 = list(chain.from_iterable(list_ini_1))
flatten_list_1 = [x.strip() for x in flatten_list_1]

list_ini_2 = lang_2_df[col_lang_2].values
flatten_list_2 = list(chain.from_iterable(list_ini_2))
flatten_list_2 = [x.strip() for x in flatten_list_2]

list_ini_3 = lang_3_df[col_lang_3].values
flatten_list_3 = list(chain.from_iterable(list_ini_3))
flatten_list_3 = [x.strip() for x in flatten_list_3]

# print(lang_1_df,lang_2_df,lang_3_df)

languages_set.update(flatten_list_1)
languages_set.update(flatten_list_2)
languages_set.update(flatten_list_3)

languages_list = list(languages_set)

state_keys = []

for i in range(1,36):
    int_2 = format(i, '02d')
    state_lang_df = pd.read_excel(INT_MED_DIR+'c172/DDW2-C17-'+int_2+'00.XLSX', header=[0,1])
    state_lang_df = state_lang_df[['State name', 'Total speakers of languages', '1st language', '2nd language']]
    state_lang_df = state_lang_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # get the state name
    state_name = state_lang_df['State name'].values
    state_name = (list(chain.from_iterable(state_name)))[0]
    # print(state_name)
    state_keys.append(state_name)


    for lang in languages_list:
        lang_1_df = state_lang_df[np.array(state_lang_df[col_lang_1] == lang)]
        pop_lang_1 = lang_1_df[col_1]
        pop_lang_1 = pop_lang_1.sum(axis=0)
        # print(lang, pop_lang_1)
        
        lang_2_df = state_lang_df[np.array(state_lang_df[col_lang_2] == lang)]
        pop_lang_2 = lang_2_df[col_2]
        pop_lang_2 = pop_lang_2.sum(axis=0)
        # print(lang, pop_lang_2)

        lang_3_df = state_lang_df[np.array(state_lang_df[col_lang_3] == lang)]
        pop_lang_3 = lang_3_df[col_3]
        pop_lang_3 = pop_lang_3.sum(axis=0)

        data_int_med.loc[len(data_int_med.index)] = [state_name, lang, pop_lang_1, pop_lang_2, pop_lang_3]

# regions:
'''
• North: JK, Ladakh, PN, HP, HR, UK, Delhi, Chandigarh
• West: RJ, GJ, MH, Goa, Dadra & Nagar Haveli, Daman & Diu
• Central: MP, UP, CG
• East: BH, WB, OR, JH
• South: KT, TG, AP, TN, KL, Lakshadweep, Puducherry
• North-East: AS, SK, MG, TR, AR, MN, NG, MZ, Andaman & Nicobar
'''
region_dict = {}
region_dict['North'] = ['JAMMU & KASHMIR','HIMACHAL PRADESH', 'PUNJAB', 'HARYANA', 'UTTARAKHAND', 'NCT OF DELHI', 'CHANDIGARH']
region_dict['West'] = ['RAJASTHAN', 'GUJARAT', 'MAHARASHTRA', 'GOA', 'DADRA & NAGAR HAVELI', 'DAMAN & DIU']
region_dict['Central'] = ['MADHYA PRADESH', 'UTTAR PRADESH', 'CHHATTISGARH']
region_dict['East'] = ['BIHAR', 'WEST BENGAL', 'ODISHA', 'JHARKHAND']
region_dict['South'] = ['KARNATAKA', 'TAMIL NADU','ANDHRA PRADESH','KERALA', 'LAKSHADWEEP', 'PUDUCHERRY']
region_dict['North-East'] = ['ASSAM','SIKKIM', 'MEGHALAYA', 'MANIPUR', 'TRIPURA', 'ARUNACHAL PRADESH', 'MIZORAM', 'NAGALAND', 'ANDAMAN & NICOBAR ISLANDS']

# ------------ Part a solution ----------------#
for region, reg_list in region_dict.items():

    states_data_int_med_0 = data_int_med[np.array(data_int_med['state'] == reg_list[0])]
    state_data_part_a_df_0 = states_data_int_med_0[['lang', 'pop_lang_1']]
    total_data_df_part_a = state_data_part_a_df_0

    for i in range(1,len(reg_list)):
        state = reg_list[i]
        states_data_int_med = data_int_med[np.array(data_int_med['state'] == state)]
        state_data_part_a_df = states_data_int_med[['lang', 'pop_lang_1']]
        total_data_df_part_a = pd.concat((total_data_df_part_a,state_data_part_a_df)).groupby('lang',as_index=False).sum()
    
    if region == 'North-East':
        result = total_data_df_part_a.sort_values(['pop_lang_1'], ascending=False, axis=0)
        # print(result)
    result = total_data_df_part_a.sort_values(['pop_lang_1'], ascending=False, axis=0).head(3)
    data_a.loc[len(data_a.index)] = [region, result.iloc[0].lang, result.iloc[1].lang, result.iloc[2].lang]
 
# ------------ Part b solution ----------------#
for region, reg_list in region_dict.items():

    states_data_int_med_0 = data_int_med[np.array(data_int_med['state'] == reg_list[0])]
    state_data_part_b_df_0 = states_data_int_med_0[['lang', 'pop_lang_1', 'pop_lang_2', 'pop_lang_3']]
    state_sum_col_0 = state_data_part_b_df_0['pop_lang_1']+state_data_part_b_df_0['pop_lang_2']+state_data_part_b_df_0['pop_lang_3']
    state_data_part_b_df_0['sum'] = state_sum_col_0
    total_data_df_part_b = state_data_part_b_df_0[['lang','sum']]

    for i in range(1,len(reg_list)):
        state = reg_list[i]
        states_data_int_med = data_int_med[np.array(data_int_med['state'] == state)]
        state_data_part_b_df = states_data_int_med[['lang', 'pop_lang_1', 'pop_lang_2', 'pop_lang_3']]
        state_sum_col = state_data_part_b_df['pop_lang_1']+state_data_part_b_df['pop_lang_2']+state_data_part_b_df['pop_lang_3']
        state_data_part_b_df['sum'] = state_sum_col
        state_data_part_b_df = state_data_part_b_df[['lang','sum']]
        total_data_df_part_b = pd.concat((total_data_df_part_b,state_data_part_b_df)).groupby('lang',as_index=False).sum()

    result = total_data_df_part_b.sort_values(['sum'], ascending=False, axis=0).head(3)
    data_b.loc[len(data_b.index)] = [region, result.iloc[0].lang, result.iloc[1].lang, result.iloc[2].lang]


# ---------- Part a -----------#
data_a_filename = 'region-india-a.csv'

data_a.to_csv(OUTPUT_DIR+data_a_filename, index=False)

# ---------- Part b -----------#
data_b_filename = 'region-india-b.csv'

data_b.to_csv(OUTPUT_DIR+data_b_filename, index=False)