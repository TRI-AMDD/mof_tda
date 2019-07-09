"""
Calculate wasserstein distance (a similarity metric) between persistence diagrams
"""
import os
from typing import Any, List, Dict, Tuple
import dionysus as d
import pickle
import numpy as np
from tqdm import tqdm
from mof_tda import MOF_TDA_PATH
from multiprocessing import Pool

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

    Wasserstein distance returns a NN approximation solution (w.r.t. delta value)
    """
    wasserstein_distance = d.wasserstein_distance(pers_diag_1[1], pers_diag_2[1], \
                                                    q=1, delta=0.2)
    return wasserstein_distance

def multiprocessing_func(combo: Tuple[str, str]) -> float:
    """
    Multiprocess calculation of wasserstein distance between persistence diagrams
    (i.e. calculate multiple at once)

    Arg:
        Tuple[string, string] consisting of name of each structure
    Return:
        Wasserstein distance between each tuple
    """
    pers_diag_1 = pickle.load(open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' \
                            + combo[0]), 'rb'))
    pers_diag_2 = pickle.load(open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' \
                            + combo[1]), 'rb'))
    wasserstein_distance = wasserstein_distance_1d(pers_diag_1, pers_diag_2)
    return wasserstein_distance

def calculate_wasserstein(structure_list : List[str]) -> Dict:
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
    # fill list with all the combinations from structure_list
    combos = list(combinations(structure_list, 2))

    #parallelize to calculate wasserstein distance
    from multiprocessing import Pool
    with Pool(processes=4) as pool:
        wds_1d = list(tqdm(pool.imap(multiprocessing_func, combos), total=len(combos)))

    # Hash structure_list tuple combos as key, value: wasserstein_distance
    wd_dict = {combo: wd_1d for combo, wd_1d in zip(combos, wds_1d)}
    return wd_dict

def write_to_csv(struct_tuple_distance : Dict) -> None:
    """
    Take in dict of {(struct1_string, struct2_string) : float} and store to csv file

    Arg:
        Dict{Tuple[string, string] : float}

    Return:
        None, just store to a csv file
    """
    import csv
    with open('wasserstein_distances_1d.csv', 'w') as wd_file:
        writer = csv.writer(wd_file)
        for key, value in struct_tuple_distance.items():
            writer.writerow([key, value])
    return None

def construct_matrix(wd_1d : Dict, structure_list) -> np.array:
    """
    Take in hash table of {tuple(string, string) : float},
    match up each tuple entry to a number (via another hash table)
    and construct a distance matrix from this

    Arg:
        wd_1d :: Dict{Tuple[string, string] : float}
        structure_list :: List[string]

    Return:
        distance_matrix :: np.array
    """
    # Give each structure an index, based on order in the original file
    index_to_structure = {} # Dict{string : float}
    for i, structure in enumerate(structure_list):
        index_to_structure[structure] = i

    total = len(structure_list)
    distance_matrix = np.zeros((total, total))
    # Replace structure names with their index
    index_to_value = {(index_to_structure[key1], index_to_structure[key2]): value \
                    for (key1, key2), value in wd_1d.items()}
    for (struct1, struct2), distance in index_to_value.items():
        distance_matrix[struct1, struct2] = distance

    for i in range(total):
        for j in range(i, total):
            # if loop so that it's agnostic to original order
            if distance_matrix[i][j] != 0:
                distance_matrix[j][i] = distance_matrix[i][j]
            else:
                distance_matrix[i][j] = distance_matrix[j][i]

    return distance_matrix

def run_code(filename: str):
    """
    Arg: Give filename of file that holds names of all the structures

    Return: distance matrix
    """
    structure_list = store_structures(filename)
    wd_dict = calculate_wasserstein(structure_list)
    # can also write to csv here
    # TO DO: separate mapping function, i.e. row/column index to compound, such as in csv
    distance_matrix = construct_matrix(wd_dict, structure_list)
    return distance_matrix
if __name__ == '__main__':
    distance_matrix = run_code('lowest_8.txt')
    print(distance_matrix)
