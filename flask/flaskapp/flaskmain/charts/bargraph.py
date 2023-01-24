from bokeh.plotting import figure, output_file, show, save
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource
import warnings
import pandas as pd
import os

warnings.simplefilter(action='ignore', category=FutureWarning)

appen1 = []
appen2 = []

def barchart(file):
filename = file
if filename.endswith('.csv'):
	df = pd.read_csv(filename, encoding='latin-1', low_memory=False).fillna("Empty")
	dflimit = df.head(10000)

	cols = dflimit.columns
	# for col in cols:
	# 	print(col)

	title = 'test'
	col1 = 'category'

	dfx = dflimit[col1]

	grp = dflimit.groupby(dfx).size().reset_index(name="count")

	fields_grp = grp[col1]
	for val in fields_grp:
		appen1.append(val)
	graph_grp = grp['count']
	for val1 in graph_grp:
		appen2.append(val1)

	fields = appen1
	graph = appen2

	lencat = len(grp[col1])
	color = Category20[lencat]

	source = ColumnDataSource(data=dict(fields=fields, graph=graph, color=color))

	tooltips=[("Field", "@fields"), ("Count", "@graph")]

	p = figure(x_range=fields, plot_width=1000, plot_height=650,tools='pan,wheel_zoom,box_zoom,reset,save', tooltips=tooltips)

	p.toolbar.logo = None
	p.title.text = title
	p.title.text_color = '#0fb6db'
	p.title.text_font = 'calibri'
	p.title.text_font_size = '20pt'
	p.title.text_font_style = 'bold'


	p.yaxis.minor_tick_line_color = 'yellow'

	p.xaxis.axis_label = col1
	p.yaxis.axis_label = 'count'


	p.vbar(x='fields', top='graph', width=0.8, color='color', legend='fields', source=source)

	# change just some things about the y-axes
	p.yaxis.major_label_text_color = "black"
	p.yaxis.major_label_orientation = "horizontal"

	p.xaxis.major_label_text_color = "black"
	p.xaxis.major_label_orientation = 45

	p.xgrid.grid_line_color = None
	p.legend.orientation = "vertical"
	p.legend.location = "top_right"
	p.legend.title = col1
	p.y_range.start = 0

	# p.circle([1,2.5,3,4.3,5,3,6], [5,8.3,7,5.5,6,4,6.4], size=[i*2 for i in [5, 8.5, 12, 15, 6.5, 5, 4]], color='#2de7ed', alpha=0.5)
	# p.line([1,2,3,4,5], [5,8,7,5,6], line_width=3, color='red', alpha=0.5)

	output_file("bar_distribution_test.html")
	save(p)