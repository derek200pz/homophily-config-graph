import random
#2739
def rds_simulation(G, count=2739, max_rec=6, seed_count=10):
    seeds = random.sample(G.nodes, seed_count)
    sample = {}
    for seed in seeds:
        sample[seed] = []

    while len(sample.keys()) < count:
        node = random.choice(list(sample.keys()))
        if(len(sample[node]) < max_rec and len(G.edges(node)) > 0):
            recruit = random.choice(list(G.edges(node)))[1]
            if recruit not in list(sample.keys()):
                sample[node].append(recruit)
                sample[recruit] = []
    return sample
    
def test_sample(sample):
    recruitList = []
    for person in sample.keys():
        for recruit in sample[person]:
            recruitList.append(recruit)
    print("#################")
    for person in sample.keys():
        if person not in recruitList:
            print(f"person: {person} recruits: {sample[person]}")

def write_csv(filename, sample, G):
    with open(filename, "w") as outfile:
        #Write the column names
        outfile.write("index,coupon,r1,r2,r3,r4,r5,r6,netsize,")
        #Here we make the assumption that every node, even those that are not in the sample, have the same features
        for feat in G.nodes[0].keys():
            outfile.write(f"{feat},")
        outfile.write("\n")

        i = 0
        for person in sample.keys():
            #write the index, skipping this causes issues for RDSAnalyst
            outfile.write(str(i))
            outfile.write(",")
            i += 1
            #write the person's coupon code
            outfile.write(str(person))
            outfile.write(",")
            #write all 6 recruits, or just commas for less than 6 recruits
            for recruit in sample[person]:
                outfile.write(str(recruit))
                outfile.write(",")
            for extra in range(6 - len(sample[person])):
                outfile.write(",")
            #write the netsize (number of edges, perfectly accurate unlike in actual sathcap)
            outfile.write(str(len(G.edges(person))) + ",")
            #write features
            for feat in G.nodes[person].keys():
                outfile.write(str(G.nodes[person][feat]) + ",")
            outfile.write("\n")