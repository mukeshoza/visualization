def barchart(graphtype, metrices, title, catg, colmns, value, selectvalue, savefile, filenamesave):

	title = title
	catg = catg
	colmns = colmns
	value = value
	selectvalue = selectvalue
	filename = filenamesave
	                      

	htmltop = '''<!DOCTYPE html>
		<html lang="en">
		<head>
	  	<meta charset="utf-8">
	  	<meta name="viewport" content="width=device-width, initial-scale=1">
	  	<meta http-equiv="x-ua-compatible" content="ie=edge">
	  	<title>DatasPoint | Data Visualization | Parsing | Entry</title>

	  <script src="https://code.highcharts.com/highcharts.js"></script>
	  <script src="https://code.highcharts.com/modules/exporting.js"></script>
	  <script src="https://code.highcharts.com/modules/export-data.js"></script>
	  <script src="https://code.highcharts.com/modules/accessibility.js"></script>
	  </head>
	  '''

	barcharcontainer = '''<figure class="highcharts-figure">
		                		<div id="container"></div>'''

	if graphtype == 'Bar Graph' and metrices == 'Count':
		insights = '''<center><h4><b>What graph is saying?</b></h4>
		<p class="highcharts-description">The bar graph shows many things. <font class="text-success">
		<b>This is a test text.</b></font></p></center></figure>'''

	scriptdown = '''<script>
		    Highcharts.chart('container', {
		      chart: {
		          type: 'column'
		      },
		      title: {text:'''
	text = "'{} - {}'".format(title, selectvalue)
	script1 = '''},
		      subtitle: {
		          text: 'Bar Graph Distribution'
		      },
		      xAxis: {categories: '''
	catgeory = "{},".format(catg)
		          
	script2 = '''title: {
		              text: null
		          }
		      },
		      yAxis: {
		          min: 0,
		          title: {
		              text: '',
		              align: 'high'
		          },
		          labels: {
		              overflow: 'justify'
		          }
		      },
		      tooltip: {
		          valueSuffix: ''
		      },
		       plotOptions: {
		        series: {
		            colorByPoint: true
		        },

		        column: {
		          dataLabels: {
		              enabled: true
		          }
		       }
		      },
			  legend: {
	          layout: 'vertical',
	          align: 'right',
	          verticalAlign: 'top',
	          x: -20,
	          y: 42,
	          floating: true,
	          borderWidth: 1,
	          backgroundColor:
	              Highcharts.defaultOptions.legend.backgroundColor || '#FFFFFF',
	          shadow: true
			      },
			      credits: {
			          enabled: false
			      },
			      series: [{name: '''
	name = "'{}',".format(colmns)
	data = "data: {}".format(value)
	script3 = '''}]
			  });
			  </script>
			  </html>
			  '''

	if filename:
		barfileall = htmltop + barcharcontainer + insights + scriptdown + text + script1 + catgeory +script2 + name + data + script3
		with open(savefile, 'w+') as barfile:
			barfile.write(barfileall)


def piechart(gtitle, selectvalue, gcolumn, comval, filenamesave, savefile):

	toppart = '''<!DOCTYPE html>
		<html lang="en">
		<head>
	  	<meta charset="utf-8">
	  	<meta name="viewport" content="width=device-width, initial-scale=1">
	  	<meta http-equiv="x-ua-compatible" content="ie=edge">
	  	<title>DatasPoint | Data Visualization | Parsing | Entry</title>

	  <script src="https://code.highcharts.com/highcharts.js"></script>
	  <script src="https://code.highcharts.com/modules/exporting.js"></script>
	  <script src="https://code.highcharts.com/modules/export-data.js"></script>
	  <script src="https://code.highcharts.com/modules/accessibility.js"></script>
	  </head>
	  '''

	piechartcontainer = '''<figure class="highcharts-figure">
		                		<div id="container"></div>'''

	piec = '''<script type="text/javascript">
      Highcharts.chart('container', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {'''
	piec1 = '''text: "{} - {}"'''.format(gtitle, selectvalue)
	piec2 = '''},
         subtitle: {
         text: "Pie Chart Distribution"'''
	piec3 = '''},
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },
        credits: {
          enabled: false
        },
        
     series: [{
            name: '''

	name = "'{}',".format(gcolumn)
	data = "colorByPoint: true, data: [{}]".format(comval)
	final = '''}]
    });
  </script></html>

  '''

	if filenamesave:
		pieileall = (toppart+piechartcontainer+piec+piec1+piec2+piec3+name+data+final)
		with open(savefile, 'w+') as piefile:
			piefile.write(pieileall)


