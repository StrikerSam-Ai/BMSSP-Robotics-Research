# BMSSP — Bidirectional Multi-Seed Shortest Path
A fast, practical alternative to Dijkstra for large sparse graphs with grid/robotics integration.

---

## Summary
BMSSP (Bidirectional Multi-Seed Shortest Path) is a graph search approach designed to speed up shortest-path queries on large, sparse graphs. It combines multi-seed exploration, bidirectional growth, and pruning (graph "freezing") to reduce the explored search space while retaining correctness (the repository contains both a conservative `safe` variant and a higher-performance `fast` variant).

This repository contains implementations, benchmarks vs Dijkstra, grid visualization, and preliminary robotics integration (Pioneer P3DX via CoppeliaSim remote API).

---

## Parent paper
This repository is a case study and implementation inspired by the following paper (please replace or extend with any other references you want shown):

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
	url          = {https://arxiv.org/abs/2504.17033v2},
	note         = {Revised version v2, July 2025}
}
```

---

## Quick start — requirements & install
Prerequisites:
- Python 3.8+ (3.10+ recommended)
- pip

Install the minimal dependencies (virtualenv recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # if present; otherwise install pygame for visualization
pip install pygame
```

If you don't have a `requirements.txt` in the repo, install the packages you need for the parts you want to run (benchmarks and algorithm are pure Python; visualization needs pygame; CoppeliaSim integration requires the CoppeliaSim remote API client).

---

## Run the code

1) Run unit tests

```powershell
python -m pytest -q
```

2) Run benchmarks

The benchmark runner compares BMSSP (safe/fast) to Dijkstra on synthetic graphs.

```powershell
python -m benchmarks.run_benchmark --n 30000 --deg 4 --mode safe
python -m benchmarks.run_benchmark --n 30000 --deg 4 --mode fast
```

Flags:
- `--n`  — total number of nodes
- `--deg` — average outgoing degree per node
- `--mode` — `safe` or `fast`

3) Use BMSSP programmatically (graph API)

```python
from core.graph import Graph
from algorithms.bmssp import bmssp_main

g = Graph(num_nodes=10000)
# g.add_edge(u, v, weight)
dist, preds, info = bmssp_main(g, source=0, mode="safe")
```

4) Visualization (grid world)

Run the simple grid visualizer (pygame). The script renders a grid, obstacles and the BMSSP-computed shortest path.

```powershell
python simulation/visualize.py
```

5) Robotics simulation (CoppeliaSim)

Files under `coppeliasim_integration/` show how a computed path can be sent to a Pioneer P3DX in CoppeliaSim using the Remote API. This is integration code and may require a running copy of CoppeliaSim with the remote API server enabled.

Key notes:
- The CoppeliaSim integration is experimental. You may need to update host/port and API client dependencies.
- Use `bmssp_pioneer_follow.py` or `bmssp_pioneer_zmq.py` as starting points.

---

## Project layout

- `algorithms/` — `bmssp.py` (BMSSP implementations: `safe` & `fast`), `dijkstra.py` baseline, helpers
- `core/` — `graph.py` lightweight adjacency-list graph API
- `benchmarks/` — `run_benchmark.py` performance harness
- `simulation/` — `visualize.py`, `robot_sim.py` grid visualization & sim
- `coppeliasim_integration/` — scripts to talk to CoppeliaSim (P3DX)
- `docs/` — design notes and summary (`bmssp_summary.md`)
- `tests/` — unit tests (e.g., `tests/test_bmssp.py`)

---

## Design and process (brief)

1. Research & design: built on bidirectional search ideas. Introduced multi-seeding to start exploration from multiple promising seeds, then merged frontiers while pruning nodes unlikely to contribute to the optimal path.
2. Implementation: two variants: `safe` maintains conservative checks to guarantee correctness; `fast` uses additional pruning heuristics to reduce runtime (empirically still correct for the test-suite used).
3. Validation: compared results against a standard Dijkstra implementation across multiple random sparse graphs. After final fixes, test-suite shows 0 mismatches vs Dijkstra.
4. Benchmarking: `benchmarks/run_benchmark.py` measures runtime across node counts and degrees; results are summarized in `docs/` and the README.
5. Visualization & simulation: grid-based visualization (pygame) for debugging, and experimental CoppeliaSim integration for robot-following pipelines.

---

## Contribution / Author
Author: Shashwat Mishra

Note: this repository is a case study and reimplementation inspired by the paper cited above (Duan et al., 2025). The work here implements and evaluates BMSSP as a practical experiment and benchmark against standard Dijkstra.

Contribution summary (this repo is a case study and implementation):
- Implemented BMSSP algorithm (safe & fast variants) as a reimplementation / case study
- Re-implemented a reference Dijkstra baseline used for correctness checks
- Built the benchmarking harness and ran comparative experiments validating BMSSP vs Dijkstra
- Implemented grid visualization and CoppeliaSim integration scaffolding for robot-following experiments

If you want any of these bullets changed (tone, scope, or to include specific datasets/experiments), tell me and I will update the text.

---

## How to cite / parent work
If you use this algorithm or codebase, please cite the parent paper (add link above) and mention the repository.

Suggested short citation (replace with official citation once paper link is available):

Shashwat Mishra — BMSSP: Bidirectional Multi-Seed Shortest Path. (link/DOI). Repository: StrikerSam-Ai/BMSSP-Robotics-Research

---

## Tests & quality
- Unit tests live in `tests/` and can be run with `pytest`.
- If you add or change algorithms, update or add tests to cover correctness vs Dijkstra and key edge-cases (disconnected graphs, negative/zero weights if applicable, single-node graphs).

---

## License
This repository is released under the terms in `LICENSE`.

---