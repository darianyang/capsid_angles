from chimerax.core.commands import run

# Select chains containing residues 144-231
run("select #1:144-231.a or #1:144-231.b")

# Find pairs of chains that are in close proximity
run("measure contacts #1:144-231.a #1:144-231.b distance 6.0")

