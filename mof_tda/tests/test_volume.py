import unittest
import os
import pickle

from mof_tda import MOF_TDA_PATH
from mof_tda.narrow_mof_dataset import get_lowest_volumes


class VolumeTest(unittest.TestCase):
    def test_volume(self):
        # TODO: duplicate code, refactor/delete
        filepath = []
        with open(os.path.join(MOF_TDA_PATH, 'allMOFs_without_disorder.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                filepath.append(line)

        total_volume = pickle.load(open(os.path.join(MOF_TDA_PATH, 'tot_volume.pkl'), 'rb'))
        minimum_index = total_volume.index(min(total_volume))
        filepath_min = filepath[minimum_index]

        # Returns a list
        new_mof_list, sorted_lowest_n = get_lowest_volumes(1, total_volume, filepath)
        self.assertEqual(filepath_min, new_mof_list[0])


if __name__ == '__main__':
    unittest.main()
