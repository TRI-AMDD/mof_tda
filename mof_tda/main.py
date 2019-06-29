import os
import pickle
from typing import Any, List
from tqdm import tqdm

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes
from mof_tda.convert_structure import convert_cif_to_xyz
from mof_tda.create_cubic_cells import copies_to_fill_cell, lattice_param

from mof_tda.get_delaunay_triangulation import get_delaunay_simplices, get_persistence, take_square_root
from multiprocessing import Pool


def get_xyz_structures(num_structures : int) -> List[str]:
    """
    Gets the (num_structures) lowest volume structures and converts them to xyz files

    Arg:
        number of structures to grab from the lowest volume ones

    Return:
        List containing names of xyz files
    """
    # TODO: similarly here, replace the intermediate text files with glob commands for getting
    #       filenames
    filepath = []
    PATH_NAME = 'allMOFs_without_disorder.txt'
    with open(os.path.join(MOF_TDA_PATH, PATH_NAME),'r') as f:
        for line in f:
            line = line.strip()
            filepath.append(line)

    # Pre-processing to get volume distribution of MOFs
    total_volume = pickle.load(open(os.path.join(MOF_TDA_PATH,'tot_volume.pkl'), 'rb'))
    lowest_mof_list, volumes = get_lowest_volumes(num_structures, total_volume, filepath)

    # MOF files to be used are printed out to "mof_structures.txt": convert to xyz
    convert_cif_to_xyz(os.path.join(MOF_TDA_PATH, 'mof_structures.txt'))

    calculation_filepath = []
    mof_files = os.path.join(MOF_TDA_PATH, 'mof_structures.txt')
    with open(mof_files,'r') as f:
        for line in f:
            line = line.strip()
            stripped_line = line[:-4]  # strip .cif off
            calculation_filepath.append(stripped_line + ".xyz")
    return calculation_filepath


# TODO: rename this file and function to something descriptive of what it's doing.
#       "main" as a function title is very rarely necessary in python
def main(xyz_file) -> Any:
    """
    Execute main code for function by reading an xyz file and returning persistence diagram

    Arg: xyz_file is the name of an xyz structure (which is stored in 'xyz_structures')

    Return: persistence diagram from Delaunay triangulation, current file name
    """
    # Point to xyz_structures directory
    os.chdir(os.path.join(MOF_TDA_PATH, 'xyz_structures/'))
    cubic_cell_dimension = 100
    current_file = xyz_file
    try:
        lattice_csts = lattice_param(xyz_file)
        new_cell = copies_to_fill_cell(cubic_cell_dimension, xyz_file, lattice_csts)
        simplices = get_delaunay_simplices(new_cell)
        simplices = take_square_root(simplices)
        dgms = get_persistence(simplices)
        current_file = current_file[:-4]
        print(current_file)
        pickle.dump(dgms, open(os.path.join(MOF_TDA_PATH, 'oned_persistence/' + current_file), "wb"))
        with open(os.path.join(MOF_TDA_PATH, "able_to_compute.txt"), "a+") as able:
            able.write("%s\n" % current_file)

        # Return none so output isn't stored in memory
        del dgms
        return None
    except Exception as exception:
        with open(os.path.join(MOF_TDA_PATH, "unable_to_compute.txt"), "a+") as unable:
            unable.write("{}: {}\n".format(current_file, exception))
        pass


if __name__ == '__main__':
    # TODO: store these commands in a separate function, then call a single function in this block
    # Remove compute/unable to compute files
    if os.path.exists(os.path.join(MOF_TDA_PATH, "able_to_compute.txt")):
        os.remove(os.path.join(MOF_TDA_PATH, "able_to_compute.txt"))
    if os.path.exists(os.path.join(MOF_TDA_PATH, "unable_to_compute.txt")):
        os.remove(os.path.join(MOF_TDA_PATH, "unable_to_compute.txt"))
    num_structures = 4
    calculation_filepath = get_xyz_structures(num_structures)
    with Pool(processes = 4) as pool:
        persistence = list(tqdm(pool.imap(main, calculation_filepath), total=num_structures))

    # TODO: remove these if unused, or store in a separate function for testing
    """
    #not parallelized
    for i in range(num_structures):
        main(calculation_filepath[i])
    """
