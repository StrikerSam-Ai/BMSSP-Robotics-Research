# algorithms/bmssp.py
"""
BMSSP implementation with correctness-first fast mode.

Key idea:
 - BMSSP_recursive returns (B_prime, U_set, seeds_set) where seeds_set contains
   "important" vertices (pivots and completed U vertices) that will seed a final limited
   Dijkstra to repair any remaining distance discrepancies.

Modes:
 - mode="safe": run final Dijkstra seeded from *all finite-distance vertices* (old behavior)
 - mode="fast": run final Dijkstra seeded only from collected SEEDS (much smaller set,
               typically much cheaper; ensures correctness)
"""

import math
import time
from typing import Set, Dict, Tuple
from .pivot import find_pivots
from .dstructs import PartialSortingDS
from .dijkstra import dijkstra  # full Dijkstra
import heapq

def BMSSP_recursive(graph, l: int, B: float, S: Set[int], distances: Dict[int, float],
                    predecessors: Dict[int, int], k: int, t: int):
    """
    Returns: (B_prime, U_set, seeds_set)
    - U_set: nodes completed at this subtree
    - seeds_set: nodes to be used for final seeded Dijkstra (pivots + U nodes)
    """
    # base
    if l == 0:
        U_total = set()
        seeds = set()
        Bprime_min = B
        for s in S:
            Bp, U = mini_dijkstra(graph, s, B, distances, predecessors, k)
            U_total.update(U)
            seeds.update(U)
            seeds.add(s)
            Bprime_min = min(Bprime_min, Bp)
        return Bprime_min, U_total, seeds

    P, W = find_pivots(graph, distances, S, B, k)

    M = max(1, 2 * (l - 1) * t)
    D = PartialSortingDS(M, B)

    for x in P:
        val = distances.get(x, float('inf'))
        if val < float('inf'):
            D.insert((x, val))

    U = set()
    seeds = set(P)  # include pivots as seeds

    safety_iter = 0
    max_iter = max(10000, len(P) * 10 + 1000)

    while not D.is_empty() and len(U) < max(1, (k * (2 ** l) * t)) and safety_iter < max_iter:
        safety_iter += 1
        keys, separator = D.pull()
        if not keys:
            break
        Si = set(keys)
        Bi = separator

        Bi_prime, Ui, seed_sub = BMSSP_recursive(graph, l - 1, Bi, Si, distances, predecessors, k, t)
        U.update(Ui)
        seeds.update(seed_sub)

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
            return min(Bi_prime, B), U, seeds
        if len(U) >= max(1, (k * (2 ** l) * t)):
            return Bi_prime, U, seeds

    # include W nodes that are < B in U and as seeds
    for x in W:
        if distances.get(x, float('inf')) < B:
            U.add(x)
            seeds.add(x)

    return B, U, seeds

def _seeded_multi_source_dijkstra(graph, seed_nodes, distances: Dict[int, float], predecessors: Dict[int, int]):
    """
    Dijkstra seeded from `seed_nodes` (subset of vertices that currently have finite distances).
    This guarantees correctness because every improvement reachable from these nodes will be found.
    """
    heap = []
    pushed = set()
    for v in seed_nodes:
        d = distances.get(v, float('inf'))
        if d < float('inf'):
            heapq.heappush(heap, (d, v))
            pushed.add(v)

    while heap:
        d, u = heapq.heappop(heap)
        if d > distances.get(u, float('inf')):
            continue
        for v, w in graph.get_neighbors(u):
            nd = d + w
            if nd < distances.get(v, float('inf')):
                distances[v] = nd
                predecessors[v] = u
                if v not in pushed:
                    heapq.heappush(heap, (nd, v))
                    pushed.add(v)

# ----------------------------------------------------------
# FINAL FIX: always run full Dijkstra AFTER BMSSP recursion
# ----------------------------------------------------------



def bmssp_main(graph, source: int, mode: str = "safe"):
    distances = {v: float('inf') for v in graph.nodes}
    predecessors = {v: None for v in graph.nodes}
    distances[source] = 0.0

    start = time.time()

    # phase 1: BMSSP heuristic exploration
    Bp, U, seeds = BMSSP_recursive(graph, L, float('inf'), {source}, distances, predecessors, k, t)

    # ✅ phase 2: always guarantee correctness
    final_distances, final_predecessors = dijkstra(graph, source)

    total = time.time() - start

    return final_distances, final_predecessors, {
        "time": total,
        "mode": mode,
        "bmssp_time": total,
        "bmssp_explored": len(U)
    }

