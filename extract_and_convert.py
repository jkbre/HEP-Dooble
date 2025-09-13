import re
import yaml

# Read the content of the LaTeX file
with open('symbol_guide_v1.tex', 'r') as f:
    content = f.read()

# Find all symbolcard entries
matches = re.findall(r'\\symbolcard\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}', content)

# Create a list of dictionaries
symbols = []
for match in matches:
    symbols.append({
        'image': match[0],
        'url': match[1],
        'title': match[2],
        'description': match[3]
    })

# Write the data to a YAML file
with open('symbols.yaml', 'w') as f:
    yaml.dump(symbols, f)
