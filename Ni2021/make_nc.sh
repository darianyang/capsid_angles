#!/bin/bash
# make a trajectory file from all pentamer or all hexamer pdbs
# using cpptraj

SHAPE="hexs"

CMD="parm parm.pdb \n"

for PDB in ${SHAPE}_combined/*-leap.pdb ; do 

    # check to make sure that the leap ready pdb is 156 res long with VAL as last
    lastline=$(tail -2 parm.pdb)
    if [[ $lastline == **'VAL'**  && $lastline == **'156'** ]] ; then
        # if everything checks out, add to nc file
        CMD="$CMD trajin $PDB \n"
    else
        echo "$PDB is NO GOOD"
    fi

done

#CMD="$CMD fixatomorder"
#CMD="$CMD parmout ${SHAPE}.parm \n"
CMD="$CMD trajout ${SHAPE}.nc \n"

echo -e $CMD | cpptraj
