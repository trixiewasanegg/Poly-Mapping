# Imports
from dash import Dash, html, callback, Input, Output
import dash_cytoscape as cyto
import json

#######################################
# Boilerplate functions
#######################################

# Transforms incoming string into base 10
# Used to generate unique IDs for edges
def base26_to_base10(base26):
    base10_val = 0
    for i, char in enumerate(reversed(base26)):
        base10_val  += (ord(char.upper()) - ord('A') + 1) * (26 ** i)
    return base10_val

# Transforms input JSON into cytoscape node notation
def nodeFormat(jsonIn):
    node = {'id':jsonIn['id'],'label': jsonIn['name'], 'color': jsonIn['hex']}
    return node

# Transforms input into cytoscape edge notation
def edgeFormat(source,dest,relType,relData):
    srcVal = base26_to_base10(source)
    destVal = base26_to_base10(dest)
    edgeID = hex(srcVal + destVal)[2:]
    relHex = relData["hex"]
    relStyle = relData["style"]
    relWidth = relData["width"]
    edge = {'data': {'id': edgeID, 'source': source, 'target': dest, 'label': relType, 'color': relHex, 'lineStyle': relStyle, 'width': relWidth, 'classes': ["edge", relType]}}
    return (edgeID,edge)

#######################################
# JSON Input & Transformation
#######################################

# Load Source JSON File
sourceFile = "source.json"
with open(sourceFile) as file:
    data = json.load(file)

# Reads JSON data, adds elements to a list for later use
elements = []
edgeDict = dict()
nodeConnections = dict()

# Reads data for groups
for group in data["groups"]:
    node = nodeFormat(group)
    node['classes'] = ['group']
    node['shortDesc'] = group['shortDesc']
    elements.append({'data': node})

# Reads data for gorups
for person in data["people"]:
    person['id'] = person['name']
    node = nodeFormat(person)
    if person['group'] != "":
        node['parent'] = person['group']
    node['classes'] = ["person"]
    elements.append({'data': node})

# Reads data for links
for link in data["links"]:
    source = link["source"]
    dest = link["dest"]
    relType = link["relType"]

    # Transforms to formatted edge & generates edgeID
    edgeTuple = edgeFormat(source,dest,relType,data['relColors'][relType])
    edgeID = edgeTuple[0]
    edge = edgeTuple[1]

    # adds data to NodeConnections
    for person in [source,dest]:
        if person in nodeConnections.keys():
            connections = nodeConnections[person]
            connections.append(edgeID)
            nodeConnections[person] = connections
        else:
            nodeConnections[person] = list([edgeID])

    # adds edge to edgeDict
    edgeDict[edgeID] = [source,dest]

    # adds edge to elements
    elements.append(edge)

# Loads some pre-set style values & misc metadata
meta = data['meta']
mapName = meta['mapName']
nodeSize = meta['nodeSize']
algo = meta['algo']
selectCol = meta['selectedColor']

# Sets pre-set styles to static variable for callbacks
stylePredef = [
    {'selector': 'node', 'style': {'content': 'data(label)', 'width': nodeSize, 'height': nodeSize, 'background-color': 'data(color)'}},
    {'selector': 'edge', 'style': {'curve-style': 'round-segments', 'width': 'data(width)','line-style': 'data(lineStyle)', 'line-color': 'data(color)'}}
]

styles = stylePredef

#######################################
# Dash app loading
#######################################
cyto.load_extra_layouts()
app = Dash()

app.layout = html.Div([
    cyto.Cytoscape(
        id=mapName,
        elements=elements,
        responsive=True,
        layout={'name': algo, 'fit': True, 'nodeSep': 200},
        style={'width': '100vw', 'height': '100vh'},
        stylesheet = styles,
    ),
])

@callback(
    Output(mapName, "stylesheet"),
    Input(mapName, "selectedNodeData"),
    Input(mapName, "selectedEdgeData"),
    prevent_initial_call=True,
)
def selectNode(nodes, edges):
    print(f"Node/s selected: {nodes}")
    newStyles = []
    if nodes != [] and nodes != None:
        for node in nodes:
            if 'group' in node['classes']:
                return stylePredef
            else:
                key = node['id']
                newStyles.append({'selector': '#'+key, 'style': {'background-color': selectCol}})
                connections = nodeConnections[key]
                print(f'Connections: {connections}')
                
                for con in connections:
                    newStyles.append({'selector': '#'+con, 'style': {'width': 5, 'content': 'data(label)'}})
                    linked = edgeDict[con]
                    if linked[0] != key:
                        newStyles.append({'selector': "#"+linked[0], 'style': {'background-color': selectCol}})
                    else:
                        newStyles.append({'selector': "#"+linked[1], 'style': {'background-color': selectCol}})



    print(f"Edge/s selected: {edges}")
    if edges != [] and edges != None:
        for edge in edges:
            newStyles.append({'selector': "#"+edge['id'], 'style': {'width': 5, 'content': 'data(label)'}})
            for node in [edge['source'], edge['target']]:
                newStyles.append(
                    {'selector': "#"+node, 'style': {'background-color': selectCol}}
                )

    return stylePredef + newStyles


if __name__ == '__main__':
    app.run(debug=True)