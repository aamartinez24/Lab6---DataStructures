import queue

class GraphAM:

    def __init__(self, vertices, weighted=False, directed=False):
        self.am = []

        for i in range(vertices):  # Assumption / Design Decision: 0 represents non-existing edge
            self.am.append([0] * vertices)

        self.directed = directed
        self.weighted = weighted
        self.representation = 'AM'

    def is_valid_vertex(self, u):
        return 0 <= u < len(self.am)

    def insert_vertex(self):
        for lst in self.am:
            lst.append(0)

        new_row = [0] * (len(self.am) + 1)  # Assumption / Design Decision: 0 represents non-existing edge
        self.am.append(new_row)

        return len(self.am) - 1  # Return new vertex id

    def insert_edge(self, src, dest, weight=1):
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return

        self.am[src][dest] = weight

        if not self.directed:
            self.am[dest][src] = weight

    def delete_edge(self, src, dest):
        self.insert_edge(src, dest, 0)

    def num_vertices(self):
        return len(self.am)
    
    def get_adj_vertices(self, vertex):
        adjvert = []
        for dest in range(len(self.am[vertex])):
            if self.am[vertex][dest] != 0:
                adjvert.append(dest)
        return adjvert
    
class Disjoint_Set_Forest:
    
    def __init__(self, n):
        self.dsf = [-1] * n
        
    def find(self, a):
        if self.dsf[a] < 0:
            return a
        return self.find(self.dsf[a])
    
    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        
        self.dsf[rb] = ra

def compute_indegree_every_vertex(graph):
    indeg = {}
    for i in range(len(graph.am)):
        count = 0
        for j in range(len(graph.am[i])):
            if graph.am[j][i] != 0:
                count += 1
        indeg[i] = count
    return indeg

def topological_sort(graph):
    all_in_degrees = compute_indegree_every_vertex(graph)
    sort_result = []
    q = queue.Queue()
    
    for i in range(len(all_in_degrees)):
        if all_in_degrees[i] == 0:
            q.put(i)
            
    while not q.empty():
        u = q.get()
        sort_result.append(u)
        
        for adj_vertex in graph.get_adj_vertices(u):
            all_in_degrees[adj_vertex] -= 1
            
            if all_in_degrees[adj_vertex] == 0:
                q.put(adj_vertex)
                
    if len(sort_result) != len(graph.am):
        return None
    return sort_result 

def edge_sort(graph):
    l = {}
    for i in range(len(graph.am)):
        for j in range(len(graph.am[i])):
            if graph.am[i][j] != 0 and i != j and i < j:
                l[(i,j)] = graph.am[i][j]
    return sorted(l.items(), key=lambda x: x[1])

def kruskals_Al(graph):
    sort = edge_sort(graph)
    T={}
    i = 0
    forest = Disjoint_Set_Forest(len(sort))
    for edge in sort:
        if i == 0:
            T[edge[0]] = edge[1]
            tup = edge[0]
            forest.union(tup[0], tup[1])
            i += 1
        else:
            tup = edge[0]
            x = forest.find(tup[0])
            y = forest.find(tup[1])
            if x != y:
                forest.union(tup[0], tup[1])
                T[edge[0]] = edge[1]
    return T

def main():
    g = GraphAM(6, directed=True)
    g.insert_edge(0, 1)
    g.insert_edge(0, 4)
    g.insert_edge(1, 4)
    g.insert_edge(1, 2)
    g.insert_edge(4, 5)
    g.insert_edge(5, 2)
    g.insert_edge(5, 3)
    g.insert_edge(2, 3)
    
    g = GraphAM(6, weighted=True)
    g.insert_edge(0, 1, 4)
    g.insert_edge(0, 2, 3)
    g.insert_edge(1, 2, 2)
    g.insert_edge(2, 3, 1)
    g.insert_edge(3, 4, 5)
    g.insert_edge(4, 1, 4)
    print(kruskals_Al(g))
    
    
main()