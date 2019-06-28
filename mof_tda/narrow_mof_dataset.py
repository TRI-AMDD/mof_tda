from typing import List, Tuple
import numpy as np
import pickle
from mof_tda import MOF_TDA_PATH
import os


# TODO: duplicated code, reuse other module vars and delete
MOF_FILES = 'allMOFs_without_disorder.txt'
filepath = []
with open(os.path.join(MOF_TDA_PATH, MOF_FILES), 'r') as f:
    for line in f:
        line = line.strip()
        filepath.append(line)


# TODO: reformat docstring properly
def get_lowest_volumes(n: int, total_volume: List[float], mof_list) -> Tuple[List[str], List[float]]:
    """
    Return the lowest volume structures, that can then be used for persistence diagrams

    Arg: number of lowest volume structures, total volume list of all MOFs, list of names of MOF structure_list

    Return: list of structure names of lowest volume structures, volumes of lowest volume structures
    """
    sorted_volume_index = np.argsort(total_volume)
    lowest_n = sorted_volume_index[:n]
    new_mof_list = [mof_list[i] for i in lowest_n]

    sorted_volume = np.sort(total_volume)
    sorted_lowest_n = sorted_volume[:n]

    with open(os.path.join(MOF_TDA_PATH, 'mof_structures.txt'), 'w') as f:
        for item in new_mof_list:
            f.write("%s\n" % item)
    return new_mof_list, sorted_lowest_n


if __name__ == '__main__':
    total_volume = pickle.load(open('tot_volume.pkl', 'rb'))
    new_mof_list = get_lowest_volumes(40, total_volume, filepath)
