#!/bin/bash

for I in {1..5} ; do
    echo "--------------------------------------"
    echo "pent-dim${I}-leap.pdb"
    cat pent-dim${I}-leap/o_angle.dat
    cat pent-dim${I}-leap/c2_angle.dat
    echo "--------------------------------------"
done
