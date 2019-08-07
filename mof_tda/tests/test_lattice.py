import unittest
import os
import numpy as np

from mof_tda import MOF_TDA_PATH, MOF_TDA_TEST_FILE_PATH
from mof_tda.create_cubic_cells import lattice_param
from pymatgen import Structure, Lattice
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io.xyz import write_xyz


class LatticeTest(unittest.TestCase):
    def test_lattice(self):
        xyz_file = os.path.join(MOF_TDA_TEST_FILE_PATH, "00958972.2016.1250260_1436516_clean.xyz")
        cif_file = os.path.join(MOF_TDA_TEST_FILE_PATH, "00958972.2016.1250260_1436516_clean.cif")
        lattice_csts = lattice_param(xyz_file)
        structure = Structure.from_file(cif_file)
        self.assertAlmostEqual(np.linalg.norm(lattice_csts[0]), structure.lattice.a)
        self.assertAlmostEqual(np.linalg.norm(lattice_csts[1]), structure.lattice.b)
        self.assertAlmostEqual(np.linalg.norm(lattice_csts[2]), structure.lattice.c)

    def test_create_cubic_cell(self):
        from mof_tda.create_cubic_cells import copies_to_fill_cell
        structure = Structure.from_spacegroup("Fm-3m", Lattice.cubic(2.0), ["Ni"],
                                              [[0, 0, 0]])
        self.assertEqual(len(structure), 4)
        with ScratchDir('.'):
            aaa = AseAtomsAdaptor()
            atoms = aaa.get_atoms(structure)
            write_xyz("out.xyz", atoms)
            lattice_params = lattice_param('out.xyz')
            size = 100
            output_coords = copies_to_fill_cell(size, 'out.xyz', lattice_params)
            self.assertEqual(len(output_coords), (size/2) ** 3 * 4)

        # Try with primitive cell
        with ScratchDir('.'):
            aaa = AseAtomsAdaptor()
            atoms = aaa.get_atoms(structure.get_primitive_structure())
            write_xyz("out.xyz", atoms)
            lattice_params = lattice_param('out.xyz')
            # TODO: test something about this variable
            output_coords = copies_to_fill_cell(size, 'out.xyz', lattice_params)

    # TODO: delete this if not used
    @unittest.skip
    def test_test_pymatgen(self):
        from mof_tda.test_pymatgen import get_coordinates
        structure = Structure.from_spacegroup("Fm-3m", Lattice.cubic(2.0), ["Ni"],
                                              [[0, 0, 0]])
        self.assertEqual(len(structure), 4)
        with ScratchDir('.'):
            structure.to(filename="out.cif")
            size = 100
            output_coords = get_coordinates(size, 'out.cif')
            self.assertEqual(len(output_coords), (size / 2) ** 3 * 4)

        with ScratchDir('.'):
            structure.get_primitive_structure().to(filename="out.cif")
            size = 100
            output_coords = get_coordinates(size, 'out.cif')
            self.assertEqual(len(output_coords), (size / 2) ** 3 * 4)


if __name__ == '__main__':
    unittest.main()
