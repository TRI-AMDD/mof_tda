"""
Calculate persistence images from the persistence diagrams
"""
import pickle
from typing import (Any, Set, List, Tuple, Dict, Optional, TextIO)
import os
import numpy as np
import matplotlib.pyplot as plt
import dionysus as d
import pandas as pd
from tqdm import tqdm
from mof_tda import MOF_TDA_PATH
from multiprocessing import Pool

from persim import PersImage

def create_structure_list_without_cif(filepath: str) -> List[str]:
    """
    Create the structure list with just the structure name, since the persistence
    diagrams don't have the extension

    Arg: Take in file with names of all the structures

    Return: List with all the structure names
    """
    structure_list = []
    with open(os.path.join(MOF_TDA_PATH, "persistence_images/" + filepath), "r") as filepath:
        for line in filepath:
            line = line.strip()
            line = line[:-4] #remove .cif
            structure_list.append(line)
    return structure_list

def create_structure_list(filepath: str) -> List[str]:
    """
    Arg: Take in file with names of all the structures

    Return: List with all the structure names
    """
    structure_list = []
    with open(os.path.join(MOF_TDA_PATH, "persistence_images/" + filepath), "r") as filepath:
        for line in filepath:
            line = line.strip()
            structure_list.append(line)
    return structure_list

def unpickle_persistence_diagram(pickled_file):
    """
    Unpickle the persistence diagram
    """
    persistence_diagram = pickle.load(open(os.path.join(MOF_TDA_PATH, "oned_persistence/" + pickled_file), 'rb'))
    return persistence_diagram

def convert_persistence_diagrams_1d(persistence_diagram: List[Tuple]) -> List[float]:
    """
    Convert the persistence diagrams in Dionysus to the format that PersImage takes

    Arg: Persistence diagram in Dionysus format

    Return: The oned array corresponding to the persistence diagram
    """
    birth_zerod = []
    death_zerod = []
    birth_oned = []
    death_oned = []
    birth_twod = []
    death_twod = []
    for i, dgm in enumerate(persistence_diagram):
        if i == 0:
            for pt in dgm:
                birth_zerod.append(pt.birth)
                death_zerod.append(pt.death)
        zerod_array = np.column_stack((birth_zerod, death_zerod))
        if i == 1:
            for pt in dgm:
                birth_oned.append(pt.birth)
                death_oned.append(pt.death)
        oned_array = np.column_stack((birth_oned, death_oned))
        if i==2:
            for pt in dgm:
                birth_twod.append(pt.birth)
                death_twod.append(pt.death)
        twod_array = np.column_stack((birth_twod, death_twod))

    #Combine two arrays
    converted_zerod_oned = np.array([[zerod_array], [oned_array]])

    #Combine all three arrays
    total_converted = np.array([[zerod_array],[oned_array], [twod_array]])

    # Right now just return the oned array, but it's modifiable
    return(oned_array)

def file_len(filename):
    """
    Function to get the length of a file
    """
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def get_max_death(structure_list: List[str]) -> float:
    """
    Take in list of structures, and get oned_persistence arrays of each one
    Get max death value from the list, this can be used for scaling

    Arg: Take in full list of structures

    Return: max death value
    """
    store_tuples = []
    for structure in structure_list:
        struct = unpickle_persistence_diagram(structure)
        oned_array = convert_persistence_diagrams_1d(struct)
        store_tuples.append(oned_array)

    # Combine into one array
    store_tuples = np.vstack(store_tuples)
    max_death = sorted(store_tuples, key=lambda x: x[1], reverse=True)[0]
    max_death = max_death[1]
    return max_death

def convert_to_image(pers_diag_array, max_death: float, structure_name: str):
    """
    Take in the array corresponding to a persistence diagram, and convert to an image

    Arg: Persistence diagram array, max_death value, name of structure
    """
    pixels = [50,50]
    spread = 0.2
    pim = PersImage(specs={"minBD": 0, "maxBD": max_death}, spread=spread, pixels=pixels, verbose=False)

    img = pim.transform(pers_diag_array)

    pickle.dump(img, open(os.path.join(MOF_TDA_PATH, 'persistence_images/store_images/' + structure_name + ".pers_image"), 'wb'))
    return None

def convert_to_image_multiprocessing(pers_diag_array):
    """
    Take in an array, convert to an image
    Adjust all the parameters here: run the max death function first to get the value

    Arg : 2d array

    Return: Matrix of dimensions specified in pixels
    """
    pixels = [50,50]
    spread = 0.15
    max_death = 3.9096455574035645
    pim = PersImage(specs={"minBD": 0, "maxBD": max_death}, spread=spread, pixels=pixels, verbose=False)
    img = pim.transform(pers_diag_array)
    return img

def diagram_to_image(structure_name):
    """
    The function that is fed to imap to go from persistence_diagram to image

    To avoid partial/lambda, this function only takes in one argument (name of structure)
    """

    persistence_diagram = unpickle_persistence_diagram(structure_name)
    oned_persistence_array = convert_persistence_diagrams_1d(persistence_diagram)
    img = convert_to_image_multiprocessing(oned_persistence_array)
    # Store the persistence image output, this folder name can be changed depending on parameters
    pickle.dump(img, open(os.path.join(MOF_TDA_PATH, 'persistence_images/store_images/' + structure_name + ".pers_image"), 'wb'))

    return None

def run_code_multiprocessing(structure_list):
    """
    Arg: Take in a list of arrays corresponding to the persistence diagrams

    Return: Nothing, the persistence images should be pickled
    """

    with Pool(processes=2) as pool:
        pers_images = list(tqdm(pool.imap(diagram_to_image, structure_list), \
                                total=len(structure_list)))

    return None

if __name__ == '__main__':
    structure_list = create_structure_list("lowest_8.txt")
    # Run max_death first to get the value to put in, then comment it out
    # max_death = get_max_death(structure_list)
    # print(max_death)
    run_code_multiprocessing(structure_list)
