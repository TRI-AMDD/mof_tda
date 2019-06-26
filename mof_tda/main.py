import os
import numpy as np
import pickle
from typing import List, Tuple, Any

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes
from mof_tda.cif2xyz_ase import cif2xyz
from mof_tda.create_cubic_cells import copies_to_fill_cell, lattice_param
from mof_tda.get_delaunay_triangulation import get_delaunay_simplices, get_persistence, take_square_root
from pymatgen import Structure, Lattice
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io.xyz import write_xyz
from multiprocessing import Pool

def get_xyz_structures(num_structures : int) -> List[str]:
    """
    Gets the (num_structures) lowest volume structures and converts them to xyz files

    Arg:
        number of structures to grab from the lowest volume ones

    Return:
        List containing names of xyz files
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

    cif2xyz(os.path.join(MOF_TDA_PATH, 'mof_structures.txt'))

    calculation_filepath = []
    MOF_FILES = os.path.join(MOF_TDA_PATH, 'mof_structures.txt')
    with open(MOF_FILES,'r') as f:
        for line in f:
            line = line.strip()
            stripped_line = line[:-4] #strip .cif off
            calculation_filepath.append(stripped_line + ".xyz")
    return calculation_filepath

def main(xyz_file) -> Any:
    """
    Execute main code for function by reading an xyz file and returning persistence diagram

    Arg: xyz_file is the name of an xyz structure (which is stored in 'xyz_structures')

    Return: persistence diagram from Delaunay triangulation, current file name
    """
    #Point to xyz_structures directory
    os.chdir(os.path.join(MOF_TDA_PATH, 'xyz_structures/'))
    cubic_cell_dimension = 100
    current_file = xyz_file
    lattice_csts = lattice_param(xyz_file)
    new_cell = copies_to_fill_cell(cubic_cell_dimension, xyz_file, lattice_csts)
    simplices = get_delaunay_simplices(new_cell)
    simplices = take_square_root(simplices)
    try:
        dgms = get_persistence(simplices)
        current_file = current_file[:-4]
        print(current_file)
        with open(os.path.join(MOF_TDA_PATH, "able_to_compute.txt"), "a+") as able:
            able.write("%s\n" % (current_file))
        pickle.dump(dgms, open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' + current_file), "wb"))
        return dgms
    except:
        with open(os.path.join(MOF_TDA_PATH, "unable_to_compute.txt"), "a+") as unable:
            unable.write("%s\n" % (current_file))
        pass

if __name__ == '__main__':
    #rm compute/unable to compute files
    if os.path.exists(os.path.join(MOF_TDA_PATH, "able_to_compute.txt")) == True:
        os.remove(os.path.join(MOF_TDA_PATH, "able_to_compute.txt"))
    if os.path.exists(os.path.join(MOF_TDA_PATH, "unable_to_compute.txt")) == True:
        os.remove(os.path.join(MOF_TDA_PATH, "unable_to_compute.txt"))
    num_structures = 8
    calculation_filepath = get_xyz_structures(num_structures)
    from tqdm import tqdm
    with Pool(processes = 4) as pool:
        persistence = list(tqdm(pool.imap(main, calculation_filepath), total = num_structures))
    """
    #not parallelized
    for i in range(num_structures):
        main(calculation_filepath[i])
    """
    """
    from functools import partial
    from tqdm import tqdm
    num_structures = 8
    persistence = partial(main, num_structures = 8)
    with Pool(processes =4) as pool:
    #    import nose; nose.tools.set_trace()
        results = list(tqdm(pool.imap(persistence, np.arange(0, num_structures)), total = num_structures))
    #    results = pool.map(persistence, np.arange(0, num_structures))
    """
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