def lineplot(gtitle, selectvalue, refields, gmetrics, gcolumn, graph, colorpicker, filenamesave, locationline_path):

	toppart = '''<!DOCTYPE html>
		<html lang="en">
		<head>
	  	<meta charset="utf-8">
	  	<meta name="viewport" content="width=device-width, initial-scale=1">
	  	<meta http-equiv="x-ua-compatible" content="ie=edge">
	  	<title>DatasPoint | Data Visualization | Parsing | Entry</title>

	  	<script src="https://code.highcharts.com/highcharts.js"></script>
	  	<script src="https://code.highcharts.com/modules/exporting.js"></script>
	  	<script src="https://code.highcharts.com/modules/export-data.js"></script>
	  	<script src="https://code.highcharts.com/modules/accessibility.js"></script>
	  	</head>
	  '''

	linechartcontainer = '''<figure class="highcharts-figure">
		                		<div id="container"></div>'''

	lineplot = '''<script type="text/javascript">
		  Highcharts.chart('container', {
		    chart: {
		        type: 'line'
		    },
		    title: {'''
	title = '''text: "{} - {}"'''.format(gtitle, selectvalue)
	line1 = '''},
		    subtitle: {
		        text: 'Line Plot'
		    },
		    xAxis: {'''
	catg = 'categories: {}'.format(refields)
	line2 = '''},
		    yAxis: {
		        title: {'''
	line3 = 'text: "{} - Value"'.format(gmetrics)
	line4 = '''}
		    },
		    plotOptions: {
		        line: {
		            dataLabels: {
		                enabled: false
		            },
		            enableMouseTracking: true
		        }
		    },

		    credits: {
		          enabled: false
		        },
		    series: [{'''
	name = '''name: '{}','''.format(gcolumn)
	data = '''data: {},'''.format(graph)
	color = '''color: '{}','''.format(colorpicker)
	marker = '''marker: {'''
	linecolor = '''lineColor: "{}",'''.format(colorpicker)
	line5 = '''lineWidth: 4,
		            radius: 3
		        }
		    }]
		});
		</script>
		</html>
	'''
	
	if filenamesave:
		lineall = (toppart+linechartcontainer+lineplot+title+line1+catg+line2+line3+line4+name+data+color+marker+linecolor+line5)
		with open(locationline_path, 'w+') as linefile:
			linefile.write(lineall)


