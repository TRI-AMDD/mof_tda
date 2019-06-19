from typing import List, Tuple
import numpy as np
import pickle

MOF_FILES = 'allMOFs_without_disorder.txt'
filepath = []
with open(MOF_FILES,'r') as f:
    for line in f:
        line = line.strip()
        filepath.append(line)

def get_lowest_volumes(n : int, total_volume : List[float], mof_list) -> List[float]:
    sorted_volume_index = np.argsort(total_volume)
    lowest_n = sorted_volume_index[:n]
    new_mof_list = [mof_list[i] for i in lowest_n]

    with open('mof_structures.txt', 'w') as f:
        for item in new_mof_list:
            f.write("%s\n" % item)
    return new_mof_list

if __name__ == '__main__':
    total_volume = pickle.load(open('tot_volume.pkl', 'rb'))
    new_mof_list = get_lowest_volumes(40, total_volume, filepath)
