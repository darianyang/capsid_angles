import os
from chimerax.core.session import Session

# Create output directory if it doesn't exist
out_dir = 'ctd_dimers'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Get current atoms and residues
atoms = session.models[0].atoms
residues = atoms.residues

# Define function to check if residues are in close proximity
def check_proximity(r1, r2):
    r1_atoms = r1.atoms
    r2_atoms = r2.atoms
    for a1 in r1_atoms:
        for a2 in r2_atoms:
            if a1.coord.distance(a2.coord) < 6:
                return True
    return False

# Loop over all residues with ID 184
for r1 in residues[residues.ids == 184]:
    r1_chain = r1.chain_id
    r1_resnum = r1.number
    for r2 in residues[residues.ids == 184]:
        r2_chain = r2.chain_id
        r2_resnum = r2.number
        # Check if residues are in different chains and in close proximity
        if r1_chain != r2_chain and check_proximity(r1, r2):
            # Select the atoms in the two residues
            sel = atoms[(atoms.residues == r1) | (atoms.residues == r2)]
            # Save the selection as a PDB file
            fname = f"{out_dir}/{r1_chain}{r1_resnum}_{r2_chain}{r2_resnum}.pdb"
            sel.write_pdb(fname)

