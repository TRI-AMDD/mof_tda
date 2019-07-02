from typing import List, Tuple
import numpy as np
import pickle
from mof_tda import MOF_TDA_PATH
import os

MOF_FILES = 'allMOFs_without_disorder.txt'
FILEPATH = []
with open(os.path.join(MOF_TDA_PATH, MOF_FILES), 'r') as f:
    for line in f:
        line = line.strip()
        FILEPATH.append(line)

def get_lowest_volumes(num_structures : int, total_volume : List[float], mof_list) \
    -> Tuple[List[str], List[float]]:
    """
    Return the lowest volume structures, that can then be used for persistence diagrams

    Arg: number of lowest volume structures, total volume list of all MOFs,
    list of names of MOF structure_list

    Return: list of structure names of lowest volume structures, volumes of lowest volume structures
    """
    sorted_volume_index = np.argsort(total_volume)
    lowest_n = sorted_volume_index[:num_structures]
    new_mof_list = [mof_list[i] for i in lowest_n]

    sorted_volume = np.sort(total_volume)
    sorted_lowest_n = sorted_volume[:num_structures]

    with open(os.path.join(MOF_TDA_PATH, 'mof_structures.txt'), 'w') as mof_struct:
        for item in new_mof_list:
            mof_struct.write("%s\n" % item)
    return new_mof_list, sorted_lowest_n

if __name__ == '__main__':
    TOTAL_VOLUME = pickle.load(open('tot_volume.pkl', 'rb'))
    NEW_MOF_LIST = get_lowest_volumes(40, TOTAL_VOLUME, FILEPATH)
