import os
from Bio import PDB

def combine_models(input_path, output_path):
    # Load the PDB file
    parser = PDB.PDBParser()
    structure = parser.get_structure("combined_model", input_path)

    # Get the first model
    model1 = structure[0]

    # Get the second model
    model2 = structure[1]

    # Create a new structure to hold the combined model
    combined_structure = PDB.Structure.Structure("combined_model")

    # Create a new model and add it to the combined structure
    combined_model = PDB.Model.Model(0)
    combined_structure.add(combined_model)

    # Iterate over all chains in the first model and add them to the combined model
    for chain in model1:
        combined_model.add(chain)

    # Iterate over all chains in the second model, modify the chain ID, and add them to the combined model
    for i, chain in enumerate(model2):
        # Assign unique chain ID using alphabetic characters (A = 65)
        chain.id = chr(66 + i) 
        combined_model.add(chain)

    # Save the combined structure to a new PDB file
    io = PDB.PDBIO()
    io.set_structure(combined_structure)
    io.save(output_path)


# Directory containing PDB files
pdb_directory = "hexs"
# Output directory for combined PDB files
output_directory = "hexs_combined"

# Loop through PDB files in the directory
for file_name in os.listdir(pdb_directory):
    if file_name.endswith(".pdb"):
        pdb_file = os.path.join(pdb_directory, file_name)
        output_file = os.path.join(output_directory, file_name)
        combine_models(pdb_file, output_file)
