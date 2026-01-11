# Poly-Mapping
Polycule Mapping Using Dash Cytoscapes, akin to Polycul.Es.<br>
Grouping, highlighting of connected nodes when selecting edges & vice versa.

# TODO
- Cleanup callback selectors, messy AF

# Dependencies
Pip managed:
- dash
- dash_cytoscape

# Input data formatting
## meta - dict
- mapName - the map's name (str)
- nodeSize - how large your nodes should be (int)
- algo - what algorithm Cytoscapes should plot with (str)
- selectedColor - what color nodes should turn when selected (Hex with leading # as str)

## relColors - dict of dicts
key is the name of the relationship type.
Values within each dict:
- hex - color (Hex with leading # as str)
- style - solid/dashed (str)
- width - line width (int)

## groups - list of dicts
Each dict should have:
- id - unique ID (str)
- name - label name (str)
- shortDesc - Short description (str)
- hex - Color (Hex with leading # as str)

## people - list of dicts
Each dict should have:
- name - label name (str)
- groups - any groups they belong to (list)
- hex - Color (Hex with leading # as str)

## links - list of dicts
Each dict should have:
- source - matches a name in people (str)
- dest - matches a name in people (str)
- relType - matches a relationship type in relColors (str)

# Working data layouts
## elements (list of dicts)
List of elements for Cytoscapes to work with<br>
**All have:**
- id - for formatting & selection (str)
    - groups - ID defined in the JSON
    - people - ID is name
    - edge - ID is a combination of the source & dest labels
- label - for labelling (str)
- color - hex of the color to display (Hex with leading # as str)
- classes - list of classes
    - groups - just 'group'
    - people - just 'person'
    - edges - ['edge', and the RelType]

**Groups also have:**
- shortDesc - as definied in JSON (currently does nothing)

**People also have:**
- parent (optional) - as defined in JSON, must exist

**Edges also have:**
- source - as defined in JSON
- target - dest in JSON

## edgeDict (dict)
List of edges and their source and destination<br>
Allows for manipulation of nodes when an edge is selected<br>
- id:[source,target]

## nodeConnections (dict)
List of nodes and attached edges<br>
Allows for manipulation of edges when a node is selected<br>
- id:[list of edgeIDs]