# Poly-Mapping
Polycule Mapping Using Dash Cytoscapes, akin to Polycul.Es.
Grouping, highlighting of connected nodes when selecting edges & vice versa.

# TODO
- Cleanup callback selectors, messy AF

# Dependencies
Pip managed:
- dash
- dash_cytoscape

# Template Data - TestData.json (git ignored)
## meta - dict
- mapName - the map's name (str)
- nodeSize - how large your nodes should be (int)
- algo - what algorithm Cytoscapes should plot with (str)
- selectedColor - what color nodes should turn when selected (Hex with leading # as str)

## relColors - dict
- Key/Value pairs of relationship types & their respective Hex with leading # as str

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
- links - list of links with names of other relationships and what types