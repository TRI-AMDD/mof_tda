"""
Take the 5738 persistence diagrams already computed on AWS and create a data frame that
queries the isotherms database and grabs the pressure/adsorptions
Save this to a csv file, and grab items from it via dataframe

"""
import json
import pandas as pd
import os
from mof_tda import MOF_TDA_PATH

store_mofs = []
#with open(os.path.join(MOF_TDA_PATH, "create_data_frame/randomized_mof_500.txt"), "r") as mof_struct:
with open(os.path.join(MOF_TDA_PATH, "create_data_frame/pressure_1_4_75_randomized_mofs_500_v2.txt"), "r") as mof_struct:
    for line in mof_struct:
        line = line.strip()
        store_mofs.append(line)

# Load json database
with open("mofdb_isotherms.json") as f:
    isotherms_data = json.loads(f.read())

# Make a dict of the mof structure + it's information
isotherms_dict = {doc['adsorbent']['name']: doc for doc in isotherms_data}

# Store the list of pressures
pressures = [isotherm_point['pressure'] for isotherm_point in isotherms_dict[store_mofs[0]]['isotherm_data']]

# Test it out to make sure I'm getting the adsorption out
adsorption = [isotherm_point['total_adsorption'] for isotherm_point in \
                isotherms_dict[store_mofs[0]]['isotherm_data']]

# initialize dict so it can take values when the key isn't already in there
from collections import defaultdict
store_data = defaultdict(list)

for mof in store_mofs:
    store_temp_adsorption_values = []
    if isotherms_dict.get(mof) is not None:
        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
            store_temp_adsorption_values.extend([isotherm_point['total_adsorption']])
    store_data[mof].append(store_temp_adsorption_values)

from collections import defaultdict
store_data_pressures = defaultdict(list)
for mof in store_mofs:
    store_temp_pressure_values = []
    if isotherms_dict.get(mof) is not None:
        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
            store_temp_pressure_values.extend([isotherm_point['pressure']])
    store_data_pressures[mof].append(store_temp_pressure_values)

new_dict = {}

for key, value in store_data_pressures.items():
    for j in value:
        new_dict[key] = frozenset(j)

from collections import Counter
store_outputs = Counter(new_dict.values())

# For the case of just the randomized 500 mofs
"""
for key, value in new_dict.items():
    if value == {100000, 1, 23714, 4, 75, 18, 1334, 5623, 316}:
        with open("pressure_1_4_75_from_randomized_mofs_500.txt","a+") as output:
            output.write("%s\n" % key)
"""
"""
# For the case of 5000+ MOFs
for key, value in new_dict.items():
    if value == {100000, 1, 23714, 4, 75, 18, 1334, 5623, 316}:
        with open("pressure_1_4_75_from_all_mofs.txt", "a+") as output:
            output.write("%s\n" % key)
"""

# write out the hash table to a table, with the pressure header
# Note: need some small changes in excel, like including a 'Structure' column
import csv

with open('randomized_mof_500_data_v2.csv', 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow([pressures])
    for key in store_data.keys():
        writer.writerow([key] + store_data[key])
