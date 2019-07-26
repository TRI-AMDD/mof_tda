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
with open(os.path.join(MOF_TDA_PATH, "create_data_frame/randomized_mof_500.txt"), "r") as mof_struct:
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
print(adsorption)

# initialize dict so it can take values when the key isn't already in there
from collections import defaultdict
store_data = defaultdict(list)

for mof in store_mofs:
    store_temp_adsorption_values = []
    if isotherms_dict.get(mof) is not None:
        for isotherm_point in isotherms_dict[mof]['isotherm_data']:
            store_temp_adsorption_values.extend([isotherm_point['total_adsorption']])
    store_data[mof].append(store_temp_adsorption_values)

# write out the hash table to a table, with the pressure header
# Note: need some small changes in excel, like including a 'Structure' column
import csv
print(pressures)
with open('randomized_mof_500_data.csv', 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow([pressures])
    for key in store_data.keys():
        writer.writerow([key] + store_data[key])
