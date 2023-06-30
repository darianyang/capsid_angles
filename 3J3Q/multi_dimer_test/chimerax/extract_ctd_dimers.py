
# Define a cutoff distance for detecting TRP 184 residues that are close in space
distance_cutoff = 10

# Get all the TRP 184 residues in the structure
trp184_atoms = atoms :/trp184

# Initialize a list to store the dimer chains
dimer_chains = []

# Loop through all the TRP 184 residues
for trp184_atom in trp184_atoms
    # Get the monomer chain and residue number
    monomer_chain_id = trp184_atom.chain.id_string
    monomer_residue_number = trp184_atom.residue.number

    # Get all the other TRP 184 atoms that are close in space
    close_atoms = atoms @{:10 of atoms within $distance_cutoff of trp184_atom}

    # Loop through the close atoms
    for close_atom in close_atoms
        # Get the other monomer chain and residue number
        other_chain_id = close_atom.chain.id_string
        other_residue_number = close_atom.residue.number

        # Check if the monomer and other chain IDs are different and if the other residue number is greater than the monomer residue number
        if monomer_chain_id != other_chain_id and other_residue_number > monomer_residue_number
            # Get the chain IDs of the dimer
            chain_ids = [monomer_chain_id, other_chain_id]

            # Sort the chain IDs alphabetically
            chain_ids.sort()

            # Add the chain IDs to the dimer chains list
            if chain_ids not in dimer_chains
                dimer_chains.append(chain_ids)

# Loop through the dimer chains
for i, chain_ids in enumerate(dimer_chains)
    # Get the chain objects
    chain_objects = chains :/({0:s}|{1:s})$format(chain_ids[0], chain_ids[1])

    # Select the CTD residues
    ctd_atoms = atoms :/({0:s}|{1:s})@144-231$format(chain_ids[0], chain_ids[1])
    ctd_atoms.selected = True

    # Save the selected atoms to a PDB file
    save capsid-dimer-{0:d}.pdb selectedOnly true relModel #1 format pdb$format(i+1)

