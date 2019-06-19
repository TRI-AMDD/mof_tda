import os
import ase
import ase.io
import os
from typing import List

<<<<<<< HEAD
def cif2xyz(structure_list : List[str]) -> None:
    """
    Converts cif files to xyz files
    Arg: name of file containing all the cif structures
    """
    if os.path.exists('./xyz_structures') == False:
        os.mkdir('xyz_structures')
    with open(structure_list, "r") as f:
        for line in f:
            line = line.strip()
            stripped_line = line[:-4] #remove ".cif" from each line, for labeling
            atoms = ase.io.read(line) #read in cif line
            ase.io.write('./xyz_structures/' + stripped_line + '.xyz', atoms)
=======
from subset_mofs import MOF_TDA_PATH

zeoliteFiles = os.path.join(MOF_TDA_PATH, "subset_mof_list.txt")
>>>>>>> 56633fd3123deac63daa32970def503d1c7bb69a

if __name__ == '__main__':
    cif2xyz('subset_mof_list.txt')
