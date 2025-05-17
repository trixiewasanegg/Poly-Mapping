# Poly-Mapping
Polycule Mapping Using Dash Cytoscapes, akin to Polycul.Es.
Grouping, highlighting of connected nodes when selecting edges & vice versa.

# TODO
- Currently data is stored in multiple CSV files, need to build in JSON import.

# Dependencies
Pip managed:
- dash
- dash_cytoscape

# Template Data
## TestData-Simple.csv (git ignored)
CSV file with 3 columns for test data
- ID - Unique ID
- Node 1 - Name, must be on testNodes list
- Node 2 - Name, must be on testNodes list
- RelType - Relationship Type

## TestStyles-Simple.csv (git ignored)
CSV file with 2 columns for colors
- RelType - matches TestData RelType
- Hex - hex color

## TestNodes-Simple.csv (git ignored)
CSV file with 3 columns
- Name - Name of the node
- Class - Group or Person
- Group - Group this node falls under, or "None" if not