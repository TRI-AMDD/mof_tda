from pymatgen import Structure
import numpy as np
from typing import List, Tuple

def lattice_param(filepath : str) -> List[float]:
    """
    Lattice constants for each parameter
    """
    structure = Structure.from_file(filepath)
    a = structure.lattice.a
    b = structure.lattice.b
    c = structure.lattice.c
    return[a,b,c]

def get_coordinates(filepath, lattice_csts):
    structure = Structure.from_file(filepath)
    xyz = structure.cart_coords
    xyz_periodic_copies = []

    xyz_periodic_copies.append(xyz)

    """
    for x in range(0, 20):
        for y in range(0, 20):
            for z in range(0, 20):
                if x == 0 and y == 0 and z == 0: continue
                xyz_periodic_copies.append(xyz + lattice_csts*xyz)
    """
    supercell = structure.make_supercell([3,3,3])

    #Combine into one array
    xyz_periodic_total = np.vstack(xyz_periodic_copies)

    #Filter out all atoms outside of the cubic box, include atoms just below 0
    new_cell = xyz_periodic_total[np.max(xyz_periodic_total, axis = 1) < 80]
    new_cell = new_cell[np.min(new_cell, axis = 1) > -2]

    new_cell += np.random.standard_normal(new_cell.shape) * .00001

    print(len(xyz))
    print(len(new_cell))
    print(len(supercell))

if __name__ == '__main__':
    lattice_csts = lattice_param('00958972.2016.1250260_1436516_clean.cif')
    get_coordinates('00958972.2016.1250260_1436516_clean.cif', lattice_csts)
