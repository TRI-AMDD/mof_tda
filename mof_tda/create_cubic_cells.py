""" This module creates periodic copies of a structure to fit a cubic box """

import os
from typing import List
from matplotlib import pyplot as plt
import random
import numpy as np
from mof_tda import MOF_TDA_PATH

MOF_FILES = os.path.join(MOF_TDA_PATH, 'subset_mof_list.txt')
FILEPATH = []
with open(MOF_FILES, 'r') as f:
    for line in f:
        line = line.strip()
        stripped_line = line[:-4] #strip .cif off
        FILEPATH.append(stripped_line + ".xyz")

from mof_tda import MOF_TDA_PATH
import numpy as np

MOF_FILES = os.path.join(MOF_TDA_PATH, 'subset_mof_list.txt')
DEFAULT_FILEPATHS = []
with open(MOF_FILES,'r') as f:
    for line in f:
        line = line.strip()
        stripped_line = line[:-4]  # strip .cif off
        DEFAULT_FILEPATHS.append(stripped_line + ".xyz")

# TODO: replace this with pymatgen
def lattice_param(filepath: str) -> List[np.ndarray]:
    """
    Return lattice constants for each crystal structure
    Note: this can be replaced with pymatgen

    Args:
        filepath (str): name of file

    Returns:
        List of lattice constants
    """
    with open(filepath, 'r') as xyz:
        # TODO: I think you intend to access the first element of an iterator here, probably easier to do
        #    something like xyz.readlines()[1] or the like
        for i, line in enumerate(xyz):
            if i == 1:
                new_line = line.split()
                row_1 = np.array([float(new_line[0][9::]), float(new_line[1]), float(new_line[2])])
                row_2 = np.array([float(new_line[3]), float(new_line[4]), float(new_line[5])])
                row_3 = np.array([float(new_line[6]), float(new_line[7]), float(new_line[8][:-1])])
    return[row_1, row_2, row_3]

def copies_to_fill_cell(cell_size: int, filepath: str, lattice_param: List[float]) -> List[np.ndarray]:
    """
    Have a cubic cell, and fill in periodic copies up to the target cell size
    Create periodic copies of each cell until past the target size, and then remove
    the atoms outside of the target cell size
    Alternative: Get approximate LCM of all structures, but this could blow up quickly

    Args:
        cell_size (int): max dimensions of cell in x/y/z positive direction
        filepath (str): name of file
        lattice_param (list of floats): a,b,c lattice parameters

    Returns:
        nxnxn cubic cell with coordinates
    """
    with open(filepath) as f:
        data = f.readlines()

    a, b, c = lattice_param

    # Read in the initial file
    data = data[2:]  # strip the first 2 lines before the coordinates
    rows = [line.split() for line in data]
    xcoord = [(float(row[1])) for row in rows]
    ycoord = [(float(row[2])) for row in rows]
    zcoord = [(float(row[3])) for row in rows]
    xyz = np.column_stack((xcoord, ycoord, zcoord))

    # append initial xyz coordinates
    xyz_periodic_copies = [xyz]

    for x in range(0, 100):
        for y in range(0, 100):
            for z in range(0, 100):
                if x == 0 and y == 0 and z == 0: continue
                add_vector = x*a + y*b + z*c
                xyz_periodic_copies.append(xyz + add_vector)

    # Combine into one array
    xyz_periodic_total = np.vstack(xyz_periodic_copies)

    # Filter out all atoms outside of the cubic box
    # Keep axes at -10 to include negative xyz coordinates from the original cell
    new_cell = xyz_periodic_total[np.max(xyz_periodic_total, axis=1) < cell_size]
    new_cell = new_cell[np.min(new_cell, axis=1) > -10]

    np.random.seed(42)
    new_cell += np.random.standard_normal(new_cell.shape) * .00001

    return new_cell


if __name__ == '__main__':
    # TODO: is this in a unit test?  If so, delete.
    lattice_csts = lattice_param(DEFAULT_FILEPATHS[0])
    print(lattice_csts)
    size = 50
    new_cell = copies_to_fill_cell(size, DEFAULT_FILEPATHS[0], lattice_csts)
    print(len(new_cell))
    # TODO: leaving this in as reference for pymatgen refactor, but delete before
    #       concluding review
    from pymatgen import Structure, Lattice
    from pymatgen.util.coord import find_in_coord_list_pbc
    #ccc_struct = Structure(Lattice.cubic(size), ["C"]*len(new_cell),
    #                       new_cell, coords_are_cartesian=True)
    #ccc_struct.to(filename="ccc_output_{}.cif".format(size))
    #print(ccc_struct.density)
    # pmg_struct = Structure.from_file("tpmg_output_10.cif")
    # for coord in
