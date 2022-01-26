import numpy as np
import pandas as pd

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

cowin_df = pd.read_csv(INPUT_DIR+'cowin_vaccine_data_districtwise.csv', header = [0, 1])
census_df = pd.read_excel(INPUT_DIR+'DDW_PCA0000_2011_Indiastatedist_updated.xlsx')
census_df = census_df[['State', 'District', 'Level', 'Name', 'TRU', 'TOT_P']]

# using this function for matching and renaming districts in census data & vaccine data 
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

rename_city = pd.read_csv(INT_MED_DIR+'City-renaming.csv')
rename_census = pd.read_csv(INT_MED_DIR+'census-rename.csv')

cowin_df = cowin_df.fillna(0)
col_dose1 = [('14/08/2021', 'First Dose Administered')]
col_dose2 = [('14/08/2021', 'Second Dose Administered')]

district_key = np.unique(cowin_df['District_Key'])

dist_ratio_df = pd.DataFrame(columns=['districtid', 'vaccinateddose1ratio', 'vaccinateddose2ratio', 'Total Population'])

for district in district_key:
    dist_df = cowin_df[np.array(cowin_df['District_Key'] == district)]
    dname = dist_df['District'].iloc[0]
    dname = dname[0]

    dose1_row = dist_df[col_dose1]
    dose1_sum = dose1_row.sum(axis=0)[0]
    dose2_row = dist_df[col_dose2]
    dose2_sum = dose2_row.sum(axis=0)[0]

    if dname.lower() in ['bilaspur', 'aurangabad', 'hamirpur', 'pratapgarh', ]:
      dname = district

    c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
    c_rename['Name'] = c_rename['Name'].str.strip()
    c_rename['Name'] = c_rename['Name'].str.lower()
    c_rename = c_rename[(c_rename['Name'] == dname.lower())]
    c_rename = c_rename[(c_rename['TRU'] == 'Total')]   
    
    if c_rename.empty:
        rename_list = np.array(rename_city['District wise'])
        if dname.lower() in rename_list:
            renamed_dist = rename_city[rename_city['District wise'] == dname.lower()]
            re_name = renamed_dist['Neighbor json']
            re_name = re_name.iloc[0]
            c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == re_name)]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
        
        # If not found above, using algorithmic correction upto 2 characters
        if c_rename.empty:
            for name in np.unique(census_df['Name']):
                if levenshteinDistance(name.lower(), dname.lower()) < 2:
                    c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
                    c_rename['Name'] = c_rename['Name'].str.strip()
                    c_rename['Name'] = c_rename['Name'].str.lower()
                    c_rename = c_rename[(c_rename['Name'] == name.lower())]
                    c_rename = c_rename[(c_rename['TRU'] == 'Total')]
                    break
                elif levenshteinDistance(name.lower(), dname.lower()) < 3 and name[0] == dname[0]:
                    c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
                    c_rename['Name'] = c_rename['Name'].str.strip()
                    c_rename['Name'] = c_rename['Name'].str.lower()
                    c_rename = c_rename[(c_rename['Name'] == name.lower())]
                    c_rename = c_rename[(c_rename['TRU'] == 'Total')]
                    break
                
                
            # If not found in city-rename, use census-rename.csv 
            if c_rename.empty:
                rename_list = np.array(rename_census['District'])
                if dname in rename_list:
                    renamed_dist = rename_census[rename_census['District'] == dname]
                    re_name = renamed_dist['Census District']
                    re_name = re_name.iloc[0]
                    c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
                    c_rename['Name'] = c_rename['Name'].str.strip()
                    c_rename['Name'] = c_rename['Name'].str.lower()
                    c_rename = c_rename[(c_rename['Name'] == re_name.lower())]
                    c_rename = c_rename[(c_rename['TRU'] == 'Total')]
                # drop otherwise
                if c_rename.empty:
                    continue
    
    tot_pop = (c_rename['TOT_P'].iloc[0])

    dose1_ratio = dose1_sum/tot_pop
    dose2_ratio = dose2_sum/tot_pop

    dist_ratio_df.loc[len(dist_ratio_df.index)] = [district, dose1_ratio, dose2_ratio, tot_pop]

