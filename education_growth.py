from bokeh.io import show
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Div, Button
from bokeh.plotting import figure
import pandas as pd
import numpy as np

# Education data for different types of institutions (2006-07 to 2009-10)
education_data = {
    'Year': ['2006-07', '2007-08', '2008-09', '2009-10'],
    'Engineering Colleges': [1668, 1768, 1868, 1968],
    'Medical Colleges': [271, 288, 301, 314],
    'Arts & Science Colleges': [17625, 18025, 18425, 18825],
    'Polytechnics': [1224, 1324, 1424, 1524],
    'Technical Institutes': [1234, 1334, 1434, 1534]
}

# Create DataFrame
df = pd.DataFrame(education_data)

# Create ColumnDataSource
source = ColumnDataSource(df)

# Create figures for each type of institution
figures = []
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
titles = ['Engineering Colleges', 'Medical Colleges', 'Arts & Science Colleges', 'Polytechnics', 'Technical Institutes']

for i, (title, color) in enumerate(zip(titles, colors)):
    fig = figure(title=title, x_range=df['Year'], height=300, width=400,
                tools="hover", tooltips=[("Year", "@Year"), (title, f"@{title}")])
    fig.vbar(x='Year', top=title, width=0.9, source=source, color=color, alpha=0.8)
    fig.xaxis.major_label_orientation = np.pi/4
    figures.append(fig)

# Create line plot showing growth trends
line_fig = figure(title="Growth Trends of Educational Institutions (2006-07 to 2009-10)",
                 x_range=df['Year'], height=400, width=800,
                 tools="hover,pan,wheel_zoom,box_zoom,reset",
                 tooltips=[("Year", "@Year")])

for i, (title, color) in enumerate(zip(titles, colors)):
    line_fig.line(x='Year', y=title, source=source, line_width=2, color=color, legend_label=title)
    line_fig.circle(x='Year', y=title, source=source, size=8, color=color)

line_fig.legend.location = "top_left"
line_fig.legend.click_policy = "hide"

# Create download button
download_button = Button(label="Download Data", button_type="success")

# JavaScript code for downloading data
download_button.js_on_click(CustomJS(args=dict(df=df.to_csv(index=False)),
    code="""
    const blob = new Blob([df], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'education_growth_data.csv';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    """))

# Create info div
info_div = Div(text="""
    <h2>Growth of Educational Institutions in India (2006-07 to 2009-10)</h2>
    <p>This interactive dashboard shows the growth of different types of educational institutions in India:</p>
    <ul>
        <li>Engineering Colleges</li>
        <li>Medical Colleges</li>
        <li>Arts & Science Colleges</li>
        <li>Polytechnics</li>
        <li>Technical Institutes</li>
    </ul>
    <p>Hover over the bars and lines to see detailed numbers. Click on legend items to hide/show specific categories.</p>
    <p>Click the download button below to get the data in CSV format.</p>
""")

# Create grid layout for bar charts
bar_charts = gridplot([figures[:3], figures[3:]])

# Final layout
layout = column(info_div, row(line_fig), bar_charts, row(download_button))
show(layout) 