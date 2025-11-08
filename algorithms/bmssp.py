# algorithms/bmssp.py
"""
BMSSP implementation with two modes:
 - mode="safe": final multi-source Dijkstra is run to guarantee optimality (current safe behavior)
 - mode="fast": skips final Dijkstra to measure raw BMSSP work (paper-like, often faster on large graphs)

Use mode parameter from bmssp_main(...) or pass from benchmark runner.
"""

import math
import time
from typing import Set, Dict, Tuple, List
from .pivot import find_pivots
from .dstructs import PartialSortingDS
from .dijkstra import mini_dijkstra
import heapq

def BMSSP_recursive(graph, l: int, B: float, S: Set[int], distances: Dict[int, float],
                     predecessors: Dict[int, int], k: int, t: int):
    """
    Same as earlier: performs recursion, updates distances and predecessors in-place.
    Returns (B_prime, U_set)
    """
    if l == 0:
        U_total = set()
        Bprime_min = B
        for s in S:
            Bp, U = mini_dijkstra(graph, s, B, distances, predecessors, k)
            U_total.update(U)
            Bprime_min = min(Bprime_min, Bp)
        return Bprime_min, U_total

    P, W = find_pivots(graph, distances, S, B, k)
    M = max(1, 2 * (l - 1) * t)
    D = PartialSortingDS(M, B)

    for x in P:
        val = distances.get(x, float('inf'))
        if val < float('inf'):
            D.insert((x, val))

    B0_prime = min([distances.get(x, float('inf')) for x in P]) if P else B
    U = set()

    safety_iter = 0
    max_iter = max(10000, len(P) * 10 + 1000)

    while not D.is_empty() and len(U) < max(1, (k * (2 ** l) * t)) and safety_iter < max_iter:
        safety_iter += 1
        keys, separator = D.pull()
        if not keys:
            break
        Si = set(keys)
        Bi = separator

        Bi_prime, Ui = BMSSP_recursive(graph, l - 1, Bi, Si, distances, predecessors, k, t)
        U.update(Ui)

        K = []
        for u in Ui:
            du = distances.get(u, float('inf'))
            if du == float('inf'):
                continue
            for v, w in graph.get_neighbors(u):
                newd = du + w
                if newd < distances.get(v, float('inf')):
                    distances[v] = newd
                    predecessors[v] = u
                    if Bi <= newd < B:
                        D.insert((v, newd))
                    elif Bi_prime <= newd < Bi:
                        K.append((v, newd))

        batch = []
        for node in Si:
            val = distances.get(node, float('inf'))
            if Bi_prime <= val < Bi:
                batch.append((node, val))
        if K:
            batch.extend(K)
        if batch:
            D.batch_prepend(batch)

        if D.is_empty():
            return min(Bi_prime, B), U
        if len(U) >= max(1, (k * (2 ** l) * t)):
            return Bi_prime, U

    for x in W:
        if distances.get(x, float('inf')) < B:
            U.add(x)

    return B, U

def _final_multi_source_dijkstra(graph, distances: Dict[int, float], predecessors: Dict[int, int]):
    """
    Multi-source Dijkstra seeded with current finite distances to guarantee optimality.
    """
    heap = []
    for v, d in distances.items():
        if d < float('inf'):
            heapq.heappush(heap, (d, v))

    while heap:
        d, u = heapq.heappop(heap)
        if d > distances.get(u, float('inf')):
            continue
        for v, w in graph.get_neighbors(u):
            nd = d + w
            if nd < distances.get(v, float('inf')):
                distances[v] = nd
                predecessors[v] = u
                heapq.heappush(heap, (nd, v))

def bmssp_main(graph, source: int, mode: str = "safe"):
    """
    Top-level BMSSP caller.
    mode: "safe" | "fast"
    Returns (distances, predecessors, info)
    """
    assert mode in ("safe", "fast"), "mode must be 'safe' or 'fast'"

    n = max(1, graph.num_nodes)
    k = max(1, int(max(1, math.floor((math.log(n + 1)) ** (1/3)))))
    t = max(1, int(max(1, math.floor((math.log(n + 1)) ** (2/3)))))
    L = max(0, int(math.ceil(math.log(n + 1) / max(1, t))))

    distances = {v: float('inf') for v in graph.nodes}
    predecessors = {v: None for v in graph.nodes}
    distances[source] = 0.0

    start_time = time.time()
    try:
        Bp, U = BMSSP_recursive(graph, L, float('inf'), {source}, distances, predecessors, k, t)
    except RecursionError:
        Bp, U = BMSSP_recursive(graph, max(0, L - 1), float('inf'), {source}, distances, predecessors, k, t)

    # Conditional final Dijkstra
    if mode == "safe":
        _final_multi_source_dijkstra(graph, distances, predecessors)
    # else fast: skip final pass to measure BMSSP raw performance

    total_time = time.time() - start_time
    return distances, predecessors, {"time": total_time, "B_final": Bp, "mode": mode}
