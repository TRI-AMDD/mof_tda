import unittest
import os
import numpy as np
import pickle

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes
from pymatgen import Structure, Lattice
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io.xyz import write_xyz

class VolumeTest(unittest.TestCase):
    def test_volume(self):
        filepath = []
        with open(os.path.join(MOF_TDA_PATH, 'allMOFs_without_disorder.txt'),'r') as f:
            for line in f:
                line = line.strip()
                filepath.append(line)

        total_volume = pickle.load(open(os.path.join(MOF_TDA_PATH, 'tot_volume.pkl'), 'rb'))
        minimum_index = total_volume.index(min(total_volume))
        filepath_min = filepath[minimum_index]

        #returns a list
        new_mof_list = get_lowest_volumes(1, total_volume, filepath)

        self.assertEqual(filepath_min, new_mof_list[0])

if __name__ == '__main__':
    unittest.main()
