import networkx as nx
import random
import networkTools as nt


def generate_homophily_configuration(n, features=False, homophily=False, passes=1):
    
    print(f"Generating Pre-Graph")
    degrees = [random.randrange(50) for x in range(n)]
    #sum of the degrees must be even for configuration graph
    if sum(degrees) % 2 == 1:
        degrees[0] += 1
    #if no feat/homophily information is given, just use a regular configuration graph
    if features and homophily:
        G = nx.configuration_model(degrees)
        print(f"Adding Features")
        G = add_features(G, features)
        #create lists of the nodes included and the nodes not included in each feature (yes or no features)
        print(f"Creating Feature Tracking Sets")
        featlists = {}
        for feat in homophily.keys():
            featlists[f"{feat}_1"] = set([x for x,y in G.nodes(data=True) if y[feat]==1])
            featlists[f"{feat}_0"] = set([x for x,y in G.nodes(data=True) if y[feat]==0])
        
        #Some math scribbles about homophily:

        # (InDeg/TotDeg)/(In/Tot) == Indeg*Tot/(Totdeg*In)

        # homophily == Indeg*Tot/(Totdeg*In)

        # homophily*Totdeg*In/Tot == Indeg

        # homophily*Totdeg*feat_p == Indeg

        with open("out.csv", "w") as outfile:
                for feat in homophily.keys():
                    outfile.write(f"{feat},")
                outfile.write("\n")

        for i in range(passes):
            homo = nt.getHomophily(G, list(homophily.keys()))
            with open("out.csv", "a") as outfile:
                for feat in homophily.keys():
                    outfile.write(f"{homo[feat]},")
                outfile.write("\n")
            print(f"Starting Pass {i}")
            for feat in homophily.keys():
                # print(f"\t{feat}")
                relevant_edges = set([edge for node in featlists[f"{feat}_1"] for edge in list(G.edges(node))])      #This is nonsense. Python is whack for this double list comprehension.
                internal_edges = set([edge for edge in relevant_edges if edge[1] in featlists[f"{feat}_1"]])
                external_edges = set([edge for edge in relevant_edges if edge not in internal_edges])
                correction_factor = 0.5/(1-features[feat]) #This correction factor corrects for two things: 1: that inner edges are counted twice, causing the rewirings to overshoot for low p values, and 2: that the p value affects how likely it is that an edge is redundantly added (line 70, "newEdge = random.sample(node_list, 2)")
                rewire_count = int((homophily[feat]*len(relevant_edges)*features[feat] - len(internal_edges))*correction_factor)

                # print(f"expected internal edges given homophily: {homophily[feat]*len(relevant_edges)*features[feat]}")
                # print(f"actual internal edges before applying homophily: {len(internal_edges)}")
                # print(f"Number of edges to rewire: {rewire_count}")
                # print(f"homophily before rewiring: {len(internal_edges)/len(relevant_edges)/features[feat]}")

                if rewire_count > 0:
                    
                    #remove some external edges
                    old_edges = random.sample(external_edges, min(len(external_edges), rewire_count))
                    for edge in old_edges:
                        G.remove_edge(edge[0], edge[1])

                    #insert some internal edges
                    node_list = list(featlists[f"{feat}_1"])
                    for i in range(rewire_count):
                        newEdge = random.sample(node_list, 2) #choosing randomly from a list is faster than a set. NOTE: this does not always add a new edge, as the edge might already be there. Since this is a monte carlo algorithm, exact precision does not matter.
                        G.add_edge(newEdge[0], newEdge[1])
                    
                elif rewire_count < 0:
                    rewire_count = -rewire_count

                    #remove some internal edges
                    no_dulicates = set()  #remove double-edges such as (1,3) and (3,1) from set:
                    for edge in internal_edges:
                        if (edge[1], edge[0]) not in no_dulicates:
                            no_dulicates.add(edge)

                    old_edges = random.sample(no_dulicates, min(len(no_dulicates), rewire_count)) 
                    
                    for edge in old_edges:
                        G.remove_edge(edge[0], edge[1])

                    #insert some external edges
                    in_node_list = random.choices(list(featlists[f"{feat}_1"]), k=rewire_count)
                    ex_node_list = random.choices(list(featlists[f"{feat}_0"]), k=rewire_count)
                    for i in range(rewire_count):
                        G.add_edge(in_node_list[i], ex_node_list[i])
                
    #If there is no homphily given or no feats given:
    else:
        print("generate_homophily_configuration: WARNING: either features or homophily parameters are missing.")
        G = nx.configuration_model(degrees)
        #to remove parallel edges:
        G=nx.Graph(G)
        #to remove self-loops:
        G.remove_edges_from(nx.selfloop_edges(G))
        if(features):
            G = add_features(G, features)
            

    return G

def generate_erdos_renyi(n, features=False):
    G = nx.erdos_renyi_graph(n, 1/n*10)
    if(features):
        G = add_features(G, features)
    return G

def generate_barabasi_albert(n, features=False):
    G = nx.barabasi_albert_graph(n, 5)
    if(features):
        G = add_features(G, features)
    return G

#features must be a dict where the keys are feature names and the values are feature probabilities (0 - 1) 
def add_features(G, features):
    attrib = {}
    
    for node in G:
        attrib[node] = {}
        for feat in features.keys():
            attrib[node][feat] = coinFlip(features[feat])
    nx.set_node_attributes(G, attrib)
    return G

def coinFlip(p):
    return 1 if random.random() < p else 0