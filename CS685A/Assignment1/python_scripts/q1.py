import pandas as pd
import numpy as np
import json
import re

INPUT_DIR = '../covid_files/'
INT_MED_DIR = '../intermediate_files/'
OUTPUT_DIR = '../outputs/'

json_file = open(INPUT_DIR+'neighbor-districts.json')
neighbor_districts_json = json.load(json_file)

# remove given districts from neighbor districts json dataset
# also removing bijapur_district as it is not present in the csv files.
removed_districts = ['kheri', 'konkan_division', 'niwari', 'noklak', 'parbhani', 'pattanamtitta', 'bijapur_district']
removed_districts_with_codes = set()
for d in neighbor_districts_json:
  for d1 in removed_districts:
    x = "^{}.*".format(d1)
    if re.search(x, d):
      removed_districts_with_codes.add(d)

# renaming districts with same name to include their state code so they can be distinguished later
renamed = {
    "bilaspur/Q1478939" : "HP_Bilaspur",
    "bilaspur/Q100157" : "CT_Bilaspur",
    "aurangabad/Q43086" : "BR_Aurangabad",
    "aurangabad/Q592942" : "MH_Aurangabad",
    "hamirpur/Q2086180" : "HP_Hamirpur",
    "hamirpur/Q2019757" : "UP_Hamirpur",
    "pratapgarh/Q1473962" : "UP_Pratapgarh",
    "pratapgarh/Q1585433" : "RJ_Pratapgarh",
    "balrampur/Q1948380" : "UP_Balrampur",
    "balrampur/Q16056268" : "CT_Balrampur"
}

# print(len(neighbor_districts_json))
temp_dict = {}
for d in list(neighbor_districts_json):
  if d in removed_districts_with_codes:
    continue
  else:
    lst = []
    for x in list(neighbor_districts_json[d]):
      if x in removed_districts_with_codes:
        continue
      elif x in renamed:
        lst.append(renamed[x])
      else:
        lst.append(x)
  key = d
  if d in renamed.keys():
    key = renamed[d]
  temp_dict[key] = lst
# print(len(temp_dict))

merged_districts = [
    "central_delhi/Q107941",
    "west_delhi/Q549807",
    "south_east_delhi/Q25553535",
    "east_delhi/Q107960",
    "north_east_delhi/Q429329",
    "north_west_delhi/Q766125",
    "shahdara/Q83486",
    "north_delhi/Q693367",
    "new_delhi/Q987",
    "south_delhi/Q2061938",
    "south_west_delhi/Q2379189"
]
merged_list = set()
for d in list(temp_dict):
  if d in merged_districts:
    for d1 in temp_dict[d]:
      if d1 not in merged_districts:
        merged_list.add(d1)
    del temp_dict[d]
  else:
    f = False
    for d1 in temp_dict[d]:
      if d1 in merged_districts:
        f = True
    if f:
      lst = []
      for d1 in temp_dict[d]:
        if d1 not in merged_districts:
          lst.append(d1)
      del temp_dict[d]
      temp_dict[d] = lst
temp_dict["DL_Delhi"] = list(merged_list)
renamed["new_delhi/Q987"] = "DL_Delhi"
# print(len(temp_dict))

spel_df = pd.read_csv(INT_MED_DIR+'City-renaming.csv', dtype=object)
spel_dic = {}

# Replace Spaces with underscore
spel_df['District wise'].replace(' ', '_', regex=True, inplace=True)
# all in lower case
spel_df['District wise'] = spel_df['District wise'].str.lower()

# Replace Spaces with underscore
spel_df['Neighbor json'].replace(' ', '_', regex=True, inplace=True)
# all in lower case 
spel_df['Neighbor json'] = spel_df['Neighbor json'].str.lower()

# y = old name, x = new name
for x,y in zip(spel_df['District wise'], spel_df['Neighbor json']):
    spel_dic[y] = x

new_dict = {}
for d in list(temp_dict):
  l = []
  for x in temp_dict[d]:
    y = x.split("/")[0]
    y = y.split("_district")[0]
    if y in spel_dic.keys():
      # print("renaming {} to {}".format(y, spel_dic[y]))
      y = spel_dic[y]
    l.append(y)
  d1 = d.split("/")[0]
  d1 = d1.split("_district")[0]
  if d1 in spel_dic.keys():
      d1 = spel_dic[d1]
  new_dict[d1] = l
# print(new_dict)

cowin_file = INPUT_DIR+'cowin_vaccine_data_districtwise.csv'

