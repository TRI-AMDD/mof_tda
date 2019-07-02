from pymatgen import Structure, Molecule
from mof_tda.create_cubic_cells import lattice_param as lattice_param_xyz
import numpy as np
from typing import List
from pymatgen.analysis.structure_matcher import StructureMatcher


# TODO: use whatever you need from here, delete everything else
def lattice_param(filepath : str) -> List[float]:
    """
    Lattice constants for each parameter
    """
    structure = Structure.from_file(filepath)
    print("Original structure density: {}".format(structure.density))
    a = structure.lattice.a
    b = structure.lattice.b
    c = structure.lattice.c
    return[a,b,c]

def struct_from_xyz(xyz_filename):
    molecule = Molecule.from_file(xyz_filename)
    lattice_matrix = lattice_param_xyz
    return Structure(lattice_matrix, molecule.species,
                     molecule.coords, coords_are_cartesian=True)

def get_coordinates(size, filepath, lattice_csts=None):
    import nose; nose.tools.set_trace()
    if "xyz" in filepath:
        structure = struct_from_xyz(filepath)
    else:
        structure = Structure.from_file(filepath)
    lattice = structure.lattice
    print(lattice)
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
    scaling_matrix = lattice.get_fractional_coords(np.eye(3) * size)
    super_structure = structure.copy()
    super_structure.make_supercell(np.floor(scaling_matrix))
    print(scaling_matrix)
    print(lattice.matrix)

    #Combine into one array
    xyz_periodic_total = super_structure.cart_coords# np.vstack(xyz_periodic_copies)

    #Filter out all atoms outside of the cubic box, include atoms just below 0
    new_cell = xyz_periodic_total[np.max(xyz_periodic_total, axis = 1) < size + 1e-6]
    new_cell = new_cell[np.min(new_cell, axis = 1) > -3]

    new_cell += np.random.standard_normal(new_cell.shape) * .00001

    print(len(xyz))
    print(len(new_cell))
    print(len(super_structure))
    super_structure.replace_species({x: "C" for x in super_structure.composition})
    print("super structure density: {}".format(super_structure.density))
    return new_cell


if __name__ == '__main__':
    structure_matcher = StructureMatcher()
    struct_xyz = struct_from_xyz("00958972.2016.1250260_1436516_clean.xyz")
    struct_cif = Structure.from_file("00958972.2016.1250260_1436516_clean.cif")
    this_fit = structure_matcher.fit(struct_xyz, struct_cif)
    assert this_fit
    lattice_csts = lattice_param('00958972.2016.1250260_1436516_clean.cif')
    size = 200
    new_cell = get_coordinates(size, '00958972.2016.1250260_1436516_clean.cif', lattice_csts)
    from pymatgen import Structure, Lattice
    pmg_struct = Structure(Lattice.cubic(size), ["C"]*len(new_cell),
                           new_cell, coords_are_cartesian=True)
    pmg_struct.to(filename="pmg_output_{}.cif".format(size))
    print(pmg_struct.density)
    # Structure(Lattice.cubic(10), ["C"]*len(new_cell), new_cell, coords_are_cartesian=True).to(filename="tpmg_output_10.cif")
