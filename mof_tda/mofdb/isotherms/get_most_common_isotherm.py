"""
Go thru all the json files and keep a counter of the most common isotherm for N2/CH4/H2/CO2
"""
import json
import os

path = "mof_tda/mofdb/isotherms"

nums_json = []

from collections import defaultdict
store_data_pressures_ch4 = defaultdict(list)
store_data_pressures_n2 = defaultdict(list)
store_data_pressures_h2 = defaultdict(list)
store_data_pressures_co2 = defaultdict(list)

for fname in os.listdir(path):
    if fname.startswith("page_"):
        split_fname = fname.split('_')[1] # get the number.sjon, e.g. 1.json
        get_num = split_fname.split('.')[0] #store the page number

        with open(path + "/" + fname) as f:
            isotherms_data = json.loads(f.read())

            # create a dict based on the mof name
            isotherms_dict = {doc['adsorbent']['name']: doc for doc in isotherms_data}

            for index, mof in enumerate(isotherms_dict): # item is each mof
                if len(isotherms_dict[mof]['adsorbates']) > 1: # skip xe/kr
                    continue
                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'CH4':
                    store_temp_pressure_values_ch4 = [] #initialize list of pressures for each mof
                    for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                        store_temp_pressure_values_ch4.extend([isotherm_point['pressure']])
                    store_data_pressures_ch4[mof].append(store_temp_pressure_values_ch4)

                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'N2':
                    store_temp_pressure_values_n2 = [] #initialize list of pressures for each mof
                    for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                        store_temp_pressure_values_n2.extend([isotherm_point['pressure']])
                    store_data_pressures_n2[mof].append(store_temp_pressure_values_n2)

                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'H2':

                    store_temp_pressure_values_h2 = [] #initialize list of pressures for each mof
                    for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                        store_temp_pressure_values_h2.extend([isotherm_point['pressure']])

                    store_data_pressures_h2[mof].append(store_temp_pressure_values_h2)

                elif isotherms_dict[mof]['adsorbates'][0]['formula'] == 'CO2':

                    store_temp_pressure_values_co2 = [] #initialize list of pressures for each mof
                    for isotherm_point in isotherms_dict[mof]['isotherm_data']:
                        store_temp_pressure_values_co2.extend([isotherm_point['pressure']])

                    store_data_pressures_co2[mof].append(store_temp_pressure_values_co2)

# Collect the most common isotherm for each gas here
pressures_isotherms_ch4 = {}
pressures_isotherms_n2 = {}
pressures_isotherms_h2 = {}
pressures_isotherms_co2 = {}

for key, value in store_data_pressures_ch4.items():
    for j in value:
        pressures_isotherms_ch4[key] = frozenset(j)

for key, value in store_data_pressures_n2.items():
    for j in value:
        pressures_isotherms_n2[key] = frozenset(j)

for key, value in store_data_pressures_h2.items():
    for j in value:
        pressures_isotherms_h2[key] = frozenset(j)

for key, value in store_data_pressures_co2.items():
    for j in value:
        pressures_isotherms_co2[key] = frozenset(j)

from collections import Counter
common_isotherms_ch4 = Counter(pressures_isotherms_ch4.values())

common_isotherms_n2 = Counter(pressures_isotherms_n2.values())

common_isotherms_h2 = Counter(pressures_isotherms_h2.values())

common_isotherms_co2 = Counter(pressures_isotherms_co2.values())

# save the most common isotherm output to a file
with open(path + '/most_common_isotherms.txt', 'w') as f:
    f.write('CH4 ' + str(common_isotherms_ch4))
    f.write("\n")
    f.write('N2 ' + str(common_isotherms_n2))
    f.write("\n")
    f.write('H2 ' + str(common_isotherms_h2))
    f.write("\n")
    f.write('CO2 ' + str(common_isotherms_co2))
