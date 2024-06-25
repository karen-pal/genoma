import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from intervaltree import IntervalTree
from matplotlib.animation import FuncAnimation

# Load your gene data
saved = pd.read_pickle('gene_data.pkl')

# Function to check if two genes overlap
def check_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

# Initialize nodes and edges lists
nodes = []
edges = []

# Take the first 100 genes for visualization
saved_subset = saved.head(100)

# Create an interval tree
interval_tree = IntervalTree()

# Create a graph using networkx
G = nx.Graph()

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 12))

# Initialize empty plot elements
node_collection = None
edge_collection = None
label_collection = None

# Function to update graph at each animation frame
def update(frame):
    global nodes, edges, interval_tree, G, node_collection, edge_collection, label_collection
    
    if frame < len(saved_subset):
        gene1 = saved_subset.iloc[frame]

        # Add node
        G.add_node(gene1['gene_id'], label=f"{gene1['gene_name']} ({gene1['gene_id']})")

        # Add node to interval tree
        interval_tree[gene1['start']:gene1['end']] = gene1['gene_id']

        # Generate edges using the interval tree
        for gene2_id in interval_tree[gene1['start']:gene1['end']]:
            if gene1['gene_id'] != gene2_id:
                edge = (gene1['gene_id'], gene2_id)
                if edge not in G.edges():
                    G.add_edge(*edge)

    # Clear previous plot elements
    ax.clear()

    # Draw updated graph
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    node_collection = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=500, node_color='skyblue')
    edge_collection = nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), arrows=True)
    label_collection = nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=10)

    # Set plot title
    ax.set_title(f"Dynamic Interval Tree Visualization (Frame {frame+1}/{len(saved_subset)})")

    return node_collection, edge_collection, label_collection

# Create animation
anim = FuncAnimation(fig, update, frames=len(saved_subset), interval=100, blit=False)

# Show plot
plt.show()

