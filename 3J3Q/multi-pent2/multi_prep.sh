#!/bin/bash
# prep multiple pdb files for amber

# make dir for output
if [ ! -d "pdb4amber_out" ] ; then
    mkdir pdb4amber_out
fi

for I in {1..5} ; do 

    # run pdb4amber with:
    # --reduce for protonation
    # --model -1 for using all models
    # --no-conect to not write disulfide bonds
    pdb4amber -i pent-dim${I}.pdb -o pent-dim${I}-leap.pdb --reduce --model -1 --no-conect &&
    # clean up
    mv pent-dim${I}-leap_sslink pdb4amber_out
    mv pent-dim${I}-leap_renum.txt pdb4amber_out
    mv pent-dim${I}-leap_nonprot.pdb pdb4amber_out

done

mv reduce_info.log pdb4amber_out
