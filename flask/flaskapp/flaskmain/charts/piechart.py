from math import pi
import pandas as pd
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource


appen1 = []
appen2 = []

df = pd.read_csv("testfile.csv", encoding="latin-1", low_memory=False ).fillna("Empty")
dfx = df.head(10000)
cols = dfx.columns

# data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
colmn = input('Enter Column Name: ')
grp = dfx[colmn]
data = dfx.groupby(grp).size().reset_index(name="value").rename(columns={colmn: 'field'})
fields_grp = data['field']
for val in fields_grp:
    appen1.append(val)
graph_grp = data['value']
for val1 in graph_grp:
    appen2.append(val1)

cat = appen1
value = appen2

x = len(appen1)

data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[x]

source = ColumnDataSource(data=dict(fields=cat, value=value))
tooltips = [("Field", "@field"), ("Count", "@value")]


p = figure(plot_height=600, plot_width=700, title="Pie Chart",
        tools="pan,wheel_zoom,box_zoom,hover,reset,save", tooltips=tooltips)

p.toolbar.logo = None
p.title.text = 'Sample_Title'
p.title.text_color = '#0fb6db'
p.title.text_font = 'calibri'
p.title.text_font_size = '20pt'
p.title.text_font_style = 'bold'

p.yaxis.minor_tick_line_color = 'yellow'

p.xaxis.axis_label = colmn
p.yaxis.axis_label = 'value'

p.xaxis.major_label_text_color = "black"
p.xaxis.major_label_orientation = 45

p.xgrid.grid_line_color = None

p.wedge(x=0, y=1, radius=0.5,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='field', source=data)

p.legend.title = colmn

output_file("bar_distribution.html", mode='inline')
show(p)


