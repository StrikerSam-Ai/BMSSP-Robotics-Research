# algorithms/pivot.py
"""
FindPivots implementation (practical).
Per Lemma 3.2: given bound B and set S, perform k-step relaxations (bounded Bellman-Ford-like)
to grow W. If W becomes large (> k|S|) return P = S. Otherwise, build forest among W using predecessor
relationships and select pivots P as roots of subtrees with size >= k.

This version is careful to update distances in-place and maintain predecessors for forest building.
"""

from collections import defaultdict
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
    # predecessors discovered during these k rounds
    pred = {}

    for _ in range(k):
        new_frontier = set()
        for u in list(frontier):
            d_u = distances.get(u, float('inf'))
            # if u is already at/above B then it cannot help
            if d_u >= B:
                continue
            for v, w in graph.get_neighbors(u):
                newd = d_u + w
                # only consider relaxations strictly improving known distance and below B
                if newd < distances.get(v, float('inf')) and newd < B:
                    distances[v] = newd
                    pred[v] = u
                    new_frontier.add(v)
                    W.add(v)
        frontier = new_frontier
        if len(W) > k * max(1, len(S)):
            # early exit: workload large, return P = S
            return set(S), W

    # If we are here, |W| <= k|S|. Build forest F over W using pred to find subtree sizes.
    children = defaultdict(list)
    has_parent = set()
    for child, parent in pred.items():
        if parent in W:
            children[parent].append(child)
            has_parent.add(child)

    # determine potential roots: nodes in S that are in W (and have children or not)
    roots = set()
    for s in S:
        if s in W:
            roots.add(s)

    # also any node in W without a parent recorded may be treated as a root
    for node in W:
        if node not in has_parent and node not in roots:
            roots.add(node)

    # compute subtree sizes via DFS (memoized)
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

    # If no pivots found, fallback to returning S to be conservative
    if not P:
        P = set(S)

    return P, W
