def relax(u, v, w, distances):
    old = distances[v]
    new = distances[u] + w
    if new < old:
        distances[v] = new

def init_distances(vertices, source):
    distances = {u: float("infinity") for u in vertices}
    distances[source] = 0

    return distances


def BellmanFord(graph, source):

    # assume the graph is preprocessed like this
    vertices = {u for (u, v) in graph.keys()} | {v for (u, v) in graph.keys()}
    edges_with_weights = graph.items()

    # up to here zero cost

    # assume distances are stored in a dictionary
    distances = init_distances(vertices, source) # O(|V|)

    # up to here O(|V|) cost

    # let's rock
    for iters in range(len(vertices)): # O(|V|)
        for (u, v), w in edges_with_weights: # O(|E|)
            relax(u, v, w, distances) # O(1) decrease key

    # O(|V| * |E|)

    print distances

def DummyDijkstra(graph, source):

    # assume the graph is preprocessed like this
    vertices = {u for (u, v) in graph.keys()} | {v for (u, v) in graph.keys()}
    neighbors = {u: {v for (_, v) in graph if _ == u} for u in vertices}

    # up to here zero cost

    # assume distances are stored in a dictionary
    distances = init_distances(vertices, source) # O(|V|)

    # up to here O(|V|) cost

    # let's rock
    while vertices: # O(|V|) since each node is visited once
        # get nearest non-visited vertex
        _, u = min([(distances[u], u) for u in vertices]) # O(|V|) extract min
        vertices -= {u} # remove vertex if visited

        for v in neighbors[u]: # O(|E|) overall since each edge visted once
            relax(u, v, graph[(u, v)], distances) # O(1) decrease key

    # O(|V|*|V| + |E|), the ideal Fibonacci Heap version is in O(|V|log|V|+|E|)

    print distances


def DagSSSP(graph, source):

    # assume the graph is preprocessed like this
    vertices = {u for (u, v) in graph.keys()} | {v for (u, v) in graph.keys()}
    neighbors = {u: {v for (_, v) in graph if _ == u} for u in vertices}

    # up to here zero cost

    # stolen from others
    # https://algocoding.wordpress.com/2015/04/05/topological-sorting-python/
    from collections import deque
    def kahn_topsort(neighbors):

        # O(|V|+|E|)
        in_degree = { u : 0 for u in neighbors }     # determine in-degree
        for u in neighbors:                          # of each node
            for v in neighbors[u]:
                in_degree[v] += 1

        # O(|V|)
        Q = deque()                     # collect nodes with zero in-degree
        for u in in_degree:
            if in_degree[u] == 0:
                Q.appendleft(u)

        L = [] # list for order of nodes

        # O(|V|+|E|)
        while Q:
            u = Q.pop()              # choose node of zero in-degree
            L.append(u)          # and 'remove' it from graph
            for v in neighbors[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    Q.appendleft(v)

        if len(L) == len(neighbors):
            return L
        else:                    # if there is a cycle,
            raise ValueError, "cycle detected"

    distances = init_distances(vertices, source) # O(|V|)
    topsort = kahn_topsort(neighbors) # O(|V|+|E|)

    # up to here O(|V|+|E|) cost

    # Basically Dijksta just with a cheaper vertex order which is only
    # applicable to Directed Acyclic Graphs. Note that Dynamic Programms
    # like cell updates in the Smith Waterman algorithm are executed in
    # row-major order which is already a topsort of the corresponding DAG
    for u in topsort: # O(|V|)
        for v in neighbors[u]: # O(|E|) overall since each edge visited once
            relax(u, v, graph[(u, v)], distances) # O(1) decrease key

    # O(|V| + |E|)

    print distances



graph = {}
graph[(0, 1)] = 2
graph[(0, 2)] = 5
graph[(1, 2)] = 1
graph[(2, 3)] = 2
graph[(0, 3)] = 3
# introduce a cycle
#graph[(3, 0)] = 0

BellmanFord(graph, 0)
DummyDijkstra(graph, 0)
DagSSSP(graph, 0)
