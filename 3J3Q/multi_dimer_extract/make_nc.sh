#!/bin/bash
# make a trajectory file from all pentamer or all hexamer pdbs
# using cpptraj

SHAPE="hexs"

CMD="parm parm.pdb \n"

for PDB in $SHAPE/*-leap.pdb ; do 

    # check to make sure that the leap ready pdb is 176 res long with LEU
    lastline=$(tail -2 parm.pdb)
    if [[ $lastline == **'LEU'**  && $lastline == **'176'** ]] ; then
        # if everything checks out, add to nc file
        CMD="$CMD trajin $PDB \n"
    else
        echo "$PDB is NO GOOD"
    fi

done

#CMD="$CMD parmout ${SHAPE}.parm \n"
CMD="$CMD trajout ${SHAPE}.nc \n"

echo -e $CMD | cpptraj
