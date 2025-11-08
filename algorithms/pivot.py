# algorithms/pivot.py
"""
Robust FindPivots implementation.
Per Lemma 3.2: given bound B and set S, perform k-step relaxations (bounded Bellman-Ford-like)
to grow W. If W becomes large (> k|S|) return P = S. Otherwise, build forest among W using predecessor
relationships and select pivots P as roots of subtrees with size >= k.

This implementation updates distances in-place and returns (P, W).
"""

from collections import defaultdict
from typing import Set, Dict, Tuple

def find_pivots(graph, distances: Dict[int, float], S: Set[int], B: float, k: int):
    W = set(S)
    frontier = set(S)
    pred = {}

    for _ in range(max(1, k)):
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
        if len(W) > k * max(1, len(S)):
            return set(S), W

    # Build children map for forest
    children = defaultdict(list)
    has_parent = set()
    for child, parent in pred.items():
        if parent in W:
            children[parent].append(child)
            has_parent.add(child)

    # roots: nodes in S that are in W, plus any W node that has no recorded parent
    roots = set()
    for s in S:
        if s in W:
            roots.add(s)
    for node in W:
        if node not in has_parent and node not in roots:
            roots.add(node)

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

    P = set()
    for s in S:
        if s in subtree_size and subtree_size[s] >= k:
            P.add(s)

    if not P:
        P = set(S)
    return P, W
