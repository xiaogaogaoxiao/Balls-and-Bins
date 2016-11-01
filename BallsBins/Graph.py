import networkx as nx
import math
import sys
import numpy as np
#import matplotlib.pyplot as plt

sqrt = math.sqrt


# This function return a square lattice graph.
# The lattice size should be a perfect square.
def Gen2DLattice(size):
    side = sqrt(size)
    if not side.is_integer():
        print("Error: the size of lattice is not perfect square!")
        sys.exit()

    G = nx.empty_graph(size)

    for i in range(size):
        r = i // side
        c = i % side
        # Now we have to add 4 edges to the neighbours of i_th node
        # Adding edge to the neighbour: (r+1,c)
        l = ((r+1) % side) * side + c
        G.add_edge(i,l)
        # Adding edge to the neighbour: (r-1,c)
        l = ((r-1) % side) * side + c
        G.add_edge(i,l)
        # Adding edge to the neighbour: (r,c+1)
        l = r * side + ((c+1) % side)
        G.add_edge(i,l)
        # Adding edge to the neighbour: (r,c-1)
        l = r * side + ((c-1) % side)
        G.add_edge(i,l)

    return G


# This function return the shortest path from a source node to
# the rest of torus nodes.
# The upper left node is labeled by 0 and the lower right by size-1
# size: is the size of torus and it should be a perfect square.
def shortest_path_length_torus(size, source):
    side = int(sqrt(size))
    src_r = source // side
    src_c = source % side
#    shortest_path_length = {}
#    for i in xrange(size):
#        r = i // side
#        c = i % side
#        shrtplen = min(abs(src_c-c)+abs(src_r-r), abs(src_c-side-c)+abs(src_r-r), abs(src_c+side-c)+abs(src_r-r), abs(src_c-c)+abs(src_r-side-r), abs(src_c-c)+abs(src_r+side-r))
#        shortest_path_length[i] = shrtplen
    i = np.arange(size, dtype=np.int32)
    r = i // side
    c = i % side
    tmp = np.column_stack((abs(src_c-c)+abs(src_r-r), abs(src_c-side-c)+abs(src_r-r), abs(src_c+side-c)+abs(src_r-r), abs(src_c-c)+abs(src_r-side-r), abs(src_c-c)+abs(src_r+side-r)))
#    print(r)
#    print(c)
#    print((abs(src_c-c)+abs(src_r-r)).shape)
    shortest_path_length = np.amin(tmp, axis=1)
#    print(tmp.shape)
#    print(tmp)
#    print(shortest_path_length[1].dtype.name)

    return shortest_path_length