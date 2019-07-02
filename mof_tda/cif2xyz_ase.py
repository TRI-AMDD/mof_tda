import os
import ase
import ase.io
import os
from typing import List
from mof_tda import MOF_TDA_PATH

def cif2xyz(structure_list : str) -> None:
    """
    Converts cif files to xyz files
    Arg: name of file containing all the cif structures
    """
    if not os.path.exists(os.path.join(MOF_TDA_PATH, './xyz_structures')):
        os.mkdir('xyz_structures')
    with open(os.path.join(MOF_TDA_PATH, structure_list), "r") as struct_list:
        for line in struct_list:
            line = line.strip()
            stripped_line = line[:-4] #remove ".cif" from each line, for labeling
            #go to path that contains all the cif files
            os.chdir(os.path.join(MOF_TDA_PATH, 'all_MOFs'))
            atoms = ase.io.read(line) #read in cif line
            ase.io.write(os.path.join(MOF_TDA_PATH, './xyz_structures/' + \
                        stripped_line + '.xyz'), atoms)

if __name__ == '__main__':
    cif2xyz('subset_mof_list.txt')
