# tests/test_bmssp.py
import pytest
from core.graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.bmssp import bmssp_main

def make_small_graph():
    # simple directed graph
    # edges: 0->1(1), 0->2(4), 1->2(2), 2->3(1)
    edges = [
        (0,1,1.0),
        (0,2,4.0),
        (1,2,2.0),
        (2,3,1.0)
    ]
    g = Graph.from_edge_list(4, edges)
    return g

def test_bmssp_matches_dijkstra():
    g = make_small_graph()
    dist_dij, prev = dijkstra(g, 0)
    dist_bm, pred, info = bmssp_main(g, 0)
    for v in g.nodes:
        a = dist_dij[v]
        b = dist_bm[v]
        assert abs(a - b) < 1e-9