dist_ratio_df = dist_ratio_df.sort_values('vaccinateddose1ratio', axis = 0)

state_keys = np.unique(cowin_df['State'])


state_ratio_df = pd.DataFrame(columns=['stateid', 'vaccinateddose1ratio', 'vaccinateddose2ratio', 'Total Population'])

for state in state_keys:
    state_vaccine_data = cowin_df[np.array(cowin_df['State'] == state)]

    dose1_row = state_vaccine_data[col_dose1]
    dose1_sum = dose1_row.sum(axis=0)[0]
    dose2_row = state_vaccine_data[col_dose2]
    dose2_sum = dose2_row.sum(axis=0)[0]

    vaccination_ratio = dose2_sum/dose1_sum

    c_rename = census_df[(census_df['Level'] == 'STATE')]
    c_rename['Name'] = c_rename['Name'].str.strip()
    c_rename['Name'] = c_rename['Name'].str.lower()
    c_rename = c_rename[(c_rename['Name'] == state.lower())]
    c_rename = c_rename[(c_rename['TRU'] == 'Total')]   
    tot_pop = 0
    if c_rename.empty:
        if state == 'Dadra and Nagar Haveli and Daman and Diu':
            name1 = 'DADRA & NAGAR HAVELI'
            name2 = 'DAMAN & DIU'
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name1.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            tot_pop = (c_rename['TOT_P'].iloc[0])
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name2.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            tot_pop = tot_pop + (c_rename['TOT_P'].iloc[0])

        elif state == 'Ladakh':
            name1 = 'Leh(Ladakh)'
            name2 = 'Kargil'
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name1.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            tot_pop = (c_rename['TOT_P'].iloc[0])
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name2.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            tot_pop = tot_pop + (c_rename['TOT_P'].iloc[0])
        else:
            rename_list = {
                'Andaman and Nicobar Islands': 'ANDAMAN & NICOBAR ISLANDS',
                'Delhi': 'NCT OF DELHI',
                'Jammu and Kashmir': 'JAMMU & KASHMIR',
                'Telangana': 'ANDHRA PRADESH'
            }
            re_name = rename_list[state]
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == re_name.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            if c_rename.empty:
                continue

    if state != 'Dadra and Nagar Haveli and Daman and Diu' and state != 'Ladakh':
        tot_pop = (c_rename['TOT_P'].iloc[0])

    dose1_ratio = dose1_sum/tot_pop
    dose2_ratio = dose2_sum/tot_pop
    stateid = cowin_df[np.array(cowin_df['State']==state)]
    stateid = stateid['State_Code'].iloc[0]
    state_ratio_df.loc[len(state_ratio_df.index)] = [stateid[0], dose1_ratio, dose2_ratio, tot_pop]

state_ratio_df = state_ratio_df.sort_values('vaccinateddose1ratio', axis = 0)

country = 'India'

overall_ratio_df = pd.DataFrame(columns=['overallid', 'vaccinateddose1ratio', 'vaccinateddose2ratio', 'Total Population'])

overall_vaccine_data = cowin_df

dose1_row = overall_vaccine_data[col_dose1]
dose1_sum = dose1_row.sum(axis=0)[0]
dose2_row = overall_vaccine_data[col_dose2]
dose2_sum = dose2_row.sum(axis=0)[0]

c_rename = census_df[(census_df['Level'] == 'India')]
c_rename = c_rename[(c_rename['TRU'] == 'Total')]

tot_pop = (c_rename['TOT_P'].iloc[0])

dose1_ratio = dose1_sum/tot_pop
dose2_ratio = dose2_sum/tot_pop

overall_ratio_df.loc[len(overall_ratio_df.index)] = [country, dose1_ratio, dose2_ratio, tot_pop]

# printing to csv files
district_filename = 'vaccinated-dose-ratio-district.csv'
state_filename = 'vaccinated-dose-ratio-state.csv'
overall_filename = 'vaccinated-dose-ratio-overall.csv'

dist_ratio_df.to_csv(OUTPUT_DIR+district_filename, index=False)
state_ratio_df.to_csv(OUTPUT_DIR+state_filename, index=False)
overall_ratio_df.to_csv(OUTPUT_DIR+overall_filename, index=False)