import unittest
import os
import pickle

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes
from mof_tda.convert_structure import convert_cif_to_xyz
from mof_tda.create_cubic_cells import copies_to_fill_cell, lattice_param
from mof_tda.get_delaunay_triangulation import get_delaunay_simplices, get_persistence


class EndToEndTest(unittest.TestCase):
    # TODO: note that methods in TestCases won't be run unless they contain "test", delete this comment
    def test_workflow(self):
        filepath = []
        with open(os.path.join(MOF_TDA_PATH, 'allMOFs_without_disorder.txt'),'r') as f:
            for line in f:
                line = line.strip()
                filepath.append(line)
        total_volume = pickle.load(open(os.path.join(MOF_TDA_PATH, 'tot_volume.pkl'), 'rb'))

        # TODO: test something about this variable
        lowest_mof_list = get_lowest_volumes(1, total_volume, filepath)

        # Also generates a file that can be read by ase
        convert_cif_to_xyz(os.path.join(MOF_TDA_PATH, 'mof_structures.txt'))

        # TODO: Remove duplicated code here
        filepaths = []
        mof_files = os.path.join(MOF_TDA_PATH, 'mof_structures.txt')
        with open(mof_files,'r') as f:
            for line in f:
                line = line.strip()
                stripped_line = line[:-4]  # strip .cif off
                filepaths.append(stripped_line + ".xyz")

        lattice_csts = lattice_param(filepaths[0])
        new_cell = copies_to_fill_cell(90, filepaths[0], lattice_csts)
        simplices = get_delaunay_simplices(new_cell)
        dgms = get_persistence(simplices)
        print(dgms)


if __name__ == '__main__':
    unittest.main()
