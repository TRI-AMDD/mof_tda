"""
Calculate wasserstein distance (a similarity metric) between persistence diagrams
"""
import os
from typing import Any, List
import dionysus as d
import pickle
from mof_tda import MOF_TDA_PATH

def store_structures(filename : str) -> List[str]:
    """
    Store the structures from a file to a list, to be used to calculate wasserstein distances

    Arg:
        Filename :: string containing MOF structure names

    Return:
        List of structure names
    """
    structure_list = []
    with open(os.path.join(MOF_TDA_PATH, 'metrics/' + filename), 'r') as structures:
        for line in structures:
            line = line.strip()
            structure_list.append(line)
    return structure_list

def wasserstein_distance_1d(pers_diag_1, pers_diag_2) -> float:
    """
    Takes in 1d persistence diagrams and returns a wasserstein distance
    Args:
        pers_diag_1, pers_diag_2 :: persistence diagrams
    Return:
        Wasserstein distance :: float
    """
    wasserstein_distance = d.wasserstein_distance(pers_diag_1[1], pers_diag_2[2], \
                                                    q=1, delta=0.2)
    return wasserstein_distance

def calculate_wasserstein(structure_list : List[str]) -> List[float]:
    """
    Calculate wasserstein distances for all combinations of structure in text file

    Arg:
        structure_list :: list of strings containing structure paths

    Return:
        list of wasserstein distances
    """
    from itertools import combinations

    # from collections import defaultdict
    # wd_1d = defaultdict(list)
    wd_1d = {}
    for combo in combinations(os.listdir(os.path.join(MOF_TDA_PATH, \
                                    'oned_persistence/')), 2):
        # Check if the structures are in the original structure list
        if all(x in structure_list for x in (combo[0], combo[1])):
            pers_diag_1 = pickle.load(open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' \
                                    + combo[0]), 'rb'))
            pers_diag_2 = pickle.load(open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' \
                                    + combo[1]), 'rb'))
            wasserstein_distance = wasserstein_distance_1d(pers_diag_1, pers_diag_2)

            # Hash structure_list tuple combos as key, value: wasserstein_distance
            wd_1d[combo] = wasserstein_distance
    return wd_1d

if __name__ == '__main__':
    structure_list = store_structures('lowest_8.txt')
    print(structure_list)

    wd_1d = calculate_wasserstein(structure_list)
    print(wd_1d)

    # Write out to a csv file
    import csv
    with open('wasserstein_distances_1d.csv', 'w') as wd_file:
        writer = csv.writer(wd_file)
        for key, value in wd_1d.items():
            writer.writerow([key, value])
