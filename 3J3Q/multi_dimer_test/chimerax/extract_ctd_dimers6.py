from chimerax.core.session import Session
from chimerax.atomic import AtomicStructure

# Open PDB file
pdb_file = '/Users/darian/Downloads/ChimeraX/PDB/3j3q.cif'
atomic_structure = session.open_command.open_data(pdb_file, format='mmCIF')

# Select chain B
chain = atomic_structure.chains
chain_atoms = chain.atoms

# Select residues with id 184
residues = chain.residues
trp184_residues = residues[residues.ids() == 184]

# Select all dimers containing Trp184
for r1 in trp184_residues:
    r1_atoms = r1.atoms
    for r2 in trp184_residues:
        r2_atoms = r2.atoms
        if r1 == r2:
            continue
        inter = r1_atoms.intersect(r2_atoms)
        if len(inter) >= 5:
            fname = out_dir + '/' + root_name + '-' + str(count) + '.pdb'
            inter.write_pdb(fname)
            count += 1

# Close session
#session.delete()    

