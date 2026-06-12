from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D

# Single SMILES string
smiles = "C[N+](C)(C)[O-]"  # TMAO

# Convert to RDKit molecule
mol = Chem.MolFromSmiles(smiles)
Chem.rdDepictor.Compute2DCoords(mol)  # Generate 2D coordinates

# Create drawer
drawer = rdMolDraw2D.MolDraw2DSVG(300, 300)

# Set transparent background
drawer.drawOptions().clearBackground = False 

drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Save as SVG file
with open("tmao.svg", "w") as f:
    f.write(drawer.GetDrawingText())

# Single SMILES string
smiles = "CCCCCCCCCCCCCCCC(O)=O"  # Palmitate

# Convert to RDKit molecule
mol = Chem.MolFromSmiles(smiles)
Chem.rdDepictor.Compute2DCoords(mol)  # Generate 2D coordinates

# Create drawer
drawer = rdMolDraw2D.MolDraw2DSVG(300, 300)

# Set transparent background
drawer.drawOptions().clearBackground = False 

drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Save as SVG file
with open("palmitate.svg", "w") as f:
    f.write(drawer.GetDrawingText())

# Single SMILES string
smiles = "OC(=O)CC1=CNC2=CC=CC=C12"  # IAA

# Convert to RDKit molecule
mol = Chem.MolFromSmiles(smiles)
Chem.rdDepictor.Compute2DCoords(mol)  # Generate 2D coordinates

# Create drawer
drawer = rdMolDraw2D.MolDraw2DSVG(300, 300)

# Set transparent background
drawer.drawOptions().clearBackground = False 

drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Save as SVG file
with open("iaa.svg", "w") as f:
    f.write(drawer.GetDrawingText())

# Single SMILES string
smiles = "C[C@H](CCC(=O)NCC(=O)O)[C@H]1CC[C@@H]2[C@@]1([C@H](C[C@H]3[C@H]2CC[C@H]4[C@@]3(CC[C@H](C4)O)C)O)C"
# GDCA - SMILES with full stereochemistry specifications
# From https://pubchem.ncbi.nlm.nih.gov/compound/Glycodeoxycholic-Acid rather than HMDB

# Convert to RDKit molecule
mol = Chem.MolFromSmiles(smiles)
Chem.rdDepictor.Compute2DCoords(mol)  # Generate 2D coordinates

# Create drawer
drawer = rdMolDraw2D.MolDraw2DSVG(300, 300)

# Set transparent background
drawer.drawOptions().clearBackground = False 

drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Save as SVG file
with open("gdca.svg", "w") as f:
    f.write(drawer.GetDrawingText())
