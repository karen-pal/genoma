import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from intervaltree import IntervalTree
from matplotlib.animation import FuncAnimation
from threading import Timer


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

black=(.1,.1,.1)
# Initialize plot
# Initialize plot with black background and fullscreen size
fig, ax = plt.subplots(figsize=(15, 10))
fig.patch.set_facecolor(black)  # Set background color to black


# Initialize empty plot elements
node_collection = None
edge_collection = None
label_collection = None

# Initial interval value (in milliseconds)
interval = 1000
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
    ax.patch.set_facecolor(black)

    # Draw updated graph
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    red = (.9,.1,.2)
    blue = (.1,.4,.9)
    colors =[red,blue]
    # Draw nodes with red color
    node_collection = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=500, node_color=[colors[i % 2] for i in range(len(G))])


    # Draw edges with white color
    edge_collection = nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), edge_color=(.9,.8,.7), arrows=True)

    # Draw labels with white color
    label_collection = nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=5, font_color='white')


    desc_text.set_text(gene1['desc'])
    # Set plot title
    ax.set_title(f"Genoma (Intervalo {frame+1}/{len(saved_subset)}) {interval}")

    return node_collection, edge_collection, label_collection

# Function to handle key press events
def on_key_press(event):
    global anim, interval
    
    if event.key == 'left':
        # Decrease interval by 1000 ms
        interval += 100
    elif event.key == 'right':
        # Increase interval by 1000 ms
        interval -= 100
        
    # Ensure interval doesn't go below 100 ms
    interval = max(interval, 10)
    
    # Pause the animation
    anim.event_source.stop()

    # Update animation interval
    anim.event_source.interval = interval
    print(anim.event_source.interval)    
    # Resume the animation
    anim.event_source.start()

# Connect key press event to figure
fig.canvas.mpl_connect('key_press_event', on_key_press)

anim = FuncAnimation(fig, update, frames=len(saved_subset), interval=interval, blit=False)
# Create a separate text window for gene description
desc_fig, desc_ax = plt.subplots(figsize=(6, 3))
desc_fig.patch.set_facecolor(black)
desc_text = desc_ax.text(0.5, 0.5, "", color='white', ha='center', va='center', fontsize=12)
desc_ax.axis('off')

# Function to update description text
def update_desc_text(frame):
    if frame < len(saved_subset):
        gene1 = saved_subset.iloc[frame]
        desc_text.set_text(gene1['desc'])

# Timer to update description text every interval
def description_timer():
    for i in range(len(saved_subset)):
        Timer(interval / 1000 * i, update_desc_text, args=[i]).start()

# Start description timer
description_timer()
# Create animation

# Show plot
plt.show()

