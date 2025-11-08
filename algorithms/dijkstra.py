# algorithms/dijkstra.py
"""
Dijkstra baseline and the 'mini_dijkstra' used as base-case for BMSSP.
"""

import heapq
from typing import Tuple, Dict, Set, List

def dijkstra(graph, source: int):
    dist = {v: float('inf') for v in graph.nodes}
    prev = {v: None for v in graph.nodes}
    dist[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.get_neighbors(u):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev

def mini_dijkstra(graph, source: int, B: float, distances: Dict[int, float],
                  predecessors: Dict[int, int], k: int) -> Tuple[float, Set[int]]:
    """
    Run a Dijkstra-like expansion from source x up to (k+1) nodes or until no more nodes found within B.
    Returns (B_prime, U_set) with U_set being nodes discovered with d < B_prime and all complete.
    """
    # Use local heap seeded with current known distance for source
    import heapq
    heap = []
    seen = set()
    U0 = set()
    # seed
    initial = distances.get(source, float('inf'))
    heapq.heappush(heap, (initial, source))
    while heap and len(U0) < (k + 1):
        d, u = heapq.heappop(heap)
        if d > distances.get(u, float('inf')):
            continue
        if d >= B:
            break
        if u in U0:
            continue
        U0.add(u)
        for v, w in graph.get_neighbors(u):
            nd = d + w
            if nd < distances.get(v, float('inf')) and nd < B:
                distances[v] = nd
                predecessors[v] = u
                heapq.heappush(heap, (nd, v))
    if len(U0) <= k:
        return B, U0
    else:
        Bprime = max(distances[v] for v in U0)
        # U returned should be {v in U0 : d(v) < Bprime}
        U = set(v for v in U0 if distances[v] < Bprime)
        return Bprime, U
