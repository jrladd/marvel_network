#! /usr/bin/env python

import networkx as nx
from networkx.readwrite import json_graph
import json, community

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

with open('marvel_edges.csv') as edgecsv:
    rows = edgecsv.read().split('\r\n')
    edges = [r.split(',')[:2] for r in rows[1:]]
    weights = [r.split(',')[-1] for r in rows[1:]]
    edge_tuples=[(e[0], e[1], int(weights[i])) for i,e in enumerate(edges)]

edges = []
for e in edge_tuples:
    if all(x in node_ids for x in e[:2]):
        edges.append(e)

G = nx.Graph()
G.add_nodes_from(node_ids)
G.add_weighted_edges_from(edges)
groups = community.best_partition(G)

nx.set_node_attributes(G, 'name', node_dict)
nx.set_node_attributes(G, 'group', groups)

data = json_graph.node_link_data(G)
#id_with_name = {i:d['id'] for i,d in enumerate(data['nodes'])}
#new_data = dict(nodes=data['nodes'], links=[dict(source=id_with_name[d['source']],target=id_with_name[d['target']],weight=d['weight']) for d in data['links']])

#new_data = dict(nodes=[dict(id=n) for n in list(set(nodes))], links=[dict(source=node_dict[e[0]], target=node_dict[e[1]], weight=e[2]) for e in edges])

with open('marvel.json', 'w') as output:
    json.dump(data, output, sort_keys=True, indent=4, separators=(',',':'))
