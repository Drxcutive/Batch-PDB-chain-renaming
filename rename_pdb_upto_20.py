#@title 🔁 Rename Chain ID in Multiple PDB Files
from google.colab import files
import os

# Upload up to 20 files
print("📁 Upload up to 20 PDB files:")
uploaded_files = files.upload()
assert len(uploaded_files) <= 20, "Please upload no more than 20 PDB files."

#@markdown ### Input Parameters
to_chain = "A"  #@param {type:"string"}
from_chain = ""  #@param {type:"string"}
from_line = ""  #@param {type:"string"}
to_line = ""  #@param {type:"string"}

# Convert string to int if valid
from_line = int(from_line) if from_line.strip().isdigit() else None
to_line = int(to_line) if to_line.strip().isdigit() else None

# Validate chains
assert len(to_chain) == 1, "Target chain ID must be one character."
if from_chain:
    assert len(from_chain) == 1, "From chain ID must be one character."

def rename_chain_in_pdb(content, to_chain, from_chain=None, from_line=None, to_line=None):
    modified = []
    for i, line in enumerate(content.splitlines(), start=1):
        if line.startswith(('ATOM', 'HETATM', 'TER')) and len(line) >= 22:
            current_chain = line[21]
            change = False

            if from_line and to_line:
                if from_line <= i <= to_line:
                    change = True
            elif from_chain:
                if current_chain == from_chain:
                    change = True
            else:
                change = True

            if change:
                line = line[:21] + to_chain + line[22:]
        modified.append(line)
    return "\n".join(modified) + "\n"

# Process each uploaded file
for filename, file_data in uploaded_files.items():
    pdb_text = file_data.decode("utf-8")
    new_pdb = rename_chain_in_pdb(pdb_text, to_chain, from_chain, from_line, to_line)
    
    output_filename = f"renamed_{filename}"
    with open(output_filename, 'w') as out_f:
        out_f.write(new_pdb)
    
    # Automatically download the modified file
    files.download(output_filename)

print("✅ All files processed and downloads initiated.")
