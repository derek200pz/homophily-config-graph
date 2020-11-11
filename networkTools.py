#Takes a networkx graph and a list of categorical features of nodes in the graph.
def getHomophily(G, features):
    homophily = {}
    for feat in features:
        in_nodes = set([x for x,y in G.nodes(data=True) if y[feat]==1])
        relevant_edges = set([edge for node in in_nodes for edge in list(G.edges(node))])
        internal_edges = set([edge for edge in relevant_edges if edge[1] in in_nodes])
        homophily[feat] = len(internal_edges)*len(G.nodes(data=True))/(len(relevant_edges)*len(in_nodes))
    return homophily