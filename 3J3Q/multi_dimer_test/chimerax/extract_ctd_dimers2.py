
atoms = session.current_model.atoms

# Define the TRP184 atoms
trp184_atoms = atoms.trp184

# Find pairs of chains that are close enough in space based on the distance between TRP184 atoms
chain_pairs = []
for chain1 in models[0].chains:
    for chain2 in models[0].chains:
        if chain1 != chain2 and trp184_atoms[chain1].distance(trp184_atoms[chain2]) <= 10:
            chain_pairs.append((chain1, chain2))

print(chain_pairs)

# Extract CTD dimers for each chain pair
for i, (chain1, chain2) in enumerate(chain_pairs):
    # Select residues 144-231 in each chain
    sel = f"#{models[0].id}:{chain1.id}:144-231 & #{models[0].id}:{chain2.id}:144-231"
    models[0].selection.clear()
    models[0].selection.add(sel)
    
    # Save selected atoms as a PDB file
    fname = f"capsid-dimer-{i+1}.pdb"
    #save sel format pdb file "{fname}"
    #save sel format pdb file "%s/%s-%d.pdb" % (out_dir, root_name, count)
    print(fname)



