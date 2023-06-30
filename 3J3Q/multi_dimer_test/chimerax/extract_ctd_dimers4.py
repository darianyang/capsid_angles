import os
from chimerax.core.commands import run
from chimerax.core.session import Session


# Define output directory and root filename
out_dir = "/path/to/output/dir"
root_name = "capsid-dimer"

#session = Session()
atoms = session.models[0].atoms

# Get current model
models = session.models
if not models:
    raise ValueError("No models in ChimeraX session")
model = models[0]

# Select all residues with index 144-231
residues = model.residues
selection = residues[144:232]

# Loop through all CTD dimer interfaces
count = 0
for res1 in selection:
    for res2 in selection:
        if res1 == res2:
            continue
        if res1.structure != res2.structure:
            continue
        if res1.chain_id == res2.chain_id:
            continue
        # Check if residues are close in space
        dist = res1.side_chain_atoms.coord - res2.side_chain_atoms.coord
        if dist.norm() > 10:
            continue
        # Create selection for the two chains
        chain_sel = "/%s,%s" % (res1.chain_id, res2.chain_id)
        sel = selection.chain_selection(chain_sel)
        if sel:
            count += 1
            # Save selection as PDB file
            fname = "%s-%d" % (root_name, count)
            run("save sel format pdb file \"%s/%s.pdb\"" % (out_dir, fname))