cowin_df = pd.read_csv(cowin_file, dtype=object)
# filter cols
cowin_cols = ['State_Code',	'State', 'District_Key', 'District']
cowin_df = cowin_df[cowin_cols]
# remove na values
cowin_df.dropna(inplace=True)
# remove duplicates
cowin_df = cowin_df.drop_duplicates(subset=['District_Key'])
# remove invalid districts
invalid_cowin_districts = ['Chengalpattu', 'Gaurela Pendra Marwahi', 'Nicobars', 'North and Middle Andaman', 'Saraikela-Kharsawan', 'South Andaman', 'Tenkasi', 'Tirupathur', 'Yanam']
cowin_df = cowin_df[~cowin_df['District'].isin(invalid_cowin_districts)]
# Replace Spaces with underscore
cowin_df['District'].replace(' ', '_', regex=True, inplace=True)
# convert all to lowercase
cowin_df['District'] = cowin_df['District'].str.lower()
# print(cowin_df)

districts_file = INPUT_DIR+'districts.xlsx'
districts_df = pd.read_excel(districts_file, dtype=object)

districts_cols = ['State', 'District']
districts_df = districts_df[districts_cols]
# Remove NA values
districts_df.dropna(inplace=True)
# Remove Duplicates
districts_df = districts_df.drop_duplicates(subset=['District', 'State'])
# Remove Unknown values for District field
districts_df.drop(districts_df.index[districts_df['District'] == "Unknown"], inplace=True)
# Lowercase
districts_df['District'] = districts_df['District'].str.lower()

# Creating list of all districts that exist in districts.csv as well as cowin_vaccine.csv
cowin_not_in_districts = list(set(cowin_df['District']) - set(districts_df['District']))

# Taking the intersection of vaccine data districts and districts
cowin_df = cowin_df[~cowin_df['District'].isin(cowin_not_in_districts)]
cowin_df.loc[len(cowin_df.index)] = ['DL', 'Delhi', 'DL_Delhi', 'delhi']

neighbor_districts_modified = {}

for new_dict_key in new_dict.keys():
  
  value = []
  key = ""

  if new_dict_key in renamed.values():
    key = new_dict_key
  else:
    keys = cowin_df['District_Key'].values[cowin_df['District'] == new_dict_key]
    if len(keys) == 0:
      continue
    else:
      key = keys[0]
  
  for y in new_dict[new_dict_key]:
    value_entry = ""
    if y in renamed.values():
      value_entry = y
    else:
      value_entry = cowin_df['District_Key'].values[cowin_df['District'] == y]
      if len(value_entry) == 0:
        continue
      else:
        value_entry = value_entry[0]
    value.append(value_entry)

  neighbor_districts_modified[key] = sorted(value)

neighbor_districts_modified = dict(sorted(neighbor_districts_modified.items()))

# Serializing json 
json_object = json.dumps(neighbor_districts_modified, indent = 4)
  
# Writing to neighbor-districts-modified.json
with open(OUTPUT_DIR+'neighbor-districts-modified.json', 'w') as outfile:
    outfile.write(json_object)

# add a column district key to districts in districts.csv to create modified-district.csv
state_code_map = {
    'Andhra Pradesh': 'AP',
    'Arunachal Pradesh': 'AR',
    'Assam':'AS',
    'Bihar':'BR',
    'Chandigarh':'CH',
    'Chhattisgarh':'CT',
    'Delhi':'DL',
    'Goa':'GA',
    'Gujarat':'GJ',
    'Himachal Pradesh':'HP',
    'Haryana':'HR',
    'Jharkhand':'JH',
    'Jammu and Kashmir':'JK',
    'Karnataka':'KA',
    'Kerala':'KL',
    'Ladakh':'LA',
    'Maharashtra':'MH',
    'Meghalaya':'ML',
    'Manipur':'MN',
    'Madhya Pradesh':'MP',
    'Mizoram':'MZ',
    'Odisha':'OR',
    'Punjab':'PB',
    'Puducherry':'PY',
    'Rajasthan':'RJ',
    'Telangana':'TG',
    'Tamil Nadu':'TN',
    'Tripura':'TR',
    'Uttar Pradesh':'UP',
    'Uttarakhand':'UT',
    'West Bengal':'WB',
    'Andaman and Nicobar Islands':'AN',
    'Nagaland':'NL',
    'Dadra and Nagar Haveli and Daman and Diu':'DN',
    'Sikkim': 'SK',
    'Lakshadweep': 'LD'
    }

dist_key_list = []
districts_modified_df = pd.read_excel(districts_file, dtype=object)
for ind in districts_modified_df.index:
    state = districts_modified_df['State'][ind]
    district = districts_modified_df['District'][ind]
    district_id = state_code_map[state]+"_"+district
    dist_key_list.append(district_id)

districts_modified_df['District_Id'] = dist_key_list
districts_modified_df.to_csv(INT_MED_DIR+'districts-modified.csv', index=False)