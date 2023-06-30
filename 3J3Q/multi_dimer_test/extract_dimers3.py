from Bio import PDB
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

# Define the distance cutoff for detecting dimers
cutoff = 20

# Define the reference residue (184 in this case)
ref_residue = '184'

# Define the list of chains in the structure
chains = list(structure.get_chains())

# Loop over all chain pairs
for i, chain1 in enumerate(chains):
    for chain2 in chains[i+1:]:
        # Calculate the distance between the reference residue in the two chains
        # Find the residue with index 184 in each chain
        residue1 = chain1[' ', 184, ' ']
        residue2 = chain2[' ', 184, ' ']
        distance = residue1["CA"] - residue2["CA"]
        
        # If the distance is less than the cutoff, extract the dimer
        if distance <= cutoff:
            # Create new Chain instances for the dimer
            new_chain1 = PDB.Chain.Chain(chain1.id)
            new_chain2 = PDB.Chain.Chain(chain2.id)

            # Loop over residues in the range 144-231 and copy them to the new chains
            for residue in chain1:
                if residue.id[1] >= 144 and residue.id[1] <= 231:
                    new_chain1.add(residue.copy())
            
            for residue in chain2:
                if residue.id[1] >= 144 and residue.id[1] <= 231:
                    new_chain2.add(residue.copy())

            # Create a new model for the dimer
            new_model = PDB.Model.Model(0)
            new_model.add(new_chain1)
            new_model.add(new_chain2)

            # Create a new structure and add the model to it
            new_structure = PDB.Structure.Structure("3J3Q")
            new_structure.add(new_model)

            # Save the PDB file for the dimer
            io = PDB.PDBIO()
            io.set_structure(new_structure)
            io.save('dimer_{}_{}.pdb'.format(chain1.id, chain2.id))
