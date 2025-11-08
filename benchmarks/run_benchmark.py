# benchmarks/run_benchmark.py
"""
Benchmark runner to compare Dijkstra vs BMSSP (safe / fast modes).
Usage:
    python -m benchmarks.run_benchmark --n 2000 --deg 2 --mode safe
"""

import time
import random
import argparse
from typing import List, Tuple

from core.graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.bmssp import bmssp_main

def generate_random_sparse_graph(n: int, avg_deg: int = 2, weight_range=(1.0, 10.0)):
    edges = []
    for u in range(n):
        # simple uniform degree
        neighbors = set()
        while len(neighbors) < avg_deg:
            v = random.randrange(0, n)
            if v == u:
                continue
            neighbors.add(v)
        for v in neighbors:
            w = random.uniform(weight_range[0], weight_range[1])
            edges.append((u, v, w))
    return edges

def run_demo(n=2000, avg_deg=2, mode="safe"):
    # build graph
    edges = []
    for u in range(n):
        for _ in range(avg_deg):
            v = random.randrange(0, n)
            if v == u:
                continue
            edges.append((u, v, random.uniform(1.0, 10.0)))
    graph = Graph.from_edge_list(n, edges)
    source = 0

    t0 = time.time()
    dist_dij, prev = dijkstra(graph, source)
    t_dij = time.time() - t0
    print(f"Dijkstra time: {t_dij:.4f}s")

    t0 = time.time()
    dist_bm, pred, info = bmssp_main(graph, source, mode=mode)
    t_bm = time.time() - t0
    print(f"BMSSP time ({mode}): {t_bm:.4f}s")

    mismatch = 0
    for v in graph.nodes:
        a = dist_dij.get(v, float('inf'))
        b = dist_bm.get(v, float('inf'))
        if abs(a - b) > 1e-6 and not (a == float('inf') and b == float('inf')):
            mismatch += 1

    print(f"Mismatch count: {mismatch} out of {graph.num_nodes}")
    return {"n": n, "dijkstra": t_dij, "bmssp": t_bm, "mismatch": mismatch, "mode": mode}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=2000)
    parser.add_argument("--deg", type=int, default=2)
    parser.add_argument("--mode", type=str, default="safe", choices=["safe", "fast"])
    args = parser.parse_args()
    random.seed(42)
    print(run_demo(args.n, args.deg, mode=args.mode))
