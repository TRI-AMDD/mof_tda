import unittest
import os

from subset_mofs import MOF_TDA_PATH
from subset_mofs.create_cubic_cells import lattice_param
from pymatgen import Structure, Lattice
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io.xyz import write_xyz


class LatticeTest(unittest.TestCase):
    def test_lattice(self):
        xyz_file = os.path.join(MOF_TDA_PATH, "00958972.2016.1250260_1436516_clean.xyz")
        cif_file = os.path.join(MOF_TDA_PATH, "00958972.2016.1250260_1436516_clean.cif")
        lattice_csts = lattice_param(xyz_file)
        structure = Structure.from_file(cif_file)
        self.assertEqual(lattice_csts[0], structure.lattice.a)
        self.assertEqual(lattice_csts[1], structure.lattice.b)
        self.assertEqual(lattice_csts[2], structure.lattice.c)

    def test_create_cubic_cell(self):
        from subset_mofs.create_cubic_cells import copies_to_fill_cell
        structure = Structure.from_spacegroup("Fm-3m", Lattice.cubic(2.0), ["Ni"],
                                              [[0, 0, 0]])
        self.assertEqual(len(structure), 4)
        with ScratchDir('.'):
            aaa = AseAtomsAdaptor()
            atoms = aaa.get_atoms(structure)
            write_xyz("out.xyz", atoms)
            lattice_params = lattice_param('out.xyz')
            output_coords = copies_to_fill_cell(100, 'out.xyz', lattice_params)
            self.assertEqual(len(output_coords), 50 ** 3 * 4)

    def test_test_pymatgen(self):
        from subset_mofs.test_pymatgen import get_coordinates
        structure = Structure.from_spacegroup("Fm-3m", Lattice.cubic(2.0), ["Ni"],
                                              [[0, 0, 0]])
        self.assertEqual(len(structure), 4)
        with ScratchDir('.'):
            structure.to(filename="out.cif")
            size = 100
            output_coords = get_coordinates(size, 'out.cif')
            self.assertEqual(len(output_coords), (size / 2) ** 3 * 4)


if __name__ == '__main__':
    unittest.main()
