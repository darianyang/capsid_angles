#!/bin/bash
# make chimerax command script (cxc)
# for converting a bunch of cif files to pdb

CXC="# convert cif files to pdb \n"

for CIF in hexs/*.cif ; do

    # open in model 1 slot
    CXC="$CXC open $CIF \n"
    # save without last 4 char, replace with .pdb
    CXC="$CXC save ${CIF%????}.pdb \n"
    # close model 1
    CXC="$CXC close #1 \n"

done

echo -e $CXC > cif_to_pdb.cxc
# run cxc script without opening gui and exit chimerax after processing CLI args
chimerax --nogui --script cif_to_pdb.cxc --exit