# Imports
from dash import Dash, html, callback, Input, Output
import dash_cytoscape as cyto

testDataFile = "TestData-Simple.csv"
testStyleFile = "TestStyles-Simple.csv"
testNodeFile = "TestNodes-Simple.csv"

nodes = []
with open(testNodeFile) as csv:
    lines = csv.readlines()
    for line in lines[1:]:
        vals = line.replace('\n','').split(",")
        node = {'data': {'id': vals[0],'label': vals[0],'classes': vals[1]}}
        if str(vals[2]) != 'None':
            node['data']['parent'] = vals[2]

        nodes.append(node)


links = []
nodeConnections = dict()

# Reads CSV
with open(testDataFile) as csv:
    lines = csv.readlines()
    for line in lines[1:]:
        vals = line.replace('\n','').split(",")
        edgeID = vals[0]
        node1 = vals[1]
        node2 = vals[2]
        relType = vals[3]
        link = {'id': edgeID,'node1': node1, 'node2': node2, 'relType': relType}
        links.append(link)
        try:
            nodeConnections[node1].add(edgeID)
        except:
            nodeConnections[node1] = set()
            nodeConnections[node1].add(edgeID)
        
        try:
            nodeConnections[node2].add(edgeID)
        except:
            nodeConnections[node2] = set()
            nodeConnections[node2].add(edgeID)

nodeSize = 20

stylePredef = [
    {'selector': 'node', 'style': {'content': 'data(label)', 'z-index': 999, 'width': nodeSize, 'height': nodeSize}},
    {'selector': 'edge', 'style': {'curve-style': 'round-segments', 'width': 2}},
    {'selector': 'edge:selected', 'style': {'content': 'data(label)', 'width': 5}}
]

with open(testStyleFile) as csv:
    lines = csv.readlines()
    for line in lines[1:]:
        vals = line.replace('\n','').split(",")
        style = {'selector': '.'+vals[0], 'style': {'line-color': "#"+vals[1],'background-color': "#"+vals[1]}}
        stylePredef.append(style)

styles = stylePredef

# Pulls from links & nodes, generates cytoscape elements
cytoscapeElements = nodes

for link in links:
    element = {'data': {'id': link['id'],'source': link['node1'], 'target': link['node2'], 'label': link['relType']}, 'classes': link['relType']}
    cytoscapeElements.append(element)

app = Dash()

cyto.load_extra_layouts()

app.layout = html.Div([
    cyto.Cytoscape(
        id='primaryMap',
        elements=cytoscapeElements,
        responsive=True,
        layout={'name': 'dagre', 'fit': True, 'nodeSep': 200},
        style={'width': '100vw', 'height': '100vh'},
        stylesheet = styles,
    )
])

@callback(
    Output("primaryMap", "stylesheet",allow_duplicate=True),
    Input("primaryMap", "selectedNodeData"),
    Input("primaryMap", "selectedEdgeData"),
    prevent_initial_call=True,
)
def selectNode(nodes, edges):
    print(f"Node/s selected: {nodes}")
    newStyles = []
    if nodes != [] and nodes != None:
        for node in nodes:
            if node['classes'] == 'Group':
                return stylePredef
            else:
                key = node['id']
                connections = nodeConnections[key]
                print(f'Connections: {connections}')
                
                for con in connections:
                    newStyles.append({'selector': '#'+con, 'style': {'width': 5, 'content': 'data(label)'}})

    print(f"Edge/s selected: {edges}")
    largeNode = nodeSize * 1.25
    if edges != [] and edges != None:
        for edge in edges:
            for node in [edge['source'], edge['target']]:
                newStyles.append(
                    {'selector': "#"+node, 'style': {'width': largeNode, 'height': largeNode}}
                )

    return stylePredef + newStyles


if __name__ == '__main__':
    app.run(debug=True)