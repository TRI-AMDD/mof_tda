import unittest
import os

from subset_mofs import MOF_TDA_PATH
from subset_mofs.create_cubic_cells import lattice_param
from pymatgen import Structure


class LatticeTest(unittest.TestCase):
    def test_lattice(self):
        xyz_file = os.path.join(MOF_TDA_PATH, "00958972.2016.1250260_1436516_clean.xyz")
        cif_file = os.path.join(MOF_TDA_PATH, "00958972.2016.1250260_1436516_clean.cif")
        lattice_csts = lattice_param(xyz_file)
        structure = Structure.from_file(cif_file)
        self.assertEqual(lattice_csts[0], structure.lattice.a)
        self.assertEqual(lattice_csts[1], structure.lattice.b)
        self.assertEqual(lattice_csts[2], structure.lattice.c)


if __name__ == '__main__':
    unittest.main()
