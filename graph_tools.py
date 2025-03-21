import os
import itertools
import copy
import numpy as np
from itertools import combinations

##### This is the main graph class. It contains the methods for creating and 
##### minor manipulations of graphs. The creation and edge insertion process creates 
##### undirected graphs with edge labels, though one can easily adapt the representation for directed
##### graphs. Indeed, we later define the DAG (directed acyclic graph) class by
##### inheriting the methods of this class.
##### 
##### 
##### The graph is stored as an adjacency list. This is represented by a dict() structure,
##### where the keys are vertices and the values are also dict() storing the corresponding neighborhood lists. 
##### The neighborhood is stored as a dict(), so that we can store values/labels corresponding to each edge. 
#####
##### So, if an edge (u,v) has value q, then: in the adjacency structure of u, v is a key with value q.


##### 
##### C. Seshadhri, Jan 2015, Jan 2025



class graph(object):

#### Initializing empty graph
####

    def __init__(self):
        self.adj_list = dict()   # Initial adjacency list is empty dictionary 
        self.vertices = set()    # Vertices are stored in a set   
        self.degrees = dict()    # Degrees stored as dictionary

        
    def isNode(self, node):
    # Check if the node is in the graph's vertices
        if node in self.vertices:
            return True
    # Alternatively, you can check if the node is in the adjacency list
    # if node in self.adj_list:
    #     return True
        return False

#### Checks if (node1, node2) is edge of graph. Output is 1 (yes) or 0 (no).
####

    def isEdge(self,node1,node2):
        if node1 in self.vertices:               # Check if node1 is vertex
            if node2 in self.adj_list[node1]:    # Then check if node2 is neighbor of node1
                return 1                         # Edge is present!

        if node2 in self.vertices:               # Check if node2 is vertex
            if node1 in self.adj_list[node2]:    # Then check if node1 is neighbor of node2 
                return 1                         # Edge is present!

        return 0                # Edge not present!

#### Add undirected, simple edge (node1, node2, value)
#### The default value is just 1.
####
    
    def Add_und_edge(self,node1,node2,value=1):
        if node1 == node2:            # Self loop, so do nothing
            return
        if node1 in self.vertices:        # Check if node1 is vertex
            nbrs = self.adj_list[node1]   # nbrs is neighbor list of node1
            if node2 not in nbrs:         # Check if node2 already neighbor of node1
                nbrs[node2] = value       # Add node2 with value to the list. So node2 is the key, and value is the, well, value
                self.degrees[node1] = self.degrees[node1]+1    # Increment degree of node1

        else:                    # So node1 is not vertex
            self.vertices.add(node1)        # Add node1 to vertices
            self.adj_list[node1] = dict()  # Initialize node1's list as empty dictionary
            self.adj_list[node1][node2] = value  # Initialize node1's list to have node2 with associated value
            self.degrees[node1] = 1         # Set degree of node1 to be 1

        if node2 in self.vertices:        # Check if node2 is vertex
            nbrs = self.adj_list[node2]   # nbrs is neighbor list of node2
            if node1 not in nbrs:         # Check if node1 already neighbor of node2
                nbrs[node1] = value       # Add node1 with value to the list.
                self.degrees[node2] = self.degrees[node2]+1    # Increment degree of node2

        else:                    # So node2 is not vertex
            self.vertices.add(node2)        # Add node2 to vertices
            self.adj_list[node2] = dict()  # Initialize node2's list as empty dictionary
            self.adj_list[node2][node1] = value # Add node2 to the adjacency list, with associated value
            self.degrees[node2] = 1         # Set degree of node2 to be 1

#### Read a graph from a file with list of edges. Arguments are fname (file name), sep (separator). Looks for file fname.
#### Assumes that line looks like:
#### 
#### node1 sep node2 sep <anything else>
#### 
#### If sep is not set, then it is just whitespace.
#### IMPORTANT: if the first character of line is # (hash), this line is assumed to be a comment and ignored.
####
 
#     def Read_edges(self,fname,sep=None):
#         f_input = open(fname,'r')        # Open file
#         list_edges = f_input.readlines() # Read lines as list

#         print('raw edges =',len(list_edges))    # Print number of lines in file
#         for each_edge in list_edges:             # Loop of each line/edge
#             edge = each_edge.strip()             # Remove whitespace from edge
#             if len(edge) == 0:                   # If empty line, move to next line
#                 continue
# #             if edge[0] == '#':                   # line starts with #, and is comment
# #                 continue                         # this is comment, so move to next line
#             tokens = edge.split(sep)        # Split by sep to get tokens (nodes)

#             self.Add_und_edge(tokens[0],tokens[1]) # Add undirected edge given by first two tokens

    def Read_edges(self,fname,sep=None):
        with open(fname, 'r', encoding='utf-8') as file:
            for line in file:
                # Skip empty lines or comments
                if not line.strip():
                    continue

                # Split the line into tokens: Actor1, Actor2, MovieName
                tokens = line.strip().split(' ')

                # Extract the movie name and actors
                movie = tokens[0]
                actors = tokens[1:]

                # Add an edge between every pair of actors for the movie
                for actor1, actor2 in combinations(actors, 2):
                    self.Add_und_edge(actor1, actor2, movie)
