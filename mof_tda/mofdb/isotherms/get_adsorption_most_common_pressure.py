"""
Get the adsorptions for the most common pressures from the isotherms.
"""
import json
import os
import csv
from typing import List

# first let's see if we can search by pressure, and just return the adsorption for that.
# Then we automate it

"""
with open("mof_tda/mofdb/isotherms/page_2.json") as f:
    isotherms_data = json.loads(f.read())

isotherms_dict = {doc['adsorbent']['name']: doc for doc in isotherms_data}

print(isotherms_dict)

from collections import defaultdict
store_adsorptions = defaultdict(list)

for index, mof in enumerate(isotherms_dict):
    # build in getting rid of Xe/Kr?
    store_temp_adsorption_values = []
    pressures = [isotherm_point['pressure'] for isotherm_point in isotherms_dict[mof]['isotherm_data']]
    #if pressures == [65.0, 100.0]: # most common CH4 isotherm
    if pressures == [3]: # most common n2 isotherm
        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
            store_temp_adsorption_values.extend([isotherm_point['total_adsorption']])
        store_adsorptions[mof].append(store_temp_adsorption_values)
"""
# automate by most common isotherm

path = "mof_tda/mofdb/isotherms"

from collections import defaultdict
store_adsorptions_ch4_main = defaultdict(list)
store_adsorptions_ch4_second = defaultdict(list)
store_adsorptions_n2_main = defaultdict(list)
store_adsorptions_n2_second = defaultdict(list)
store_adsorptions_h2 = defaultdict(list)
store_adsorptions_co2 = defaultdict(list)

for fname in os.listdir(path):
    if fname.startswith("page_"):
        split_fname = fname.split('_')[1] # get the number.sjon, e.g. 1.json
        get_num = split_fname.split('.')[0] #store the page number

        with open(path + "/" + fname) as f:
            isotherms_data = json.loads(f.read())

            # create a dict based on the mof name
            isotherms_dict = {doc['adsorbent']['name']: doc for doc in isotherms_data}

            for index, mof in enumerate(isotherms_dict):
                if len(isotherms_dict[mof]['adsorbates']) > 1: # skip xe/kr
                    continue
                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'CH4':
                    pressures = set([isotherm_point['pressure'] for isotherm_point in isotherms_dict[mof]['isotherm_data']]) # get unique values

                    if pressures == {0.05, 0.5, 2.5, 0.9, 4.5}: # most common CH4 isotherm
                        if mof in store_adsorptions_ch4_main:
                            continue
                        store_temp_adsorption_values_ch4_main = []
                        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                            store_temp_adsorption_values_ch4_main.extend([isotherm_point['total_adsorption']])
                        store_adsorptions_ch4_main[mof].append(sorted(store_temp_adsorption_values_ch4_main)) # sort in order, to match pressure
                    elif pressures == {65.0, 100.0}:
                        if mof in store_adsorptions_ch4_second:
                            continue
                        store_temp_adsorption_values_ch4_second = []
                        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                            store_temp_adsorption_values_ch4_second.extend([isotherm_point['total_adsorption']])
                        store_adsorptions_ch4_second[mof].append(sorted(store_temp_adsorption_values_ch4_second))

                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'N2':
                    pressures = set([isotherm_point['pressure'] for isotherm_point in isotherms_dict[mof]['isotherm_data']])

                    if pressures == {0.09, 0.9}: # most common pressures
                        if mof in store_adsorptions_n2_main:
                            continue
                        store_temp_adsorption_values_n2_main = []
                        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                            store_temp_adsorption_values_n2_main.extend([isotherm_point['total_adsorption']])
                        store_adsorptions_n2_main[mof].append(sorted(store_temp_adsorption_values_n2_main))
                    elif pressures == {100000.0, 1.0, 23714.0, 4.0, 75.0, 18.0, 1334.0, 5623.0, 316.0}:
                        if mof in store_adsorptions_n2_second:
                            continue
                        store_temp_adsorption_values_n2_second = []
                        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                            store_temp_adsorption_values_n2_second.extend([isotherm_point['total_adsorption']])
                        store_adsorptions_n2_second[mof].append(sorted(store_temp_adsorption_values_n2_second))

                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'H2':
                    pressures = set([isotherm_point['pressure'] for isotherm_point in isotherms_dict[mof]['isotherm_data']])

                    if pressures == {2.0, 100.0}:
                        if mof in store_adsorptions_h2:
                            continue
                        store_temp_adsorption_values_h2 = []
                        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                            store_temp_adsorption_values_h2.extend([isotherm_point['total_adsorption']])
                        store_adsorptions_h2[mof].append(sorted(store_temp_adsorption_values_h2))

                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'CO2':
                    pressures = set([isotherm_point['pressure'] for isotherm_point in isotherms_dict[mof]['isotherm_data']])

                    if pressures == {0.1, 0.5, 2.5, 0.05, 0.01}:
                        if mof in store_adsorptions_co2:
                            continue
                        store_temp_adsorption_values_co2 = []
                        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                            store_temp_adsorption_values_co2.extend([isotherm_point['total_adsorption']])
                        store_adsorptions_co2[mof].append(sorted(store_temp_adsorption_values_co2))

ch4_main = sorted([0.05, 0.5, 2.5, 0.9, 4.5])
ch4_second = sorted([65.0, 100.0])
n2_main = sorted([0.09, 0.9])
n2_second = sorted([100000.0, 1.0, 23714.0, 4.0, 75.0, 18.0, 1334.0, 5623.0, 316.0])
h2 = sorted([2.0, 100.0])
co2 = sorted([0.1, 0.5, 2.5, 0.05, 0.01])

all_pressures = {'ch4_main': ch4_main, 'ch4_second': ch4_second, 'n2_main': n2_main, 'n2_second': n2_second, 'h2': h2, 'co2': co2}

# write out adsorptions to csv files
def pressures_adsorption(path: str, adsorption_dict: dict, pressures: List,  output_file_name: str):

    with open(f"{path}/{output_file_name}.csv", "w") as outcsv:
        pressures.insert(0, 'structure')
        pres =  map(str, pressures) # get rid of quotes around 'structure'
        pres = ",".join(pres).replace('[', '').replace(']', '')
        outcsv.write(pres + "\n")
        for key in adsorption_dict.keys():
            ads = adsorption_dict[key]
            ads.insert(0, key)
            ads = map(str, ads)
            ads = ",".join(ads).replace('[', '').replace(']', '')
            outcsv.write(ads + "\n")

if __name__ == '__main__':
    for key, value in all_pressures.items():
        # don't normally want to use eval but it's so convenient here...
        pressures_adsorption(path, eval('store_adsorptions_' + key), value, key)
