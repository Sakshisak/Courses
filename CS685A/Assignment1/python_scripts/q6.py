import numpy as np
import pandas as pd

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

cowin_df = pd.read_csv(INPUT_DIR+'cowin_vaccine_data_districtwise.csv', header = [0, 1])
census_df = pd.read_excel(INPUT_DIR+'DDW_PCA0000_2011_Indiastatedist_updated.xlsx')
census_df = census_df[['State', 'District', 'Level', 'Name', 'TRU', 'TOT_F', 'TOT_M']]

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
col_male = [('14/08/2021', 'Male(Individuals Vaccinated)')]
col_female = [('14/08/2021', 'Female(Individuals Vaccinated)')]

district_key = np.unique(cowin_df['District_Key'])

ratio_district_df = pd.DataFrame(columns=['districtid', 'vaccinationratio', 'populationratio', 'ratio of ratios'])

for district in district_key:
  # All rows corresponding a district key
    dist_vaccine_df = cowin_df[np.array(cowin_df['District_Key'] == district)]
    d_name = dist_vaccine_df['District'].iloc[0]
    d_name = d_name[0]

    # Columns from dist_vaccine_df which contail male and female people vaccinated in a district
    male_df = dist_vaccine_df[col_male]
    male_sum = male_df.sum(axis=0)[0]
    female_df = dist_vaccine_df[col_female]
    female_sum = female_df.sum(axis=0)[0]

    # Ratio of Females vaccinated to Males vaccinated
    ratio_vac = female_sum/male_sum

    # Manually replacing districts with same name in one or more states them with district key in census data
    if d_name.lower() in ['bilaspur', 'aurangabad', 'hamirpur', 'pratapgarh']:
      d_name = district

    c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
    c_rename['Name'] = c_rename['Name'].str.strip()
    c_rename['Name'] = c_rename['Name'].str.lower()
    c_rename = c_rename[(c_rename['Name'] == d_name.lower())]
    c_rename = c_rename[(c_rename['TRU'] == 'Total')]   
    if c_rename.empty:
       # If not found then check if map exists in City rename.csv
        rename_list = np.array(rename_city['District wise'])
        if d_name.lower() in rename_list:
            renamed_dist = rename_city[rename_city['District wise'] == d_name.lower()]
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
                if levenshteinDistance(name.lower(), d_name.lower()) < 2:
                    c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
                    c_rename['Name'] = c_rename['Name'].str.strip()
                    c_rename['Name'] = c_rename['Name'].str.lower()
                    c_rename = c_rename[(c_rename['Name'] == name.lower())]
                    c_rename = c_rename[(c_rename['TRU'] == 'Total')]
                    break
                elif levenshteinDistance(name.lower(), d_name.lower()) < 3 and name[0] == d_name[0]:
                    c_rename = census_df[(census_df['Level'] == 'DISTRICT')]
                    c_rename['Name'] = c_rename['Name'].str.strip()
                    c_rename['Name'] = c_rename['Name'].str.lower()
                    c_rename = c_rename[(c_rename['Name'] == name.lower())]
                    c_rename = c_rename[(c_rename['TRU'] == 'Total')]
                    break
            if c_rename.empty:
              # If not found in city-rename, use census-rename.csv 
                rename_list = np.array(rename_census['District'])
                if d_name in rename_list:
                    renamed_dist = rename_census[rename_census['District'] == d_name]
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

    male_population = (c_rename['TOT_M'].iloc[0])
    female_population = (c_rename['TOT_F'].iloc[0])
    ratio_population = female_population/male_population
    vac_to_pop_ratio = ratio_vac/ratio_population
    ratio_district_df.loc[len(ratio_district_df.index)] = [district, ratio_vac, ratio_population, vac_to_pop_ratio]

ratio_district_df = ratio_district_df.sort_values('ratio of ratios', axis = 0)
# print(ratio_district_df)

state_keys = np.unique(cowin_df['State'])
ratio_state_df = pd.DataFrame(columns=['stateid', 'vaccinationratio', 'populationratio', 'ratio of ratios'])

