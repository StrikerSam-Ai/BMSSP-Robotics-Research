# BMSSP-Robotics-Research

Research-grade implementation and benchmarking framework for the BMSSP algorithm
(Broken Sorting Barrier Single-Source Shortest Path) and comparisons with classical Dijkstra,
with an aim to apply to robotics path planning (warehouse AGV scenarios).

## Repository structure

- `algorithms/` : core algorithms (dijkstra, barrier_breaker, bmssp, helpers)
- `core/` : graph primitives and loaders
- `benchmarks/` : scripts to run performance experiments
- `simulation/` : robotics simulation (to add)
- `tests/` : unit tests

## Quick start

1. Create a Python virtual environment and install requirements:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