#### Give the size of the graph. Outputs [vertices (sum of degrees) wedges]
#### Note that sum of degrees is twice the number of edges in the undirected case 
####

    def Size(self):
        n = len(self.vertices)            # Number of vertices

        m = 0                    # Initialize edges/wedges = 0
        wedge = 0
        for node in self.vertices:        # Loop over nodes
            deg = self.degrees[node]      # Get degree of node
            m = m + deg                   # Add degree to current edge count
            wedge = wedge+deg*(deg-1)/2   # Add wedges centered at node to wedge count
        return [n, m, wedge]              # Return size info

#### Print the adjacency list of the graph. Output is written in dirname/fname. 
####
 
    def Output(self,fname,dirname):
        os.chdir(dirname)
        f_output = open(fname,'w')    # Opening file

        for node1 in list(self.adj_list.keys()):   # Looping over nodes
            f_output.write(str(node1)+': ')        # Writing node
            for node2 in (self.adj_list)[node1]:   # Looping over neighbors of node1
                f_output.write(str(node2)+' ')     # Writing out neighbor
            f_output.write('\n')
        f_output.write('------------------\n')     # Ending with dashes
        f_output.close()

#### Compute the degree distribution of graph. Note that the degree is the size of the neighbor list, and is hence the *out*-degree if graph is directed. 
#### Output is a list, where the ith entry is the number of nodes of degree i.
#### If argument fname is provided, then list is written to this file. (This is convenient for plotting.)
####
 
    def Deg_dist(self,fname=''):
        degs = list((self.degrees).values())    # List of degrees
        dd = np.bincount(degs)                  # Doing bincount, so dd[i] is number of entries of value i in degs
        if fname != '':                         # If file name is actually given
            f_input = open(fname,'w')
            for count in dd:                    # Write out each count in separate line
                f_input.write(str(count)+'\n')
            f_input.close()
        return dd 

#### The fun stuff. This computes the core numbers/degeneracy by applying the minimum vertex removal algorithm. Basically, it iteratively removes 
#### the vertex of minimum degree, till the graph is empty. This leads to an order of vertex removal, say v1, v2, v3,...,vn. The algorithm then
#### constructs the graph where all edges only point from vi to vj where i < j. This creates a DAG, where each edge of the original graph is directed.
#### 
#### The output is this directed graph. Each DAG object (see end) has an associated topological ordering of vertices. In this case, this ordering
#### is just v1, v2, ..., vn.
#### 

    def Degeneracy(self):
        G = copy.deepcopy(self)      # Generate deepcopy, since we will modify G
        n = len(G.vertices)
        top_order = [0]*(n+1)        # Initialize list of degeneracy ordering
        core_G = DAG()               # This is the DAG that will be output
        core_G.vertices = copy.deepcopy(G.vertices)    # Vertices are the same
        for node in core_G.vertices: # Initialize adjacency list and degrees of core_G, the output
            core_G.adj_list[node] = set()
            core_G.degrees[node] = 0

        deg_list = [set() for _ in range(n)]    # Initialize list, where ith entry is set of deg i vertices
        min_deg = n       # variable for min degree of graph

       
        for node in G.vertices:    # Loop over nodes
            deg = G.degrees[node]      # Get degree of node
            deg_list[deg].add(node)    # Update deg_list with node
            if deg < min_deg:          # Update min_deg
                min_deg = deg

        # At this stage, deg_list[d] is the list of vertices of degree d

        for i in range(n):        # The main loop, just going n times
                                  
            # We first need the vertex of minimum degree. Due to the looping and deletion of vertex, we may have exhaused
            # all vertices of minimum degree. We need to update the minimum degree

            while len(deg_list[min_deg]) == 0:  # update min_deg to reach non-empty set
                min_deg = min_deg+1
                
            source = deg_list[min_deg].pop()    # get vertex called "source" with minimum degree 
            core_G.top_order.append(source)     # append to this to topological ordering
            
            # We got the vertex of the ordering! All we need to do now is delete vertex from the graph,
            # and update deg_list appropriately.

            for node in G.adj_list[source]: # loop over nbrs of source, each nbr called "node" 
 
                # We update deg_list
                deg = G.degrees[node]           # degree of node
                deg_list[deg].remove(node)      # move node in deg_list, decreasing its degree by 1
                deg_list[deg-1].add(node)
                if deg-1 < min_deg:             # update min_deg in case node has lower degree
                    min_deg = deg-1

               
                # We then remove the edge (node,source) from G
                G.adj_list[node].remove(source) # remove this edge from G
                G.degrees[node] -= 1            # update degree of node

                core_G.adj_list[source].add(node) # Add directed edge (source,node) to output DAG core_G
                core_G.degrees[source] += 1       # Update the degree of source
                
        return core_G


#### The DAG class is inherited from the graph class, and the only difference is an additional topological ordering.
#### For outputting into a file, we print the vertices in topological order, so we redefine output.

class DAG(graph):

    def __init__(self):
        super(DAG,self).__init__()
        DAG.top_order = []

    def Output(self,fname):
        f_output = open(fname,'w')

        for node1 in list(self.top_order):
            f_output.write(str(node1)+': ')
            for node2 in (self.adj_list)[node1]:
                f_output.write(str(node2)+' ')
            f_output.write('\n')

