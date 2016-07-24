#! /usr/bin/env python

import networkx as nx
from networkx.readwrite import json_graph
import json, community
from networkx.algorithms import centrality as cn

# Nodes and edges csv files are in Gephi form. Get information into usable dictionaries and tuples.

# Creates dictionary of id:name pairs.
with open('marvel_nodes.csv') as nodecsv:
    rows = nodecsv.read().split('\r\n')
    node_dict = {}
    for r in rows[1:]:
        r = r.split(',')
        node_dict[r[0]] = r[1]
    print node_dict


node_dict={k:v.title() for k,v in node_dict.items()}
node_ids = node_dict.keys()
nodes = node_dict.values()

# Creates tuples with source, target, and weight.
with open('marvel_edges.csv') as edgecsv:
    rows = edgecsv.read().split('\r\n')
    edges = [r.split(',')[:2] for r in rows[1:]]
    weights = [r.split(',')[-1] for r in rows[1:]]
    edge_tuples=[(e[0], e[1], int(weights[i])) for i,e in enumerate(edges)]

# Only get edges for the select nodes in the node csv.
edges = []
for e in edge_tuples:
    if all(x in node_ids for x in e[:2]):
        edges.append(e)

# Initialize graph, add nodes and edges, calculate modularity and centrality.
G = nx.Graph()
G.add_nodes_from(node_ids)
G.add_weighted_edges_from(edges)
groups = community.best_partition(G)
degree = cn.degree_centrality(G)
betweenness = cn.betweenness_centrality(G, weight='weight')
eigenvector = cn.eigenvector_centrality(G, weight='weight')

# Add node attributes for name, modularity, and three types of centrality.
nx.set_node_attributes(G, 'name', node_dict)
nx.set_node_attributes(G, 'group', groups)
nx.set_node_attributes(G, 'degree', degree)
nx.set_node_attributes(G, 'betweenness', betweenness)
nx.set_node_attributes(G, 'eigenvector', eigenvector)

# Create json representation of the graph (for d3).
data = json_graph.node_link_data(G)

# You could create the needed json without NetworkX (but you would forfeit network metrics).
#new_data = dict(nodes=[dict(id=n) for n in list(set(nodes))], links=[dict(source=node_dict[e[0]], target=node_dict[e[1]], weight=e[2]) for e in edges])

# Output json of the graph.
with open('marvel.json', 'w') as output:
    json.dump(data, output, sort_keys=True, indent=4, separators=(',',':'))
