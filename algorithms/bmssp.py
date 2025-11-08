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


