import unittest
import os

from mof_tda import MOF_TDA_PATH
from mof_tda.main import main


class EndToEndTest(unittest.TestCase):
    def test_main(self):
        persistence_diagram, current_file = main(0, 1)

        # Check that the pickled file is the same as the item in the list: mof_structures contains cif
        with open(os.path.join(MOF_TDA_PATH, "mof_structures.txt"), "r") as f:
            data = f.readlines()
            self.assertEqual(current_file[:-4], data[0][:-5])


if __name__ == '__main__':
    unittest.main()
