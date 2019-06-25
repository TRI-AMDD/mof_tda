import os
import numpy as np
import pickle
from typing import List, Tuple, Any

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes
from mof_tda.cif2xyz_ase import cif2xyz
from mof_tda.create_cubic_cells import copies_to_fill_cell, lattice_param
from mof_tda.get_delaunay_triangulation import get_delaunay_simplices, get_persistence
from pymatgen import Structure, Lattice
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io.xyz import write_xyz
from multiprocessing import Pool

def main(i : int, num_structures : int) -> Any:
    """
    Execute main code for function

    Arg: i is the index of the structure in the txt file, num_structures is the number of structures to use

    Return: persistence diagram from Delaunay triangulation, current file name
    """
    filepath = []
    PATH_NAME = 'allMOFs_without_disorder.txt'
    with open(os.path.join(MOF_TDA_PATH, PATH_NAME),'r') as f:
        for line in f:
            line = line.strip()
            filepath.append(line)

    #Pre-processing to get volume distribution of MOFs
    total_volume = pickle.load(open(os.path.join(MOF_TDA_PATH,'tot_volume.pkl'), 'rb'))
    lowest_mof_list, volumes = get_lowest_volumes(num_structures, total_volume, filepath)

    #Use the largest volume to decide number of periodic copies
    #cubic_cell_dimension = np.ceil(((volumes[-1])**(1/3))*4)
    cubic_cell_dimension = 100

    #MOF files to be used are printed out to "mof_structures.txt": convert to xyz
    cif2xyz(os.path.join(MOF_TDA_PATH, 'mof_structures.txt'))

    calculation_filepath = []
    MOF_FILES = os.path.join(MOF_TDA_PATH, 'mof_structures.txt')
    with open(MOF_FILES,'r') as f:
        for line in f:
            line = line.strip()
            stripped_line = line[:-4] #strip .cif off
            calculation_filepath.append(stripped_line + ".xyz")

    #Point to xyz_structures directory
    os.chdir(os.path.join(MOF_TDA_PATH, 'xyz_structures/'))
    current_file = calculation_filepath[i]
    lattice_csts = lattice_param(calculation_filepath[i])
    new_cell = copies_to_fill_cell(cubic_cell_dimension, calculation_filepath[i], lattice_csts)
    simplices = get_delaunay_simplices(new_cell)
    dgms = get_persistence(simplices)
    current_file = current_file[:-4]
    pickle.dump(dgms, open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' + current_file), "wb"))
    return dgms, current_file

if __name__ == '__main__':
    from functools import partial
    from tqdm import tqdm
    num_structures = 8
    persistence = partial(main, num_structures = 8)
    with Pool(processes =4) as pool:
    #    import nose; nose.tools.set_trace()
        results = list(tqdm(pool.imap(persistence, np.arange(0, num_structures)), total = num_structures))
    #    results = pool.map(persistence, np.arange(0, num_structures))
    """
    for dgms, filename in results:
        filename = filename[:-4]
        #pickle the persistence diagram
        pickle.dump(dgms, open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' + filename), "wb"))
    """
    """
    num_structures = 4 #Number of structures to run calculation on
    for i in range(num_structures):
        print(i)
        persistence_diagram, current_file = main(i, num_structures)
        current_file = current_file[:-4]#strip the .xyz part
        #pickle the persistence diagram
        pickle.dump(persistence_diagram, open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' + current_file), "wb"))
    """
