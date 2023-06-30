from Bio import PDB
from Bio.PDB import MMCIFParser
from Bio.PDB.mmcifio import MMCIFIO
#from Bio.PDB import Select, Chain, Atom
from tqdm.auto import tqdm

path_to_cif = "/Users/darian/Downloads/ChimeraX/PDB/3j3q.cif"
#path_to_cif = "/Users/darian/Downloads/ChimeraX/PDB/3j34.cif" 
#path_to_cif = "/Users/darian/Desktop/pent-of-pent.cif" 

# Load the structure from the CIF file
parser = MMCIFParser()  # create a parser for CIF files
structure = parser.get_structure('3J3Q', path_to_cif)  # load the structure from the CIF file

# Define the distance cutoff for detecting dimers
cutoff = 20

# Define the reference residue (184 in this case)
ref_residue = 184

# Define the list of chains in the structure
chains = list(structure.get_chains())

# # Iterate through all possible chain pairs
# for i in range(len(chains)):
#     for j in range(i+1, len(chains)):
#         chain1 = chains[i]
#         chain2 = chains[j]

# Loop over all chain pairs
for i, chain1 in enumerate(tqdm(chains)):
#for i, chain1 in enumerate(chains):
    for chain2 in chains[i+1:]:
        # Calculate the distance between the reference residue in the two chains
        # Find the residue with index 184 in each chain
        residue1 = chain1[' ', ref_residue, ' ']
        residue2 = chain2[' ', ref_residue, ' ']
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
            # note that PDB does not work with chains >= 2 letters so mmCIF needed
            #io = PDB.PDBIO()
            io = MMCIFIO()
            io.set_structure(new_structure)
            #print(chain1.id, chain2.id)
            #io.save('dimer_{}_{}.pdb'.format(chain1.id, chain2.id))

            # chains that are apart of pentamers
            pent_chains = ['i', 'j', 'g', 'h', 'f', 'J', 'N', 'M', 'L', 'K', 'T', 'U', 'V', 'W', 'X', 'H', 'G', 'F', 'E', 'I', 'A', 'z', 'D', 'C', 'B', 'S', 'R', 'Q', 'P', 'O', 'p', 't', 's', 'r', 'q', 'd', 'c', 'b', 'a', 'e', '1', '0', '4', '3', '2', '8', '7', '6', '5', '9', 'm', 'n', 'o', 'k', 'I', 'y', 'u', 'v', 'w', 'x']

            # t/e block for any weird CTDs that are not homogenous            
            try:
                # if one of the chains is apart of a pentamer
                if chain1.id in pent_chains or chain2.id in pent_chains:
                    save_dir = "pents/"
                # otherwise will be apart of hexamers
                else:
                    save_dir = "hexs/"
                io.save(f'{save_dir}/dimer_{chain1.id}_{chain2.id}.cif')
            except TypeError as e:
                print(f"ERROR {e}: for {chain1.id} and {chain2.id}")
