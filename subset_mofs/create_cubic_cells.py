import os
from typing import List, Tuple
from subset_mofs import MOF_TDA_PATH
import numpy as np
from matplotlib import pyplot as plt

MOF_FILES = os.path.join(MOF_TDA_PATH, 'subset_mof_list.txt')
filepath = []
with open(MOF_FILES,'r') as f:
    for line in f:
        line = line.strip()
        stripped_line = line[:-4] #strip .cif off
        filepath.append(stripped_line + ".xyz")

def lattice_param(filepath : str) -> List[float]:
    """
    Return lattice constants for each crystal structure
    Note: this can be replaced with pymatgen

    Args:
        filepath (str): name of file
    Returns:
        List of lattice constants
    """
    with open(filepath, 'r') as xyz:
        for i, line in enumerate(xyz):
            if i == 1:
                newLine = line.split()
#                a = float(newLine[0][9::]) #remove Lattice=" part
                row_1 = np.array([float(newLine[0][9::]), float(newLine[1]), float(newLine[2])])
                row_2 = np.array([float(newLine[3]), float(newLine[4]), float(newLine[5])])
                row_3 = np.array([float(newLine[6]), float(newLine[7]), float(newLine[8][:-1])])
#                b = float(newLine[4])
#                c = float(newLine[8][:-1])
#    return[a,b,c]
    return[row_1, row_2, row_3]

def copies_to_fill_cell(cell_size: int, filepath : str, lattice_param: List[float]) -> List[float]:
    """
    Have a cubic cell, and fill in periodic copies up to the target cell cize
    Create periodic copies of each cell until past the target size, and then remove
    the atoms outside of the target cell size
    Alternative: Get approximate LCM of all structures, but this could blow up quickly

    Args:
        cellSize (int): max dimensions of cell in x/y/z positive direction
        filepath (str): name of file
        lattice_param (list of floats): a,b,c lattice parameters
    Returns:
        nxnxn cubic cell with coordinates
    """
    with open(filepath) as f:
        data = f.readlines()

    a,b,c = lattice_param

    #Read in the initial file
    data = data[2:] #strip the first 2 lines before the coordinates
    rows = [line.split() for line in data]
    xcoord = [(float(row[1])) for row in rows]
    ycoord = [(float(row[2])) for row in rows]
    zcoord = [(float(row[3])) for row in rows]
    xyz = np.column_stack((xcoord, ycoord, zcoord))

    xyz_periodic_copies = []
    #append initial xyz coordinates
    xyz_periodic_copies.append(xyz)

    for x in range(0, 20):
        for y in range(0, 20):
            for z in range(0, 20):
                if x == 0 and y == 0 and z == 0: continue
    #           xyz_periodic_copies.append(xyz + [x*a, y*b, z*c])
                add_vector = x*a + y*b + z*c
                xyz_periodic_copies.append(xyz + add_vector)
    #Combine into one array
    xyz_periodic_total = np.vstack(xyz_periodic_copies)

    #Filter out all atoms outside of the cubic box
    #Keep axes at -10 to include negative xyz coordinates from the original cell
    new_cell = xyz_periodic_total[np.max(xyz_periodic_total, axis = 1) < cell_size]
    new_cell = new_cell[np.min(new_cell, axis = 1) > -3]

    return new_cell

if __name__ == '__main__':
    lattice_csts = lattice_param(filepath[0])
    print(lattice_csts)
    new_cell = copies_to_fill_cell(10, filepath[0], lattice_csts)
    print(len(new_cell))
    from pymatgen import Structure, Lattice
    from pymatgen.utils.coordinates import find_in_coord_list_pbc
    ccc_struct = Structure(Lattice.cubic(10), ["C"]*len(new_cell), new_cell, coords_are_cartesian=True).to(filename="ccc_output_10.cif")
    pmg_struct = Structure.from_file("tpmg_output_10.cif")
    for coord in
