# BMSSP — Bidirectional Multi-Seed Shortest Path
A fast, practical alternative to Dijkstra for large sparse graphs with grid/robotics integration.

---
# BMSSP — Bidirectional Multi-Seed Shortest Path (Final)

A focused case-study implementation and benchmark suite for BMSSP — a bidirectional, multi-seed shortest-path approach designed for large, sparse graphs. This repository contains two BMSSP variants (`safe` and `fast`), a Dijkstra baseline implementation, benchmarking utilities, grid visualization, and experimental CoppeliaSim integration for robot-following experiments.

---

## Table of contents

- Summary
- Parent paper (reference)
- Quick start (install & setup)
- Examples (programmatic + visualization)
- Running benchmarks & tests
- Project layout
- Design & process
- Contribution / Author (case study)
- How to cite
- Tests & quality
- Troubleshooting & notes
- License

---

## Summary

BMSSP (Bidirectional Multi-Seed Shortest Path) uses multi-seed exploration and bidirectional frontier merging with pruning heuristics (graph "freezing") to reduce the search space on large sparse graphs. The repository includes:

- `safe` variant: conservative, correctness-first implementation
- `fast` variant: more aggressive pruning for better runtime on large graphs
- Baseline Dijkstra implementation for correctness and timing comparisons
- Benchmark harness for measuring performance over different graph sizes and degrees
- Grid visualization (pygame) and lightweight robotics integration scaffolding for CoppeliaSim

This repository is a case study and reimplementation inspired by recent algorithmic work (see Parent paper below).

---

## Parent paper (reference)

This repository is a case study inspired by the following paper:

- Duan, Ran; Mao, Jiayi; Mao, Xiao; Shu, Xinkai; Yin, Longhui — "Breaking the Sorting Barrier for Directed Single‐Source Shortest Paths", arXiv preprint arXiv:2504.17033v2 (2025).

arXiv: https://arxiv.org/abs/2504.17033v2
DOI: 10.48550/arXiv.2504.17033

BibTeX:

```bibtex
@article{duan2025breaking,
  title        = {Breaking the Sorting Barrier for Directed Single‐Source Shortest Paths},
  author       = {Duan, Ran and Mao, Jiayi and Mao, Xiao and Shu, Xinkai and Yin, Longhui},
  journal      = {arXiv preprint arXiv:2504.17033v2},
  year         = {2025},
  doi          = {10.48550/arXiv.2504.17033},
  url          = {https://arxiv.org/abs/2504.1704v2},
  note         = {Revised version v2, July 2025}
}
```

---

## Quick start — install & setup

Prerequisites
- Python 3.8+ (3.10+ recommended)
- pip

1) Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```powershell
pip install -r requirements.txt
```

Notes:
- `requirements.txt` includes the minimal deps used here (pygame, pytest). If you plan to use the CoppeliaSim scripts, you may need additional packages (ZeroMQ, the CoppeliaSim remote API client). See the Troubleshooting section below.

---

## Examples

1) Minimal programmatic example (python REPL or script):

```python
from core.graph import Graph
from algorithms.bmssp import bmssp_main

g = Graph(num_nodes=6)
# Example edges (undirected or directed depending on Graph):
g.add_edge(0, 1, 1)
g.add_edge(1, 2, 2)
g.add_edge(0, 3, 4)
g.add_edge(3, 4, 1)
g.add_edge(4, 2, 1)

dist, preds, info = bmssp_main(g, source=0, mode="safe")
print("distances:", dist)
print("info:", info)
```

2) Visualization (grid world):

```powershell
python simulation/visualize.py
```

The visualizer shows free cells, obstacles and the BMSSP-computed shortest path on a grid. Use this for quick debugging and demonstrations.

---

## Running benchmarks & tests

Unit tests (pytest):

```powershell
python -m pytest -q
```

Benchmark runner (compare BMSSP variants to Dijkstra):

