# benchmarks/run_benchmark.py
"""
Simple benchmark runner.
Generates a random directed sparse graph (edge list), writes to edge file format (if desired),
and runs Dijkstra vs BMSSP, measuring wall-clock time and path equality.

Note: for large graphs (50k nodes) it's recommended to run on Kaggle / high-ram machine.
"""

import time
import random
import os
import argparse
from collections import defaultdict
from typing import List, Tuple

# assume core.graph.Graph exists with load_edgelist and from_edges constructor
from core.graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.bmssp import bmssp_main

def generate_random_sparse_graph(n: int, avg_deg: int = 2, weight_range=(1.0, 10.0)):
    edges = []
    for u in range(n):
        deg = random.poissonvariate(avg_deg) if False else avg_deg
        # connect to random neighbors (avoid self loops)
        neighbors = set()
        while len(neighbors) < deg:
            v = random.randrange(0, n)
            if v == u:
                continue
            neighbors.add(v)
        for v in neighbors:
            w = random.uniform(weight_range[0], weight_range[1])
            edges.append((u, v, w))
    return edges

def run_small_demo(n=1000, avg_deg=2):
    # quick graph generator using uniform degree
    edges = []
    for u in range(n):
        for _ in range(avg_deg):
            v = random.randrange(0, n)
            if v == u:
                continue
            edges.append((u, v, random.uniform(1.0, 10.0)))
    graph = Graph.from_edge_list(n, edges)
    source = 0
    # run Dijkstra
    t0 = time.time()
    dist_dij, prev = dijkstra(graph, source)
    t_dij = time.time() - t0
    print(f"Dijkstra time: {t_dij:.4f}s")
    # run BMSSP
    t0 = time.time()
    dist_bm, pred, info = bmssp_main(graph, source)
    t_bm = time.time() - t0
    print(f"BMSSP time: {t_bm:.4f}s")
    # compare correctness
    mismatch = 0
    for v in graph.nodes:
        a = dist_dij.get(v, float('inf'))
        b = dist_bm.get(v, float('inf'))
        if abs(a - b) > 1e-6 and not (a == float('inf') and b == float('inf')):
            mismatch += 1
    print(f"Mismatch count: {mismatch} out of {graph.num_nodes}")
    return {"n": n, "dijkstra": t_dij, "bmssp": t_bm, "mismatch": mismatch}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=2000)
    parser.add_argument("--deg", type=int, default=2)
    args = parser.parse_args()
    print(run_small_demo(args.n, args.deg))
