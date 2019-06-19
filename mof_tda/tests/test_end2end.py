import unittest
import os
import numpy as np
import pickle

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes
from mof_tda.cif2xyz_ase import cif2xyz
from mof_tda.create_cubic_cells import copies_to_fill_cell, lattice_param
from mof_tda.get_delaunay_triangulation import get_delaunay_simplices, get_persistence
from pymatgen import Structure, Lattice
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io.xyz import write_xyz

class EndToEndTest(unittest.TestCase):
    def workflow(self):
        filepath = []
        with open(os.path.join(MOF_TDA_PATH, 'allMOFs_without_disorder.txt'),'r') as f:
            for line in f:
                line = line.strip()
                filepath.append(line)
        total_volume = pickle.load(open(os.path.join(MOF_TDA_PATH,'tot_volume.pkl'), 'rb'))
        lowest_mof_list = get_lowest_volumes(1, total_volume, filepath)
        #also generates a file that can be read by ase
        cif2xyz(os.path.join(MOF_TDA_PATH,'mof_structures.txt'))

        filepaths = []
        MOF_FILES = os.path.join(MOF_TDA_PATH, 'mof_structures.txt')
        with open(MOF_FILES,'r') as f:
            for line in f:
                line = line.strip()
                stripped_line = line[:-4] #strip .cif off
                filepaths.append(stripped_line + ".xyz")

        lattice_csts = lattice_param(filepaths[0])
        new_cell = copies_to_fill_cell(90, filepaths[0], lattice_csts)
        simplices = get_delaunay_simplices(new_cell)
        dgms = get_persistence(simplices)
        print(dgms)

if __name__ == '__main__':
    unittest.main()
