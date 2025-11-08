# algorithms/bmssp.py
"""
BMSSP implementation (practical and faithful to paper structure).
Warning: This is a practical implementation aimed at correctness and medium-scale performance.
It follows the BMSSP recursive pattern: BMSSP(l, B, S) with FindPivots and Data structure D.
"""

import math
import time
from typing import Set, Dict, Tuple, List
from .pivot import find_pivots
from .dstructs import PartialSortingDS
from .dijkstra import mini_dijkstra  # base-case helper; implement in dijkstra.py
from collections import defaultdict

def BMSSP_recursive(graph, l: int, B: float, S: Set[int], distances: Dict[int, float],
                     predecessors: Dict[int, int], k: int, t: int):
    """
    Returns (B_prime, U_set). Updates distances and predecessors in place.
    - graph: core graph object with get_neighbors(u) -> list of (v,w)
    """
    # Base case l == 0: run mini Dijkstra from the single source in S (S should be singleton)
    if l == 0:
        # Expect S size = 1
        assert len(S) == 1, "Base case expects singleton S"
        s = next(iter(S))
        Bp, U = mini_dijkstra(graph, s, B, distances, predecessors, k)
        return Bp, U
    
    # Step 1: Find pivots
    P, W = find_pivots(graph, distances, S, B, k)
    # Initialize D with M = 2*(l-1)*t
    M = max(1, 2 * (l - 1) * t)
    D = PartialSortingDS(M, B)
    # insert P into D with their current distance
    for x in P:
        val = distances.get(x, float('inf'))
        if val < float('inf'):
            D.insert((x, val))
    B0_prime = min([distances.get(x, float('inf')) for x in P]) if P else B
    U = set()
    # Iterations: pull, recursive call, relax, insert / batch-prepend
    while len(U) < (k * (2 ** l) * t) and not D.is_empty():
        keys, separator = D.pull()
        if not keys:
            break
        # Prepare Si and Bi for recursive calls: Si is set of keys
        Si = set(keys)
        Bi = separator
        # recursively call BMSSP on level l-1 for Si
        Bi_prime, Ui = BMSSP_recursive(graph, l - 1, Bi, Si, distances, predecessors, k, t)
        U.update(Ui)
        # Relax edges from Ui
        K = []
        for u in Ui:
            du = distances.get(u, float('inf'))
            if du >= B:
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
        # Batch prepend K and those Si with value in [Bi_prime, Bi)
        # Build list for batch prepend
        batch = []
        for node in Si:
            val = distances.get(node, float('inf'))
            if Bi_prime <= val < Bi:
                batch.append((node, val))
        batch.extend(K)
        if batch:
            D.batch_prepend(batch)
        # Check termination conditions
        if D.is_empty():
            return min(Bi_prime, B), U
        if len(U) >= (k * (2 ** l) * t):
            return Bi_prime, U
    # finalize: include W nodes with distance < B'
    B_final = B
    for x in W:
        if distances.get(x, float('inf')) < B_final:
            U.add(x)
    return B_final, U


