import unittest
import os
import numpy as np
import pickle

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes
from mof_tda.convert_structure import convert_cif_to_xyz
from mof_tda.create_cubic_cells import copies_to_fill_cell, lattice_param
from mof_tda.get_delaunay_triangulation import get_delaunay_simplices, get_persistence
from mof_tda.main import main
from pymatgen import Structure, Lattice
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io.xyz import write_xyz

class EndToEndTest(unittest.TestCase):
    def test_main(self):
        persistence_diagram, current_file = main(0, 1)

        #check that the pickled file is the same as the item in the list: mof_structures contains cif
        with open(os.path.join(MOF_TDA_PATH, "mof_structures.txt"), "r") as f:
            data = f.readlines()
            self.assertEqual(current_file[:-4], data[0][:-5])

if __name__ == '__main__':
    unittest.main()
