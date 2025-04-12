import graphviz

# Create a new directed graph
dot = graphviz.Digraph('CyberSecurityFlowchart', comment='Cyber Security Process Flow')
dot.attr(rankdir='TB', size='8,5')
dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
dot.attr('edge', color='gray50')

# Add nodes for the main security process
dot.node('Start', 'Start Security Process')
dot.node('RiskAssessment', 'Risk Assessment')
dot.node('Prevention', 'Prevention Measures')
dot.node('Detection', 'Threat Detection')
dot.node('Response', 'Incident Response')
dot.node('Recovery', 'Recovery & Analysis')
dot.node('End', 'End Process')

# Add prevention sub-nodes
dot.node('AccessControl', 'Access Control')
dot.node('Encryption', 'Data Encryption')
dot.node('Firewall', 'Firewall Configuration')
dot.node('Training', 'Security Training')

# Add detection sub-nodes
dot.node('Monitoring', 'Continuous Monitoring')
dot.node('IDS', 'Intrusion Detection')
dot.node('LogAnalysis', 'Log Analysis')

# Add response sub-nodes
dot.node('Containment', 'Incident Containment')
dot.node('Investigation', 'Forensic Investigation')
dot.node('Notification', 'Stakeholder Notification')

# Add recovery sub-nodes
dot.node('Restore', 'System Restoration')
dot.node('Review', 'Security Review')
dot.node('Update', 'Policy Updates')

# Connect main process nodes
dot.edge('Start', 'RiskAssessment')
dot.edge('RiskAssessment', 'Prevention')
dot.edge('Prevention', 'Detection')
dot.edge('Detection', 'Response')
dot.edge('Response', 'Recovery')
dot.edge('Recovery', 'End')

# Connect prevention measures
dot.edge('Prevention', 'AccessControl')
dot.edge('Prevention', 'Encryption')
dot.edge('Prevention', 'Firewall')
dot.edge('Prevention', 'Training')

# Connect detection measures
dot.edge('Detection', 'Monitoring')
dot.edge('Detection', 'IDS')
dot.edge('Detection', 'LogAnalysis')

# Connect response measures
dot.edge('Response', 'Containment')
dot.edge('Response', 'Investigation')
dot.edge('Response', 'Notification')

# Connect recovery measures
dot.edge('Recovery', 'Restore')
dot.edge('Recovery', 'Review')
dot.edge('Recovery', 'Update')

# Add feedback loops
dot.edge('Review', 'RiskAssessment', 'Feedback Loop')
dot.edge('Update', 'Prevention', 'Policy Updates')

# Save and render the graph
dot.render('cyber_security_flowchart', format='png', cleanup=True)
print("Cyber Security Flowchart generated successfully!") 