```powershell
python -m benchmarks.run_benchmark --n 30000 --deg 4 --mode safe
python -m benchmarks.run_benchmark --n 30000 --deg 4 --mode fast
```

Flags:
- `--n` — number of nodes
- `--deg` — average outgoing degree
- `--mode` — `safe` or `fast`

Observations (from experiments in `docs/`): on large sparse graphs BMSSP showed modest improvements vs Dijkstra (10–12% in our measured cases) while returning matching shortest paths in our test-suite.

---

## Project layout

- `algorithms/` — `bmssp.py` (BMSSP implementations), `dijkstra.py` (baseline)
- `core/` — `graph.py` lightweight adjacency list graph
- `benchmarks/` — `run_benchmark.py` performance harness
- `simulation/` — `visualize.py`, `robot_sim.py` grid visualization & sim
- `coppeliasim_integration/` — CoppeliaSim integration scripts
- `docs/` — design notes and benchmark summaries (e.g., `bmssp_summary.md`)
- `tests/` — unit tests (e.g., `tests/test_bmssp.py`)

---

## Design and process (brief)

1. Research & design
	- Built on bidirectional search techniques and modern shortest-path improvements.
	- Introduced multi-seeding to start promising simultaneous frontiers and prune nodes unlikely to be in the final path.
2. Implementation
	- `safe` variant preserves correctness guarantees through conservative merging and checks.
	- `fast` variant uses more aggressive pruning heuristics to reduce runtime on large sparse graphs.
3. Validation
	- Extensive comparison against Dijkstra across random sparse graphs. Test-suite reports 0 mismatches for the tested inputs.
4. Benchmarking
	- `benchmarks/run_benchmark.py` measures runtime vs graph size/degree. See `docs/` for recorded results.

---

## Contribution / Author (case study)

Author: Shashwat Mishra

This repository is a case study reimplementation inspired by the Duan et al. (2025) paper listed above. The code and experiments are the author's practical exploration of BMSSP-style ideas and comparisons to established baselines.

Contribution summary (this repo):
- Reimplemented BMSSP algorithm (safe & fast variants) for experimentation
- Implemented a Dijkstra baseline for correctness checks
- Built the benchmarking harness and executed comparative experiments
- Implemented grid visualization and CoppeliaSim integration scaffolding for robot-following experiments

If you'd like a different tone (e.g., academic phrasing) or to add specific experiment details (datasets, exact machine specs), tell me and I'll update this section.

---

## How to cite

If you use this repository, cite the parent paper and optionally this repository. Example repo citation (replace with official citation if needed):

Shashwat Mishra — BMSSP: Bidirectional Multi-Seed Shortest Path. Repository: StrikerSam-Ai/BMSSP-Robotics-Research

And cite Duan et al. (2025) using the BibTeX in the Parent paper section.

---

## Tests & quality

- Unit tests are under `tests/` (run with `pytest`).
- When changing algorithm code add tests covering correctness vs Dijkstra and edge-cases (disconnected graphs, trivial graphs, single-node graphs, zero-weight edges if applicable).

Quality gates to run locally:

```powershell
# create env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
```

---

## Troubleshooting & notes

- Pygame: on some systems you may need system SDL libraries installed. On Windows pip wheels are usually sufficient.
- CoppeliaSim integration: requires a running CoppeliaSim instance with the remote API server enabled; update host/port in the scripts as needed.
- Large benchmarks: increase process memory or run on a machine with more RAM if `--n` is very large.

If you hit a specific error, paste the traceback and I will help diagnose.

---

## Next steps (suggested)

- Add an `examples/` folder with small runnable scripts demonstrating BMSSP on grid and graph inputs.
- Pin exact dependency versions in `requirements.txt` used for published experiments.
- Add machine specs and full benchmark data in `docs/` for reproducibility.

---

## License

See `LICENSE` in the repository root.

---
