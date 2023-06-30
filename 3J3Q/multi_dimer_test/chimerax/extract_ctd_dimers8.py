# Import the chimeraX package
import chimerax

# Get the current session
session = chimerax.getCurrentSession()

# Select the chains
session.selection.clear()
session.selection.add(" #1:144-231.a or #1:144-231.b ")

# Print the chains
chains = session.selection.chains
print(chains)

