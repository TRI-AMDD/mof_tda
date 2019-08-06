import ase.io
import os
from mof_tda import MOF_TDA_PATH


# TODO: the structure_list parameter seems unnecessary here,
#   let's refactor to take in a directory that contains cif files
#   then use glob to get a list of all cif files in that directory
def convert_cif_to_xyz(structure_list: str) -> None:
    """
    Converts cif files to xyz files

    Args:
        structure_list (str): name of file containing all the cif structures
    """
    if not os.path.exists(os.path.join(MOF_TDA_PATH, 'xyz_structures')):
        os.mkdir('xyz_structures')
    with open(os.path.join(MOF_TDA_PATH, structure_list), "r") as f:
        for line in f:
            line = line.strip()
            stripped_line = line[:-4]  # remove ".cif" from each line, for labeling
            # Go to path that contains all the cif files
            os.chdir(os.path.join(MOF_TDA_PATH, 'all_MOFs'))
            atoms = ase.io.read(line)  # read in cif line
            ase.io.write(os.path.join(MOF_TDA_PATH, 'xyz_structures',  stripped_line+'.xyz'), atoms)


if __name__ == '__main__':
    convert_cif_to_xyz('subset_mof_list.txt')
