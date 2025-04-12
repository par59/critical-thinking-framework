import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes with different types
nodes = {
    'Users': 'user',
    'Firewall': 'security',
    'Authentication': 'security',
    'Monitoring': 'monitor',
    'Web Services': 'service',
    'Database': 'data'
}

# Add nodes to the graph
for node, node_type in nodes.items():
    G.add_node(node, type=node_type)

# Add edges with labels
edges = [
    ('Users', 'Firewall', '1. Request'),
    ('Firewall', 'Authentication', '2. Filter'),
    ('Authentication', 'Web Services', '3. Verify'),
    ('Web Services', 'Database', '4. Query'),
    ('Monitoring', 'Firewall', 'Monitor'),
    ('Monitoring', 'Authentication', 'Monitor'),
    ('Monitoring', 'Web Services', 'Monitor'),
    ('Monitoring', 'Database', 'Monitor'),
    ('Monitoring', 'Users', 'Alert')
]

G.add_edges_from([(u, v) for u, v, _ in edges])

# Create the plot
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=1, iterations=50)

# Draw nodes with different colors based on type
colors = {
    'user': '#3498db',      # Blue
    'security': '#e74c3c',  # Red
    'monitor': '#2ecc71',   # Green
    'service': '#f39c12',   # Orange
    'data': '#9b59b6'       # Purple
}

for node_type in set(nx.get_node_attributes(G, 'type').values()):
    nodelist = [node for node, attr in G.nodes(data=True) if attr['type'] == node_type]
    nx.draw_networkx_nodes(G, pos, nodelist=nodelist, node_color=colors[node_type],
                          node_size=2000, alpha=0.7)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)

# Add labels
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
edge_labels = {(u, v): d for u, v, d in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)

# Add title and legend
plt.title('Cybersecurity Process Flow', fontsize=16, pad=20)

# Add legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                            markerfacecolor=color, markersize=10, label=node_type.title())
                  for node_type, color in colors.items()]
plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

# Adjust layout and save
plt.tight_layout()
plt.axis('off')
plt.savefig('cyber_security_flow.png', dpi=300, bbox_inches='tight')
plt.close()

print("Cyber Security Flow Chart generated successfully!") 