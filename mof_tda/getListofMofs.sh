# TODO: this should be unnecessary after glob refactor, delete when done

#!/bin/bash

for file in *.cif
	do
	echo $file >> subset_mof_list.txt
	done

