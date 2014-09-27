"""
proj1 contains the solutions to the proj1 problems.
"""
# Graph 0
EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2:set([])}

# Graph 1
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]), 6: set([])}

# Graph 2
EX_GRAPH2 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3,7]), 3: set([7]), 4: set([1]), 5: set([2]), 6: set([]), 7: set([3]), 8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """ Generates complete graph with num_nodes vertices."""
    res = dict()
    for node in xrange(0, num_nodes):
        edges = [edge for edge in xrange(0, num_nodes) if edge != node]
        res[node] = set(edges)
    return res

        
def compute_in_degrees(digraph):
    """ compute_in_degrees computes the in degrees for the directed graph digraph."""
    res = dict()
    for key in digraph.keys():
        res[key] = 0
    for vertices in digraph.values():
        for val in vertices:
            if val in res:
                res[val] += 1
            else:
                res[val] = 1
    return res

def compute_out_degrees(digraph):
    """ compute_out_degrees computes the out degrees for the directed graph digraph."""
    res = dict()
    for key, val in digraph.items():
        res[key] = len(val)
    return res

def in_degree_distribution(digraph):
    """ in_degree_distribution computes in degree distribution for directed graph digraph."""
    temp = compute_in_degrees(digraph)
    res = dict()
    for val in temp.values():
        if val in res:
            res[val] += 1
        else:
            res[val] = 1
    return res

