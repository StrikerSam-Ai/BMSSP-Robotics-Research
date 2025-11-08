# algorithms/pivot.py
"""
FindPivots implementation (practical).
Per Lemma 3.2: given bound B and set S, perform k-step relaxations (bounded Bellman-Ford-like)
to grow W. If W becomes large (> k|S|) return P = S. Otherwise, build forest among W using predecessor
relationships and select pivots P as roots of subtrees with size >= k.

This practical version uses local BFS-style expansion for k rounds and maintains predecessors.
"""

from collections import deque, defaultdict
from typing import Set, Tuple, Dict, List

def find_pivots(graph, distances: Dict[int, float], S: Set[int], B: float, k: int):
    """
    :param graph: Graph object with get_neighbors(u) -> list of (v, w)
    :param distances: current d̂[] dictionary (mutable: will be updated for discovered nodes)
    :param S: initial set of nodes (complete ones)
    :param B: upper bound
    :param k: number of relaxation rounds
    :return: (P, W) where P is set of pivots (subset of S) and W is set of visited nodes
    """
    # W starts with S
    W = set(S)
    frontier = set(S)
    # We'll update distances transiently but keep predecessors to build forest F
    pred = {}
    for _ in range(k):
        new_frontier = set()
        for u in list(frontier):
            d_u = distances.get(u, float('inf'))
            if d_u >= B:
                continue
            for v, w in graph.get_neighbors(u):
                newd = d_u + w
                if newd < distances.get(v, float('inf')) and newd < B:
                    distances[v] = newd
                    pred[v] = u
                    new_frontier.add(v)
                    W.add(v)
        frontier = new_frontier
        if len(W) > k * len(S):
            # early exit
            return set(S), W
    # Now when |W| <= k|S| build forest over W using pred
    # Build adjacency child lists
    children = defaultdict(list)
    roots = set()
    for v, parent in pred.items():
        if parent in W:
            children[parent].append(v)
        else:
            # If parent not in W, treat v as root (rare)
            roots.add(v)
    # Any node in S that has no parent recorded becomes a root if in W
    for s in S:
        if s in W:
            if s not in pred:
                roots.add(s)
    # Compute subtree sizes via DFS
    visited = set()
    subtree_size = {}
    def dfs(u):
        if u in subtree_size:
            return subtree_size[u]
        total = 1
        for v in children.get(u, []):
            total += dfs(v)
        subtree_size[u] = total
        return total
    for r in list(roots):
        dfs(r)
    # Select pivots among S: those roots with subtree size >= k
    P = set()
    for s in S:
        if s in subtree_size and subtree_size[s] >= k:
            P.add(s)
    # If P empty, fallback: choose S (safe)
    if not P:
        P = set(S)
    return P, W
