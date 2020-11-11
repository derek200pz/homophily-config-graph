import networkx as nx
import rdsSimulator as rs
import networkTools as nt
import networkGenerator as ng
#G = ng.generate_erdos_renyi(15000, add_race=True)
featuresxxx = {
    "alive": 0.12,
    "barefoot": 0.8,
    "bald": 0.01,
    "blind": 0.005,
    "afflicted": 0.08,
}

features = {
    "p=0.1": 0.1,
    "p=0.4": 0.4,
    "p=0.3": 0.3,
    "p=0.01": 0.01,
    "p=0.2": 0.2,
    "p=0.5": 0.5,
    "p=0.1": 0.1,
    "p=0.1": 0.1,
    "p=0.3": 0.3,
    "p=0.09": 0.09,
    "p=0.07": 0.07,
    "p=0.03": 0.03,
    "p=0.1": 0.1,
    "p=0.44": 0.44,
    "p=0.13": 0.13,
}

homophilyxxx = {
    "alive": 1,
    "barefoot": 0.8,
    "bald": 1.5,
    "blind": 2,
    "afflicted": 1.1,
}

homophily = {
    "p=0.1": 0.6,
    "p=0.4": 0.7,
    "p=0.3": 0.8,
    "p=0.01": 0.9,
    "p=0.2": 1,
    "p=0.5": 1.1,
    "p=0.1": 1.2,
    "p=0.1": 1.3,
    "p=0.3": 1.4,
    "p=0.09": 1.5,
    "p=0.07": 1.6,
    "p=0.03": 1.7,
    "p=0.1": 1.8,
    "p=0.44": 1.9,
    "p=0.13": 2,
}

G = ng.generate_homophily_configuration(15000, features=features, homophily=homophily, passes=20)
homo = nt.getHomophily(G, list(features.keys()))

for feat in homo:
    print(f"{feat} homophily: {homo[feat]}")


# print(G.nodes[2])
# print(G.nodes[3])
# print(G.nodes[4])
# print(G.nodes[5])
# print(G.nodes[6])

#sample = rs.rds_simulation(G)
#rs.test_sample(sample)
# print(sample)
#rs.write_csv("sim.csv", sample, G)

# import matplotlib.pyplot as plt
# nx.draw_networkx(G, node_color="#ddddff", edge_color="#7777ff",font_size=8)
# plt.show()
