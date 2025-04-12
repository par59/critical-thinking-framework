import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Create PDF file
with PdfPages('cyber_security_flowchart_industry.pdf') as pdf:
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 15)
    ax.axis('off')

    # Define industry standard colors
    colors = {
        'start_end': '#2c3e50',      # Dark blue for start/end
        'process': '#27ae60',        # Green for processes
        'decision': '#e74c3c',       # Red for decisions
        'input': '#f39c12',          # Orange for input/output
        'feedback': '#3498db'        # Blue for feedback
    }

    # Function to draw standard flowchart shapes
    def draw_node(x, y, width, height, color, text, shape='rectangle', ax=None):
        if shape == 'start_end':
            # Rounded rectangle for start/end
            rect = patches.FancyBboxPatch((x, y), width, height,
                                        boxstyle=patches.BoxStyle("Round", pad=0.2),
                                        facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(rect)
        elif shape == 'process':
            # Rectangle for processes
            rect = patches.Rectangle((x, y), width, height,
                                   facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(rect)
        elif shape == 'decision':
            # Diamond for decisions
            diamond = patches.RegularPolygon((x + width/2, y + height/2), 4,
                                           radius=width/2,
                                           facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(diamond)
        elif shape == 'input':
            # Parallelogram for input/output
            vertices = np.array([
                [x, y],
                [x + width*0.2, y + height],
                [x + width, y + height],
                [x + width*0.8, y]
            ])
            path = Path(vertices)
            patch = patches.PathPatch(path, facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(patch)
        
        ax.text(x + width/2, y + height/2, text,
                ha='center', va='center',
                fontsize=10, fontweight='bold')

    # Main process nodes with standard shapes
    main_nodes = [
        (2, 12, 3, 1, 'Start', colors['start_end'], 'start_end'),
        (2, 10, 3, 1, 'Risk Assessment', colors['process'], 'process'),
        (2, 8, 3, 1, 'Security Controls', colors['process'], 'process'),
        (2, 6, 3, 1, 'Monitor & Detect', colors['process'], 'process'),
        (2, 4, 3, 1, 'Incident Response', colors['process'], 'process'),
        (2, 2, 3, 1, 'Recovery & Review', colors['process'], 'process'),
        (2, 0, 3, 1, 'End', colors['start_end'], 'start_end')
    ]

    # Risk Assessment sub-nodes
    risk_nodes = [
        (6, 10.5, 3, 0.8, 'Asset Inventory', colors['input'], 'input'),
        (6, 9.5, 3, 0.8, 'Threat Analysis', colors['process'], 'process'),
        (6, 8.5, 3, 0.8, 'Vulnerability Scan', colors['process'], 'process')
    ]

    # Security Controls sub-nodes
    control_nodes = [
        (6, 8.5, 3, 0.8, 'Access Management', colors['process'], 'process'),
        (6, 7.5, 3, 0.8, 'Data Protection', colors['process'], 'process'),
        (6, 6.5, 3, 0.8, 'Security Training', colors['process'], 'process')
    ]

    # Monitoring sub-nodes
    monitor_nodes = [
        (6, 6.5, 3, 0.8, 'SIEM Monitoring', colors['process'], 'process'),
        (6, 5.5, 3, 0.8, 'Log Analysis', colors['process'], 'process'),
        (6, 4.5, 3, 0.8, 'Alert Management', colors['process'], 'process')
    ]

    # Response sub-nodes
    response_nodes = [
        (6, 4.5, 3, 0.8, 'Incident Triage', colors['decision'], 'decision'),
        (6, 3.5, 3, 0.8, 'Containment', colors['process'], 'process'),
        (6, 2.5, 3, 0.8, 'Investigation', colors['process'], 'process')
    ]

    # Recovery sub-nodes
    recovery_nodes = [
        (6, 2.5, 3, 0.8, 'System Recovery', colors['process'], 'process'),
        (6, 1.5, 3, 0.8, 'Post-Incident Review', colors['process'], 'process'),
        (6, 0.5, 3, 0.8, 'Improvement Plan', colors['input'], 'input')
    ]

    # Draw all nodes
    for x, y, w, h, text, color, shape in main_nodes:
        draw_node(x, y, w, h, color, text, shape, ax)

    for x, y, w, h, text, color, shape in risk_nodes:
        draw_node(x, y, w, h, color, text, shape, ax)

    for x, y, w, h, text, color, shape in control_nodes:
        draw_node(x, y, w, h, color, text, shape, ax)

    for x, y, w, h, text, color, shape in monitor_nodes:
        draw_node(x, y, w, h, color, text, shape, ax)

    for x, y, w, h, text, color, shape in response_nodes:
        draw_node(x, y, w, h, color, text, shape, ax)

    for x, y, w, h, text, color, shape in recovery_nodes:
        draw_node(x, y, w, h, color, text, shape, ax)

    # Draw connections with proper arrows
    def draw_arrow(x1, y1, x2, y2, color='black', style='->', text=''):
        ax.annotate(text, xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, linewidth=2),
                    ha='center', va='center')

    # Main flow
    for i in range(len(main_nodes)-1):
        draw_arrow(main_nodes[i][0] + main_nodes[i][2],
                  main_nodes[i][1] + main_nodes[i][3]/2,
                  main_nodes[i+1][0],
                  main_nodes[i+1][1] + main_nodes[i+1][3]/2)

    # Sub-node connections
    def connect_sub_nodes(main_node, sub_nodes):
        for node in sub_nodes:
            draw_arrow(main_node[0] + main_node[2],
                      main_node[1] + main_node[3]/2,
                      node[0],
                      node[1] + node[3]/2)

    connect_sub_nodes(main_nodes[1], risk_nodes)
    connect_sub_nodes(main_nodes[2], control_nodes)
    connect_sub_nodes(main_nodes[3], monitor_nodes)
    connect_sub_nodes(main_nodes[4], response_nodes)
    connect_sub_nodes(main_nodes[5], recovery_nodes)

    # Feedback loops
    draw_arrow(recovery_nodes[1][0] + recovery_nodes[1][2],
              recovery_nodes[1][1] + recovery_nodes[1][3]/2,
              main_nodes[1][0],
              main_nodes[1][1] + main_nodes[1][3]/2,
              colors['feedback'], '->', 'Lessons Learned')

    # Add legend
    legend_elements = [
        patches.Patch(facecolor=colors['start_end'], label='Start/End'),
        patches.Patch(facecolor=colors['process'], label='Process'),
        patches.Patch(facecolor=colors['decision'], label='Decision'),
        patches.Patch(facecolor=colors['input'], label='Input/Output'),
        patches.Patch(facecolor=colors['feedback'], label='Feedback')
    ]
    ax.legend(handles=legend_elements, loc='upper right',
              bbox_to_anchor=(0.95, 0.95), fontsize=10)

    # Add title and subtitle
    plt.suptitle('Cybersecurity Management Process Flow', fontsize=24, fontweight='bold')
    plt.title('ISO 27001 & NIST CSF Compliant Implementation', fontsize=16, pad=20)

    # Add footer
    plt.figtext(0.5, 0.01,
                'Based on ISO 27001 and NIST Cybersecurity Framework\n'
                '© 2024 Cybersecurity Process Flow',
                ha='center', fontsize=10)

    # Adjust layout and save to PDF
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print("Industry Standard Cyber Security Flowchart generated successfully in PDF format!") 