for state in state_keys:
    state_vaccine_data = cowin_df[np.array(cowin_df['State'] == state)]
    male_df = state_vaccine_data[col_male]
    male_sum = male_df.sum(axis=0)[0]
    female_df = state_vaccine_data[col_female]
    female_sum = female_df.sum(axis=0)[0]
    ratio_vac = female_sum/male_sum
    c_rename = census_df[(census_df['Level'] == 'STATE')]
    c_rename['Name'] = c_rename['Name'].str.strip()
    c_rename['Name'] = c_rename['Name'].str.lower()
    c_rename = c_rename[(c_rename['Name'] == state.lower())]
    c_rename = c_rename[(c_rename['TRU'] == 'Total')]   
    male_population = 0
    female_population = 0
    if c_rename.empty:
        # Manually creating list of changed names from census 2011 data and vaccination data
        if state == 'Dadra and Nagar Haveli and Daman and Diu':
            name1 = 'DADRA & NAGAR HAVELI'
            name2 = 'DAMAN & DIU'
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name1.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            male_population = (c_rename['TOT_M'].iloc[0])
            female_population = (c_rename['TOT_F'].iloc[0])
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name2.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            male_population = male_population + (c_rename['TOT_M'].iloc[0])
            female_population = female_population + (c_rename['TOT_F'].iloc[0])
        
        elif state == 'Ladakh':
            name1 = 'Leh(Ladakh)'
            name2 = 'Kargil'
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name1.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            male_population = (c_rename['TOT_M'].iloc[0])
            female_population = (c_rename['TOT_F'].iloc[0])
            c_rename = census_df
            c_rename['Name'] = c_rename['Name'].str.strip()
            c_rename['Name'] = c_rename['Name'].str.lower()
            c_rename = c_rename[(c_rename['Name'] == name2.lower())]
            c_rename = c_rename[(c_rename['TRU'] == 'Total')]
            male_population = male_population + (c_rename['TOT_M'].iloc[0])
            female_population = female_population + (c_rename['TOT_F'].iloc[0])
            
        else:
            rename_list = {
                'Andaman and Nicobar Islands': 'ANDAMAN & NICOBAR ISLANDS',
                'Delhi': 'NCT OF DELHI',
                'Jammu and Kashmir': 'JAMMU & KASHMIR',
                'Telangana': 'ANDHRA PRADESH' # Assuming Telangana proportional in size with Andhra Pradesh
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
        male_population = (c_rename['TOT_M'].iloc[0])
        female_population = (c_rename['TOT_F'].iloc[0])
    ratio_population = female_population/male_population
    vac_to_pop_ratio = ratio_vac/ratio_population
    ratio_state_df.loc[len(ratio_state_df.index)] = [state, ratio_vac, ratio_population, vac_to_pop_ratio]

ratio_state_df = ratio_state_df.sort_values('ratio of ratios', axis = 0)
# print(ratio_state_df)

country = 'India'
ratio_country_df = pd.DataFrame(columns=['overallid', 'vaccinationratio', 'populationratio', 'ratio of ratios'])
country_vac_r = cowin_df
male_df = country_vac_r[col_male]
male_sum = male_df.sum(axis=0)[0]
female_df = country_vac_r[col_female]
female_sum = female_df.sum(axis=0)[0]
ratio_vac = female_sum/male_sum
c_rename = census_df[(census_df['Level'] == 'India')]
c_rename = c_rename[(c_rename['TRU'] == 'Total')] 
male_population = (c_rename['TOT_M'].iloc[0])
female_population = (c_rename['TOT_F'].iloc[0])
ratio_population = female_population/male_population
vac_to_pop_ratio = ratio_vac/ratio_population
ratio_country_df.loc[len(ratio_country_df.index)] = [country, ratio_vac, ratio_population, vac_to_pop_ratio]

# print(ratio_country_df)

district_filename = 'vaccination-population-ratio-district.csv'
state_filename = 'vaccination-population-ratio-state.csv'
overall_filename = 'vaccination-population-ratio-country.csv'

ratio_district_df.to_csv(OUTPUT_DIR+district_filename, index=False)
ratio_state_df.to_csv(OUTPUT_DIR+state_filename, index=False)
ratio_country_df.to_csv(OUTPUT_DIR+overall_filename, index=False)
