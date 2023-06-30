#!/bin/bash

PDB=hex-dim

for I in {1..6} ; do
    echo "--------------------------------------"
    echo "$PDB${I}-leap.pdb"
    cat $PDB${I}-leap/o_angle.dat
    cat $PDB${I}-leap/c2_angle.dat
    echo "--------------------------------------"
done
