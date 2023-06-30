import os
import re
from chimerax.atomic import Atoms

# Define the TRP 184 residue pattern
trp184_pattern = re.compile("^TRP\s+A\s+184$")

# Get the atoms in the currently open model
atoms = Atoms(session.current_model.atoms)

# Create a list of all TRP 184 atoms
trp184_atoms = atoms[residue for residue in atoms.residues if trp184_pattern.match(residue.name)]

# Create a list of all unique chain IDs in the model
chain_ids = set(atom.structure.chain_ids[0] for atom in atoms)

# Loop over all pairs of chains
count = 0
for chain_id1 in chain_ids:
    for chain_id2 in chain_ids:
        if chain_id1 < chain_id2:
            # Get the TRP 184 atoms for each chain
            trp184_chain1 = trp184_atoms.filter(trp184_atoms.structure.chain_ids == chain_id1)
            trp184_chain2 = trp184_atoms.filter(trp184_atoms.structure.chain_ids == chain_id2)
            
            # Calculate the distance between the TRP 184 atoms
            distance = trp184_chain1.distance(trp184_chain2).min()
            
            # Check if the TRP 184 atoms are close enough to be part of a dimer interface
            if distance < 7:
                # Select the CTD dimer atoms
                selection_string = f"/{chain_id1} & :144-231 | /{chain_id2} & :144-231"
                atoms_to_save = atoms.select(selection_string)
                
                # Save the selected atoms as a PDB file
                root_name = os.path.splitext(os.path.basename(session.current_model.path))[0]
                out_dir = "/Users/darian/Drive/MBSB/Research/Projects/hiv1_capsid/pdb_files/full_capsid_3J3Q/multi_dimer_test" 
                count += 1
                fname = f"{root_name}-{count}.pdb"
                atoms_to_save.write_pdb(os.path.join(out_dir, fname))

