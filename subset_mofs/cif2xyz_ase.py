import ase
import ase.io

zeoliteFiles = "subset_mof_list.txt"

with open(zeoliteFiles, "r") as f:
    for line in f:
        line = line.strip()
        stripped_line = line[:-4] #remove ".cif" from each line, for labeling
        atoms = ase.io.read(line) #read in cif line
        ase.io.write(stripped_line + '.xyz', atoms)
