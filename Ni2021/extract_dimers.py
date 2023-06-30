from Bio import PDB
#from Bio.PDB import MMCIFParser
from Bio.PDB import PDBParser
from Bio.PDB.mmcifio import MMCIFIO
#from Bio.PDB import Select, Chain, Atom
from tqdm.auto import tqdm
import sys

#path_to_pdb = "/Users/darian/Desktop/2021capsid/multi-pent.pdb" 
#path_to_pdb = "/Users/darian/Desktop/2021capsid/Ni2021_models_cut.pdb" 
path_to_pdb = "/Users/darian/Desktop/2021capsid/Ni2021_models.pdb" 
model_name = "Ni2021"

# Load the structure from the CIF file
parser = PDBParser()  # create a parser for CIF files
# load the structure from the PDB file
structure = parser.get_structure(model_name, path_to_pdb) 

# Define the distance cutoff for detecting dimers
cutoff = 20

# Define the reference residue (184 in this case)
ref_residue = 184

# Define the list of chains in the structure
# for Ni2021, each model is a single CA
# note that biopython indexes models by 0 and chimeraX does it by 1
chains = list(structure.get_chains())
print(chains)
models = list(structure.get_models())
print(models)
import sys ; exit(0)

# Loop over all model pairs
for i, model1 in enumerate(tqdm(models)):
    for model2 in models[i+1:]:
        # Calculate the distance between the reference residue in the two chains
        # Find the residue with index 184 in each chain
        #print(model1['H'][184])

        residue1 = model1[0, ref_residue, " "]
        residue2 = model2[0, ref_residue, " "]
        distance = residue1["CA"] - residue2["CA"]
        print("HMM", distance)
        import sys ; exit(0)
        # If the distance is less than the cutoff, extract the dimer
        if distance <= cutoff:
            # Create new empty models
            new_model1 = []
            new_model2 = []

            # Loop over residues in the range 144-221 and copy them to the new chains
            for residue in model1.get_residues():
                if residue.id[1] >= 144 and residue.id[1] <= 221:
                    new_model1.add(residue.copy())
            
            for residue in model2.get_residues():
                if residue.id[1] >= 144 and residue.id[1] <= 221:
                    new_model2.add(residue.copy())

            # Create a new model for the dimer
            new_model = PDB.Model.Model(0)
            new_model.add(new_model1)
            new_model.add(new_model2)

            # Create a new structure and add the model to it
            new_structure = PDB.Structure.Structure(model_name)
            new_structure.add(new_model)

            # Save the PDB file for the dimer
            # note that PDB does not work with chains >= 2 letters so mmCIF needed
            io = PDB.PDBIO()
            #io = MMCIFIO()
            io.set_structure(new_structure)
            #print(chain1.id, chain2.id)
            #io.save('dimer_{}_{}.pdb'.format(chain1.id, chain2.id))

            # chains that are apart of pentamers
            # TODO: replace with (models - 1)
            pent_chains = ['i', 'j', 'g', 'h', 'f', 'J', 'N', 'M', 'L', 'K', 'T', 'U', 'V', 'W', 'X', 'H', 'G', 'F', 'E', 'I', 'A', 'z', 'D', 'C', 'B', 'S', 'R', 'Q', 'P', 'O', 'p', 't', 's', 'r', 'q', 'd', 'c', 'b', 'a', 'e', '1', '0', '4', '3', '2', '8', '7', '6', '5', '9', 'm', 'n', 'o', 'k', 'I', 'y', 'u', 'v', 'w', 'x']

            # t/e block for any weird CTDs that are not homogenous            
            try:
                # if one of the chains is apart of a pentamer
                if model1.id in pent_chains or model2.id in pent_chains:
                    save_dir = "pents/"
                # otherwise will be apart of hexamers
                else:
                    save_dir = "hexs/"
                io.save(f'{save_dir}/dimer_{model1.id}_{model2.id}.pdb')
            except TypeError as e:
                print(f"ERROR {e}: for {model1.id} and {model2.id}")
