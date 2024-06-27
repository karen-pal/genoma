import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from intervaltree import IntervalTree
from pythonosc import udp_client
from PIL import Image, ImageDraw, ImageFont
import time

# Define the IP address and port of the OSC server
ip = "192.168.1.102"  # The IP address of the OSC server
ip_val = "192.168.1.100"  # The IP address of the OSC server
port = 9999  # The port on which the OSC server is listening

address_opacity = "/composition/layers/1/video/opacity"
address_color_r = "/composition/layers/1/video/effects/colorize/effect/color/red"
address_color_g = "/composition/layers/1/video/effects/colorize/effect/color/green"
address_color_b = "/composition/layers/1/video/effects/colorize/effect/color/blue"
address_distortion = "/composition/layers/1/video/effects/distortion/effect/distort"
address_distortion_radius = "/composition/layers/1/video/effects/distortion/effect/radius"
address_data_random_ = "/data"

# Create an OSC client
client_data = udp_client.SimpleUDPClient(ip_val, port)
client_projection = udp_client.SimpleUDPClient(ip, port)
print("Created UDP client for OSC messaging")

# Load your gene data
saved = pd.read_pickle('gene_data.pkl')

# Function to check if two genes overlap
def check_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

# Take the first 1000 genes for visualization
saved_subset = saved.head(1000)

# Create an interval tree
interval_tree = IntervalTree()

# Create a graph using networkx
G = nx.Graph()

# Initialize variables for image generation
image_counter = 0
image_path = "gene_images/"

# Function to send OSC messages and handle sleep
def send_osc_and_sleep(gene1):
    dist = str(gene1["end"])[-1:]
    dist2 = str(gene1["end"])[-2:-1]
    client_projection.send_message(address_distortion, float(dist) * .01)
    client_projection.send_message(address_distortion_radius, float(dist2) * .01)
    
    value = str(gene1["end"])[-1:]
    value_random = int(str(gene1["end"])[-3:])
    if value_random > 100:
        value_random = str(value_random)[-2:]
    #client_projection.send_message(address_opacity, float(value) * .1)
    client_data.send_message("/data", int(value_random))
    client_projection.send_message(address_color_r, float(str(gene1["end"])[-2:-1])*.1)
    print("r")
    print(float(str(gene1["end"])[-2:-1])*.1)
    client_projection.send_message(address_color_g, float(0.))
    client_projection.send_message(address_color_b, float(str(gene1["end"])[-4:-3])*.1)
    print("b")
    print(float(str(gene1["end"])[-4:-3])*.1)
    print(f"Sent OSC message to address with value {value_random}")
    value_random = int(value_random)
    if value_random < 10:
        to_sleep = 10
    elif value_random < 25:
        to_sleep = 19000
    elif value_random < 50:
        to_sleep = 22000
    elif value_random < 75:
        to_sleep = 15000
    elif value_random < 85:
        to_sleep = 17000
    elif value_random < 92:
        to_sleep = 5000
    else:
        to_sleep = 4000
    print("about to sleep >", to_sleep)
    time.sleep(to_sleep / 1000)  # Convert to seconds

# Function to create and update PNG image with description
def create_image_with_description(gene1):
    global image_counter, interval_tree, G

    # Add node to networkx graph
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
    plt.clf()
    plt.figure(figsize=(15, 10))

    # Draw updated graph
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    red = (.9, .1, .2)
    blue = (.1, .4, .9)
    colors = [red, blue]

    # Draw nodes with red color
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=[colors[i % 2] for i in range(len(G))])

    # Draw edges with white color
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=(.9, .8, .7), arrows=True)

    # Draw labels with white color
    nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=5, font_color='white')

    # Set plot title
    plt.title(f"Genoma (Intervalo {image_counter + 1}/{len(saved_subset)})")

    # Save image
    image_file = f"{image_path}gene_image.png"
    plt.savefig(image_file)

    # Create a new image with description using Pillow
    img = Image.open(image_file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Arial.ttf", 16)  # Example font and size, adjust as needed

    # Position and format the description text
    description = gene1['desc']
    text_bbox = draw.textbbox((0, 0), description, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_position = ((img.width - text_width) // 2, img.height - text_height - 20)
    text_color = (255, 255, 255)  # White color

    # Draw text on the image
    draw.text(text_position, description, font=font, fill=text_color)

    # Save the updated image
    img.save(image_file)

    # Send OSC messages and handle sleep
    send_osc_and_sleep(gene1)

    # Increment image counter
    image_counter += 1

    # Schedule next update
    if image_counter < len(saved_subset):
        create_image_with_description(saved_subset.iloc[image_counter])

# Main simulation loop
for index, gene1 in saved_subset.iterrows():
    # Check for overlaps
    overlaps = interval_tree[gene1['start']:gene1['end']]
    for overlap_gene_id in overlaps:
        overlap_gene = saved_subset[saved_subset['gene_id'] == overlap_gene_id]
        # Your overlap handling logic here

    # Update images with descriptions
    create_image_with_description(gene1)

