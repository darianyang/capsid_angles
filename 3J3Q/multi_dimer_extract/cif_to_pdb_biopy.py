
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.PDBIO import PDBIO

# Parse the CIF file
parser = MMCIFParser()
structure = parser.get_structure("my_structure", "pents/dimer_f_jn.cif")

# TODO: set chain ID to be blank then save for all mmCIF files

# Save the structure as a PDB file
io = PDBIO()
io.set_structure(structure)
io.save("test.pdb")