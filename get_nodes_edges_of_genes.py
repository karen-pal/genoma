import json
import pandas as pd
from tqdm import tqdm
from intervaltree import IntervalTree

# Load your gene data
saved = pd.read_pickle('gene_data.pkl')

# Function to check if two genes overlap (redundant with intervaltree, but kept for clarity)
def check_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

# Initialize nodes and edges lists
nodes = []
edges = []

# Add progress bar for node generation
print("Generating nodes...")
for i, gene1 in tqdm(saved.iterrows(), total=len(saved)):
    node1 = {
        'id': gene1['gene_id'],
        'label': f"{gene1['gene_name']} ({gene1['gene_id']})",  # Custom label combining gene name and ID
        'data': {
            'desc': gene1['desc']   # Additional data for tooltips or labels
        }
    }
    nodes.append(node1)

# Create an interval tree
interval_tree = IntervalTree()

# Populate the interval tree with genes
print("Building interval tree...")
for i, gene in tqdm(saved.iterrows(), total=len(saved)):
    interval_tree[gene['start']:gene['end']] = gene['gene_id']

# Generate edges using the interval tree
print("Generating edges...")
for i, gene1 in tqdm(saved.iterrows(), total=len(saved)):
    overlaps = interval_tree[gene1['start']:gene1['end']]
    for overlap in overlaps:
        gene2_id = overlap.data
        if gene1['gene_id'] != gene2_id:
            edge = {
                'id': f'{gene1["gene_id"]}-{gene2_id}',
                'source': gene1['gene_id'],
                'target': gene2_id,
                'type': 'smoothstep',  # Customize edge type as needed
                'animated': True  # Add animation for visualization
            }
            edges.append(edge)

# Save nodes to JSON file
with open('nodes_data.json', 'w') as nodes_file:
    json.dump(nodes, nodes_file, indent=4)

# Save edges to JSON file
with open('edges_data.json', 'w') as edges_file:
    json.dump(edges, edges_file, indent=4)

