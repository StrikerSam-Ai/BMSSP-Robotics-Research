# algorithms/dstructs.py
"""
Practical implementation of the partial-sorting data structure D described in the BMSSP paper.
Supports:
 - Insert(key, value)
 - BatchPrepend(list_of_pairs)
 - Pull() -> (subset_keys, separator_value)

Design choices for practicality:
 - D0: deque of batches (each batch is a list sorted by value, prepended)
 - D1: list of blocks; each block is a list kept roughly size M (unsorted inside),
       with an index of block upper bounds for fast location using bisect.
 - For Pull we collect up to M smallest elements by merging prefix blocks from D0 and D1.
 - This is not a full theoretical implementation but follows required semantics and
   is efficient for medium-scale graphs (50k nodes) as requested.
"""

import bisect
import heapq
from collections import deque
from typing import List, Tuple, Dict, Any, Optional

class Block:
    def __init__(self, items: List[Tuple[int, float]] = None):
        # items: list of (key, value)
        self.items = items or []
        # maintain an upper bound value for block
        self.update_bound()
    
    def update_bound(self):
        if not self.items:
            self.ub = float('inf')
        else:
            # ub is max value in items
            self.ub = max(v for _, v in self.items)
    
    def push(self, pair: Tuple[int, float]):
        self.items.append(pair)
        if pair[1] > self.ub:
            self.ub = pair[1]
    
    def extend(self, pairs: List[Tuple[int, float]]):
        self.items.extend(pairs)
        if pairs:
            self.ub = max(self.ub, max(v for _, v in pairs))
    
    def pop_all(self) -> List[Tuple[int, float]]:
        items = self.items
        self.items = []
        self.ub = float('inf')
        return items


