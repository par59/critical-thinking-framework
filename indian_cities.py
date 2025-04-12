from bokeh.io import show
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Div, LabelSet, Button
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
import math
import pandas as pd
import io
import base64

# Convert latitude and longitude to Web Mercator
def wgs84_to_web_mercator(lat, lon):
    k = 6378137
    x = lon * (k * math.pi / 180.0)
    y = math.log(math.tan((90 + lat) * math.pi / 360.0)) * k
    return x, y

# Top 10 most populated cities in India with multiple metrics
city_data = [
    # (City, Lat, Lon, Population(millions), Income(USD billions), GDP(USD billions), UNESCO Sites)
    ("Delhi", 28.7041, 77.1025, 32.9, 293, 370, 3),
    ("Mumbai", 19.0760, 72.8777, 20.9, 310, 400, 2),
    ("Bangalore", 12.9716, 77.5946, 13.6, 110, 150, 0),
    ("Hyderabad", 17.3850, 78.4867, 10.3, 75, 100, 1),
    ("Ahmedabad", 23.0225, 72.5714, 8.5, 68, 90, 1),
    ("Chennai", 13.0827, 80.2707, 7.2, 66, 85, 0),
    ("Kolkata", 22.5726, 88.3639, 5.1, 60, 75, 1),
    ("Surat", 21.1702, 72.8311, 4.9, 40, 50, 0),
    ("Pune", 18.5204, 73.8567, 4.7, 48, 60, 0),
    ("Jaipur", 26.9124, 75.7873, 4.0, 35, 45, 1)
]

# Sort by population
city_data.sort(key=lambda x: x[3], reverse=True)

names = [c[0] for c in city_data]
lats = [c[1] for c in city_data]
lons = [c[2] for c in city_data]
pops = [c[3] for c in city_data]
incomes = [c[4] for c in city_data]
gdps = [c[5] for c in city_data]
unesco_sites = [c[6] for c in city_data]

# Convert to Web Mercator
xs, ys = zip(*[wgs84_to_web_mercator(lat, lon) for lat, lon in zip(lats, lons)])

# Create data source
source = ColumnDataSource(data=dict(
    name=names,
    lat=lats,
    lon=lons,
    pop=pops,
    income=incomes,
    gdp=gdps,
    unesco=unesco_sites,
    x=xs,
    y=ys
))

# Create map
tile_provider = get_provider(Vendors.CARTODBPOSITRON)
map_fig = figure(title="Top 10 Indian Cities",
                 x_range=(6.5e6, 1.05e7), y_range=(500000, 4.5e6),
                 x_axis_type="mercator", y_axis_type="mercator", height=400, width=600,
                 tools="pan,wheel_zoom,box_zoom,reset,hover", 
                 tooltips=[("City", "@name"), ("Population", "@pop millions"), 
                          ("Income", "@income billion USD"), ("GDP", "@gdp billion USD"),
                          ("UNESCO Sites", "@unesco")])
map_fig.add_tile(tile_provider)
map_fig.circle(x='x', y='y', size=20, color='red', alpha=0.8, source=source)

# Add city labels
city_labels = LabelSet(x='x', y='y', text='name', y_offset=7, 
                      text_font_size="8pt", source=source, text_align='center')
map_fig.add_layout(city_labels)

# Create population bar chart
pop_fig = figure(title="Population (in millions)",
                x_range=names, height=300, width=600,
                tools="hover", tooltips=[("City", "@name"), ("Population", "@pop millions")])
pop_fig.vbar(x='name', top='pop', width=0.9, source=source, color='red', alpha=0.8)
pop_fig.xaxis.major_label_orientation = math.pi/4

# Create income bar chart
income_fig = figure(title="Income (in billion USD)",
                   x_range=names, height=300, width=600,
                   tools="hover", tooltips=[("City", "@name"), ("Income", "@income billion USD")])
income_fig.vbar(x='name', top='income', width=0.9, source=source, color='blue', alpha=0.8)
income_fig.xaxis.major_label_orientation = math.pi/4

# Create GDP bar chart
gdp_fig = figure(title="GDP (in billion USD)",
                x_range=names, height=300, width=600,
                tools="hover", tooltips=[("City", "@name"), ("GDP", "@gdp billion USD")])
gdp_fig.vbar(x='name', top='gdp', width=0.9, source=source, color='green', alpha=0.8)
gdp_fig.xaxis.major_label_orientation = math.pi/4

# Create UNESCO sites bar chart
unesco_fig = figure(title="Number of UNESCO World Heritage Sites",
                   x_range=names, height=300, width=600,
                   tools="hover", tooltips=[("City", "@name"), ("UNESCO Sites", "@unesco")])
unesco_fig.vbar(x='name', top='unesco', width=0.9, source=source, color='purple', alpha=0.8)
unesco_fig.xaxis.major_label_orientation = math.pi/4

# Create DataFrame for Excel export
df = pd.DataFrame({
    'City': names,
    'Latitude': lats,
    'Longitude': lons,
    'Population (millions)': pops,
    'Income (billion USD)': incomes,
    'GDP (billion USD)': gdps,
    'UNESCO Sites': unesco_sites
})

# Create download button
download_button = Button(label="Download Excel", button_type="success")

# JavaScript code for downloading Excel file
download_button.js_on_click(CustomJS(args=dict(df=df.to_csv(index=False)),
    code="""
    const blob = new Blob([df], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'indian_cities_data.csv';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    """))

# Create info div
info_div = Div(text="""
    <h2>Top 10 Indian Cities - Comprehensive Analysis</h2>
    <p>This interactive dashboard shows various metrics for the top 10 Indian cities:</p>
    <ul>
        <li>Population (in millions)</li>
        <li>Income (in billion USD)</li>
        <li>GDP (in billion USD)</li>
        <li>Number of UNESCO World Heritage Sites</li>
    </ul>
    <p>Hover over the points on the map or bars in the charts to see more details.</p>
    <p>Click the download button below to get the data in Excel format.</p>
""")

# Create grid layout for charts
charts = gridplot([[pop_fig, income_fig], [gdp_fig, unesco_fig]])

# Final layout
layout = column(info_div, row(map_fig), charts, row(download_button))
show(layout)