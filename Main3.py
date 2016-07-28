# In this file we use Simulator3 to find the trade-off between maximum load and
# communication cost.

from __future__ import division
import math
#import matplotlib.pyplot as plt
#import networkx as nx
from multiprocessing import Pool
import sys
import numpy as np
import scipy.io as sio
import time
#from BallsBins.Simulator1 import Simulator1
#from BallsBins.Simulator1 import Simulator1_lowmem
#from BallsBins.Simulator2 import Simulator2
#from BallsBins.Simulator2 import Simulator2_lowmem
from BallsBins.Simulator_Torus import *



#--------------------------------------------------------------------
#log = math.log
sqrt = math.sqrt

#--------------------------------------------------------------------
# Simulation parameters

# Base part of the output file name
base_out_filename = 'Tradeoff'
# Pool size for parallel processing
pool_size = 4
# Number of runs for computing average values. It is more eficcient that num_of_runs be a multiple of pool_size
num_of_runs = 4

# Number of servers
srv_num = 625
#srv_range = [500, 1000, 2000, 5000, 7000, 10000, 20000, 50000, 70000, 100000, 200000, 500000]
#srv_range = [2025, 5041, 7056, 10000, 20164, 50176, 70225, 100489]
#srv_range = [225, 324, 625, 900, 1225, 1600, 2025, 3025, 4096, 5041]

# Cache size of each server (expressed in number of files)
cache_sz = 2000

# Total number of files in the system
file_num = 200

# Range of alpha where alpha is the trade-off parameter and determines the radius of our search.
alpha_range = [0, 0.2, 0.4, 0.7, 1, sqrt(2), sqrt(3), sqrt(4), sqrt(6), sqrt(8), sqrt(12), sqrt(16), sqrt(25), 6, 10, 15, 30, 60, 120]
#alpha_range = [50]

# The graph structure of the network
# It can be:
# 'Lattice' for square lattice graph. For the lattice the graph size should be perfect square.
graph_type = 'Lattice'
#graph_type = 'RGG'

#--------------------------------------------------------------------


if __name__ == '__main__':
    # Create a number of workers for parallel processing
    pool = Pool(processes=pool_size)

    t_start = time.time()

    rslt_maxload = np.zeros((len(alpha_range),1+num_of_runs))
    rslt_avgcost = np.zeros((len(alpha_range),1+num_of_runs))
    for i, alpha in enumerate(alpha_range):
        params = [(srv_num, cache_sz, file_num, graph_type, alpha) for itr in range(num_of_runs)]
        print(params)

        rslts = pool.map(simulator3_torus, params)
#        rslts = [Simulator3((srv_num, cache_sz, file_num, graph_type, alpha))]

        for j, rslt in enumerate(rslts):
            #print(rslt)
            rslt_maxload[i, j + 1] = rslt['maxload']
            rslt_avgcost[i, j + 1] = rslt['avgcost']
            #tmpmxld = tmpmxld + rslt['maxload']
            #tmpavgcst = tmpavgcst + rslt['avgcost']

            rslt_maxload[i, 0] = alpha
            rslt_avgcost[i, 0] = alpha

    t_end = time.time()
    print("The runtime is {}".format(t_end-t_start))

    # Write the results to a matlab .mat file
    sio.savemat(base_out_filename + '_srvn={}_fn={}_cs={}_itr={}.mat'.format(srv_num, file_num, cache_sz, num_of_runs), {'maxload': rslt_maxload, 'avgcost': rslt_avgcost})

#    if (simulator == 'one choice') or (simulator == 'one choice, low mem'):
#        sio.savemat(base_out_filename + '_one_choice_' + 'fn={}_cs={}_itr={}.mat'.format(file_num, cache_sz, num_of_runs), {'maxload': rslt_maxload, 'avgcost': rslt_avgcost})
#    elif (simulator == 'two choice') or (simulator == 'two choice, low mem'):
#        sio.savemat(base_out_filename + '_two_choice_' + 'fn={}_cs={}_itr={}.mat'.format(file_num, cache_sz, num_of_runs), {'maxload': rslt_maxload, 'avgcost': rslt_avgcost})

#    if simulator == 'one choice':
#        np.savetxt(base_out_filename+'_sim1_'+'fn={}_cs={}_itr={}.txt'.format(file_num,cache_sz,num_of_runs), result, delimiter=',')
#    elif simulator == 'two choice':
#        np.savetxt(base_out_filename+'_sim2_'+'fn={}_cs={}_itr={}.txt'.format(file_num,cache_sz,num_of_runs), result, delimiter=',')

#    plt.plot(result[:,0], result[:,1])
#    plt.plot(result[:,0], result[:,2])
#    plt.xlabel('Cache size in each server (# of files)')
#    plt.title('Random server selection methods. Number of servers = {}, number of files = {}'.format(srv_num,file_num))
#    plt.show()

    #print(result['loads'])
    #print("------")
    #print('The maximum load is {}'.format(result['maxload']))
    #print('The average request cost is {0:0}'.format(result['avgcost']))

