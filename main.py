# Python modules
import os
import datetime
import fnmatch
import string
import random

# Mapping
from dash import Dash, html
import dash_cytoscape as cyto

class color:	
	def redistribute(r, g, b):
		#Sets max value
		threshold = 255.999
		
		#Gets max value, if so returns (r,g,b)
		m = max(r,g,b)
		if m <= threshold:
			return int(r),int(g),int(b)
		
		#If pure white, return 255,255,255
		total = r+g+b
		if total >= 3*threshold:
			return int(threshold),int(threshold),int(threshold)
		
		# Gets color ratios & redistributes max value down
		x = (3 * threshold - total) / (3 * m - total)
		gray = threshold - x * m
		return int(gray + x * r), int(gray + x * g), int(gray + x * b)
	
	# Lightens hex value by factor
	def lighten(hexa, factor):
		r = int(hexa[0:2],16)
		g = int(hexa[2:4],16)
		b = int(hexa[4:6],16)

		r = r * factor
		g = g * factor
		b = b * factor

		rgb = color.redistribute(r,g,b)

		hexa = '%02x%02x%02x' % rgb

		return hexa

testDataFile = "TestData-Simple.csv"
testColorFile = "TestColors-Simple.csv"

links = []
nodes = set()

# Reads CSV
with open(testDataFile) as csv:
    lines = csv.readlines()
    for line in lines[1:]:
        vals = line.replace('\n','').split(",")
        node1 = vals[0]
        node2 = vals[1]
        relType = vals[2]
        link = {'node1': node1, 'node2': node2, 'relType': relType}
        links.append(link)
        nodes.add(node1)
        nodes.add(node2)

colors = []

with open(testColorFile) as csv:
    lines = csv.readlines()
    for line in lines[1:]:
        vals = line.replace('\n','').split(",")
        normal = {'selector': '.'+vals[0], 'style': {'line-color': "#"+vals[1], 'width': 2}}
        selected = {'selector': '.'+vals[0]+':selected', 'style': {'width': 5}}
        colors.append(normal)
        colors.append(selected)

# Pulls from links & nodes, generates cytoscape elements
cytoscapeElements = []

for node in nodes:
    element = {'data' : {'id': node, 'label': node}}
    cytoscapeElements.append(element)

for link in links:
    element = {'data': {'source': link['node1'], 'target': link['node2'], 'label': link['relType']}, 'classes': link['relType']}
    cytoscapeElements.append(element)

app = Dash()

cyto.load_extra_layouts()

app.layout = html.Div([
    cyto.Cytoscape(
        id='primaryMap',
        elements=cytoscapeElements,
        layout={'name': 'dagre', 'fit': True, 'nodeSep': 200},
        style={'width': '100vw', 'height': '100vh'},
        stylesheet = [
            {'selector': 'node', 'style': {'content': 'data(label)'}},
            {'selector': 'edge:selected', 'style': {'content': 'data(label)'}},
        ] + colors
    )
])

if __name__ == '__main__':
    app.run(debug=True)