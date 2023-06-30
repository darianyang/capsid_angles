from Bio.PDB import *
import os

from tqdm.auto import tqdm

# Define the threshold distance for the two chains to be considered a dimer
threshold_distance = 10.0

path_to_cif = "/Users/darian/Downloads/ChimeraX/PDB/3j34.cif"
#path_to_cif = "/Users/darian/Downloads/ChimeraX/PDB/3j3q.cif"

# Load the structure from the CIF file
parser = MMCIFParser()  # create a parser for CIF files
structure = parser.get_structure('3J3Q', path_to_cif)  # load the structure from the CIF file

# Get all the chains in the structure
chains = list(structure.get_chains())

# Set the serial numbers of the chains
for i, chain in enumerate(chains):
    chain.serial_num = i + 1

# Iterate through all possible chain pairs
for i in range(len(chains)):
    for j in range(i+1, len(chains)):
        chain1 = chains[i]
        chain2 = chains[j]

        # Find the residue with index 184 in each chain
        residue1 = chain1[' ', 184, ' ']
        residue2 = chain2[' ', 184, ' ']

        # Calculate the distance between the two residues
        distance = residue1['CA'] - residue2['CA']

        # If the distance is below the threshold, write out the PDB file for the dimer
        if distance < threshold_distance:
            # Create a new structure containing only residues 144 to 231 of each chain
            new_structure = Structure.Structure('dimer')
            new_chain1 = Chain.Chain(chain1.id, chain1.serial_num)
            new_chain2 = Chain.Chain(chain2.id, chain2.serial_num)
            new_structure.add(new_chain1)
            new_structure.add(new_chain2)

            # Copy only residues 144 to 231 from each chain to the new structure
            for residue in chain1.get_residues():
                res_id = residue.get_id()[1]
                if res_id >= 144 and res_id <= 231:
                    new_residue = residue.copy()
                    new_chain1.add(new_residue)
            for residue in chain2.get_residues():
                res_id = residue.get_id()[1]
                if res_id >= 144 and res_id <= 231:
                    new_residue = residue.copy()
                    new_chain2.add(new_residue)

            # Set the serial numbers of the chains
            for chain in new_structure.get_chains():
                chain.serial_num = chain.id

            # Write the new structure out to a PDB file
            io = PDBIO()
            io.set_structure(new_structure)
            io.save('dimer_{}_{}.pdb'.format(chain1.id, chain2.id))