def areaplot(gtitle, selectvalue, refields, gmetrics, gcolumn, graph, colorpicker, filenamesave, locationarea_path):

	toppart = '''<!DOCTYPE html>
		<html lang="en">
		<head>
	  	<meta charset="utf-8">
	  	<meta name="viewport" content="width=device-width, initial-scale=1">
	  	<meta http-equiv="x-ua-compatible" content="ie=edge">
	  	<title>DatasPoint | Data Visualization | Parsing | Entry</title>

	  	<script src="https://code.highcharts.com/highcharts.js"></script>
	  	<script src="https://code.highcharts.com/modules/exporting.js"></script>
	  	<script src="https://code.highcharts.com/modules/export-data.js"></script>
	  	<script src="https://code.highcharts.com/modules/accessibility.js"></script>
	  	</head>
	  '''

	areachartcontainer = '''<figure class="highcharts-figure">
		                		<div id="container"></div>'''

	areaplot = '''<script type="text/javascript">
		  Highcharts.chart('container', {
		    chart: {
		        type: 'area'
		    },
		    title: {'''
	title = '''text: "{} - {}"'''.format(gtitle, selectvalue)
	line1 = '''},
		    subtitle: {
		        text: 'Area Plot'
		    },
		    xAxis: {'''
	catg = 'categories: {}'.format(refields)
	line2 = '''},
		    yAxis: {
		        title: {'''
	line3 = 'text: "{} - Value"'.format(gmetrics)
	line4 = '''}
		    },
		    plotOptions: {
		        line: {
		            dataLabels: {
		                enabled: false
		            },
		            enableMouseTracking: true
		        }
		    },

		    credits: {
		          enabled: false
		        },
		    series: [{'''
	name = '''name: '{}','''.format(gcolumn)
	data = '''data: {},'''.format(graph)
	color = '''color: '{}','''.format(colorpicker)
	marker = '''fillOpacity: 0.2, marker: {'''
	linecolor = '''lineColor: "{}",'''.format(colorpicker)
	line5 = '''lineWidth: 4,
		            radius: 3
		        }
		    }]
		});
		</script>
		</html>
	'''
	
	if filenamesave:
		lineall = (toppart+areachartcontainer+areaplot+title+line1+catg+line2+line3+line4+name+data+color+marker+linecolor+line5)
		with open(locationarea_path, 'w+') as linefile:
			linefile.write(lineall)

def bubblechart(gtitle, selectvalue, gcolumn, colorpicker, reappendvalbubble, filenamesave, locationbubble_path):

	toppart = '''<!DOCTYPE html>
		<html lang="en">
		<head>
	  	<meta charset="utf-8">
	  	<meta name="viewport" content="width=device-width, initial-scale=1">
	  	<meta http-equiv="x-ua-compatible" content="ie=edge">
	  	<title>DatasPoint | Data Visualization | Parsing | Entry</title>

	  	<script src="https://code.highcharts.com/highcharts.js"></script>
	  	<script src="https://code.highcharts.com/modules/exporting.js"></script>
	  	<script src="https://code.highcharts.com/modules/export-data.js"></script>
	  	<script src="https://code.highcharts.com/modules/accessibility.js"></script>
	  	<script src="https://code.highcharts.com/highcharts-more.js"></script>
	  	</head>
	  '''

	bubblechartcontainer = '''<figure class="highcharts-figure">
		                		<div id="container"></div>'''
	bubble = '''
		    <script type="text/javascript">
		  Highcharts.chart('container', {
		    chart: {
		        type: 'packedbubble',
		    },
		    title: {'''
	title = '''text: "{} - {}"'''.format(gtitle, selectvalue)
	bubble1 = '''},
		    subTitle: {
					text: 'Bubble Chart'
		    },
		    tooltip: {
		        useHTML: true,
		        pointFormat: '<b>{point.name}:</b> {point.y}</sub>'
		    },
		    plotOptions: {
		        packedbubble: {
		            dataLabels: {
		                enabled: true,
		                format: '{point.name}',
		                style: {
		                    color: 'black',
		                    textOutline: 'none',
		                    fontWeight: 'normal'
		                }
		            },
		            minPointSize: 5
		        }
		    },
		      credits: {
		          enabled: false
		        },
		    series: [{'''
	name = '''name: "{}",'''.format(gcolumn)
	color = '''color: "{}",'''.format(colorpicker)
	data = '''data: [{}]'''.format(reappendvalbubble)
	bubble2 = '''}]

		});

		</script></html>
    '''
	if filenamesave:
		bubbleall = (toppart+bubblechartcontainer+bubble+title+bubble1+name+color+data+bubble2)
		with open(locationbubble_path, 'w+') as bubblefile:
			bubblefile.write(bubbleall)