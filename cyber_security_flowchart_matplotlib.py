import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(15, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Define colors
colors = {
    'main': '#3498db',
    'prevention': '#2ecc71',
    'detection': '#e74c3c',
    'response': '#f39c12',
    'recovery': '#9b59b6'
}

# Function to draw rounded rectangle
def rounded_rect(x, y, width, height, color, text, ax):
    rect = patches.FancyBboxPatch((x, y), width, height,
                                 boxstyle=patches.BoxStyle("Round", pad=0.2),
                                 facecolor=color, edgecolor='black', alpha=0.7)
    ax.add_patch(rect)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center', fontsize=8)

# Main process nodes
main_nodes = [
    (1, 8, 1.5, 0.6, 'Start', colors['main']),
    (1, 7, 1.5, 0.6, 'Risk Assessment', colors['main']),
    (1, 6, 1.5, 0.6, 'Prevention', colors['main']),
    (1, 5, 1.5, 0.6, 'Detection', colors['main']),
    (1, 4, 1.5, 0.6, 'Response', colors['main']),
    (1, 3, 1.5, 0.6, 'Recovery', colors['main']),
    (1, 2, 1.5, 0.6, 'End', colors['main'])
]

# Prevention sub-nodes
prevention_nodes = [
    (3, 6.5, 1.5, 0.6, 'Access Control', colors['prevention']),
    (3, 6, 1.5, 0.6, 'Encryption', colors['prevention']),
    (3, 5.5, 1.5, 0.6, 'Firewall', colors['prevention']),
    (3, 5, 1.5, 0.6, 'Training', colors['prevention'])
]

# Detection sub-nodes
detection_nodes = [
    (3, 5.5, 1.5, 0.6, 'Monitoring', colors['detection']),
    (3, 5, 1.5, 0.6, 'IDS', colors['detection']),
    (3, 4.5, 1.5, 0.6, 'Log Analysis', colors['detection'])
]

# Response sub-nodes
response_nodes = [
    (3, 4.5, 1.5, 0.6, 'Containment', colors['response']),
    (3, 4, 1.5, 0.6, 'Investigation', colors['response']),
    (3, 3.5, 1.5, 0.6, 'Notification', colors['response'])
]

# Recovery sub-nodes
recovery_nodes = [
    (3, 3.5, 1.5, 0.6, 'Restore', colors['recovery']),
    (3, 3, 1.5, 0.6, 'Review', colors['recovery']),
    (3, 2.5, 1.5, 0.6, 'Update', colors['recovery'])
]

# Draw all nodes
for x, y, w, h, text, color in main_nodes:
    rounded_rect(x, y, w, h, color, text, ax)

for x, y, w, h, text, color in prevention_nodes:
    rounded_rect(x, y, w, h, color, text, ax)

for x, y, w, h, text, color in detection_nodes:
    rounded_rect(x, y, w, h, color, text, ax)

for x, y, w, h, text, color in response_nodes:
    rounded_rect(x, y, w, h, color, text, ax)

for x, y, w, h, text, color in recovery_nodes:
    rounded_rect(x, y, w, h, color, text, ax)

# Draw connections
def draw_arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color='black'))

# Main flow
for i in range(len(main_nodes)-1):
    draw_arrow(main_nodes[i][0] + main_nodes[i][2], main_nodes[i][1] + main_nodes[i][3]/2,
              main_nodes[i+1][0], main_nodes[i+1][1] + main_nodes[i+1][3]/2)

# Prevention connections
for node in prevention_nodes:
    draw_arrow(main_nodes[2][0] + main_nodes[2][2], main_nodes[2][1] + main_nodes[2][3]/2,
              node[0], node[1] + node[3]/2)

# Detection connections
for node in detection_nodes:
    draw_arrow(main_nodes[3][0] + main_nodes[3][2], main_nodes[3][1] + main_nodes[3][3]/2,
              node[0], node[1] + node[3]/2)

# Response connections
for node in response_nodes:
    draw_arrow(main_nodes[4][0] + main_nodes[4][2], main_nodes[4][1] + main_nodes[4][3]/2,
              node[0], node[1] + node[3]/2)

# Recovery connections
for node in recovery_nodes:
    draw_arrow(main_nodes[5][0] + main_nodes[5][2], main_nodes[5][1] + main_nodes[5][3]/2,
              node[0], node[1] + node[3]/2)

# Feedback loops
draw_arrow(recovery_nodes[1][0] + recovery_nodes[1][2], recovery_nodes[1][1] + recovery_nodes[1][3]/2,
          main_nodes[1][0], main_nodes[1][1] + main_nodes[1][3]/2)
draw_arrow(recovery_nodes[2][0] + recovery_nodes[2][2], recovery_nodes[2][1] + recovery_nodes[2][3]/2,
          main_nodes[2][0], main_nodes[2][1] + main_nodes[2][3]/2)

# Add title
plt.title('Cyber Security Process Flow', fontsize=16, pad=20)

# Save the figure
plt.savefig('cyber_security_flowchart.png', dpi=300, bbox_inches='tight')
print("Cyber Security Flowchart generated successfully!") 