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
def JSONToNode(jsonIn):
    node = {'id':jsonIn['id'],'label': jsonIn['name'], 'color': jsonIn['hex']}
    return node

# Transforms input JSON into cytoscape edge notation
def JSONToEdge(source,links,colors):
    srcVal = base26_to_base10(source)
    edgeTuples = []
    for link in links:
        dest = link[0]
        destVal = base26_to_base10(dest)
        relType = link[1]
        relHex = colors[relType]
        edgeID = hex(srcVal + destVal)[2:]
        edge = {'data': {'id': edgeID, 'source': source, 'target': dest, 'label': relType, 'color': relHex}, 'classes': relType}
        edgeTuples.append((edgeID,edge))
    return edgeTuples

#######################################
# JSON Input & Transformation
#######################################

# Load Source JSON File
sourceFile = "TestData.json"
with open(sourceFile) as file:
    data = json.load(file)

# Reads JSON data, adds elements to a list for later use
elements = []
edgeDict = dict()
nodeConnections = dict()

for group in data["groups"]:
    node = JSONToNode(group)
    node['classes'] = 'group'
    node['shortDesc'] = group['shortDesc']
    elements.append({'data': node})

for person in data["people"]:
    person['id'] = person['name']
    node = JSONToNode(person)
    if person['group'] != "":
        node['parent'] = person['group']
    node['classes'] = "person"

    elements.append({'data': node})
    relations = JSONToEdge(person['name'],person['links'], data['relColors'])
    relIDs = []
    for edge in relations:
        relIDs.append(edge[0])
        if not edge[0] in edgeDict.keys():
            edgeDict[edge[0]] = [person['id'],edge[1]['data']['target']]
            elements.append(edge[1])
    nodeConnections[person['name']] = relIDs

# Loads some pre-set style values & misc metadata
meta = data['meta']
mapName = meta['mapName']
nodeSize = meta['nodeSize']
algo = meta['algo']
selectCol = meta['selectedColor']

# Sets pre-set styles to static variable for callbacks
stylePredef = [
    {'selector': 'node', 'style': {'content': 'data(label)', 'width': nodeSize, 'height': nodeSize, 'background-color': 'data(color)'}},
    {'selector': 'edge', 'style': {'curve-style': 'round-segments', 'width': 2, 'line-color': 'data(color)'}}
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
    )
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
            if node['classes'] == 'group':
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