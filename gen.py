import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from intervaltree import IntervalTree
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import time
from pythonosc import udp_client
# Define the IP address and port of the OSC server
ip = "192.168.0.101"  # The IP address of the OSC server
ip_val = "192.168.1.100"  # The IP address of the OSC server
port = 9999       # The port on which the OSC server is listening

address_opacity = "/composition/layers/1/video/opacity" #/test/address"
address_color_r = "/composition/layers/1/video/effects/colorize/effect/color/red" #/test/address"
address_color_g = "/composition/layers/1/video/effects/colorize/effect/color/green" #/test/address"
address_color_b = "/composition/layers/1/video/effects/colorize/effect/color/blue" #/test/address"

address_distortion ="/composition/layers/1/video/effects/distortion/effect/distort" #/test/address"

address_distortion_radius ="/composition/layers/1/video/effects/distortion/effect/radius" #/test/address"
 
address_data_random_ = "/data"
# Create an OSC client
client_data = udp_client.SimpleUDPClient(ip_val, port)
client_projection = udp_client.SimpleUDPClient(ip, port)
print("created UDP client for OSC messaging")

"""
# example Send an OSC message
value = 123

client.send_message(address, value)
print(f"Sent OSC message to {address} with value {value}")
"""

# Load your gene data
saved = pd.read_pickle('gene_data.pkl')

# Function to check if two genes overlap
def check_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

# Take the first 100 genes for visualization
saved_subset = saved.head(1000)

# Create an interval tree
interval_tree = IntervalTree()

# Create a graph using networkx
G = nx.Graph()

black = (.1, .1, .1)

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
                dist = str(gene1["end"])[-1:]
                dist2 = str(gene1["end"])[-2:-1]
                client_projection.send_message(address_distortion, float(dist)*.01)
                client_projection.send_message(address_distortion_radius, float(dist2)*.01)
                if edge not in G.edges():
                    G.add_edge(*edge)

        # Clear previous plot elements
        ax.clear()
        ax.patch.set_facecolor(black)

        # Draw updated graph
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        red = (.9, .1, .2)
        blue = (.1, .4, .9)
        colors = [red, blue]
        
        # Draw nodes with red color
        node_collection = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=500, node_color=[colors[i % 2] for i in range(len(G))])

        # Draw edges with white color
        edge_collection = nx.draw_networkx_edges(G, pos, ax=ax, edgelist=G.edges(), edge_color=(.9, .8, .7), arrows=True)

        # Draw labels with white color
        label_collection = nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=5, font_color='white')

        # Set plot title
        ax.set_title(f"Genoma (Intervalo {frame+1}/{len(saved_subset)}) {interval}")

        # Update description window text
        desc_window.update_text(gene1['desc'])
        value = str(gene1["end"])[-1:]
        value_random = int(str(gene1["end"])[-3:])
        if value_random > 100:
            value_random = str(value_random)[-2:]
        client_projection.send_message(address_opacity, float(value)*.1)
        client_data.send_message("/data", int(value_random))
        client_projection.send_message(address_color_r, float(str(gene1["end"])[-2:-1]))
        client_projection.send_message(address_color_g, float(str(gene1["end"])[-3:-2]))
        client_projection.send_message(address_color_b, float(str(gene1["end"])[-4:-3]))
        print(f"Sent OSC message to address with value {value_random}")
        value_random = int(value_random)
        if value_random <10:
            to_sleep=10
        elif value_random < 25:
            to_sleep=19000
        elif value_random < 50:
            to_sleep=22000
        elif value_random < 75:
            to_sleep=15000
        elif value_random<85:
            to_sleep=17000
        elif value_random<92:
            to_sleep=5000
        else:
            to_sleep=4000
        print("about to sleep > ", to_sleep)
        time.sleep(to_sleep)

    return node_collection, edge_collection, label_collection

# PyQt5 Description Window
class DescriptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Descripcion del gen')
        self.setGeometry(100, 100, 400, 200)
        # Convert RGB tuple to hex format for stylesheet
        hex_color = f"#{int(black[0]*255):02x}{int(black[1]*255):02x}{int(black[2]*255):02x}"
        
        # Set background color using stylesheet
        self.setStyleSheet(f"background-color: {hex_color};") 
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { color : white; }")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def update_text(self, text):
        self.label.setText(text)

# Create description window instance
desc_window = DescriptionWindow()
desc_window.show()

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
    
    # Resume the animation
    anim.event_source.start()

# Connect key press event to figure
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Create animation
anim = FuncAnimation(fig, update, frames=len(saved_subset), interval=interval, blit=False)

fig.canvas.setWindowTitle('Genoma')

# Show plot
plt.show()

