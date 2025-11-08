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

class PartialSortingDS:
    def __init__(self, M: int, B: float):
        # M controls block sizes and Pull batch size
        self.M = max(1, int(M))
        self.B = B
        # D0 is deque of prepended batches (each batch is a list of pairs sorted ascending by value)
        self.D0 = deque()
        # D1 is list of blocks (each block contains <= ~M items) with maintained upper bounds array
        self.D1: List[Block] = []
        self.D1_bounds: List[float] = []  # ascending list of ub per block
        # keys map to current value for quick update
        self.key_map: Dict[int, float] = {}
    
    def _rebuild_bounds(self):
        self.D1_bounds = [blk.ub for blk in self.D1]
    
    def insert(self, pair: Tuple[int, float]):
        """
        Insert a key/value pair. If key exists with larger value, update it.
        Insert to D1 (append to last block or create new).
        """
        key, value = pair
        old = self.key_map.get(key)
        if old is not None:
            # only keep smaller value
            if value >= old:
                return
            # value improved: we simply update map and append new pair (old stale entries will be ignored on pull)
        self.key_map[key] = value
        # append into last block
        if not self.D1 or len(self.D1[-1].items) >= 2 * self.M:
            # create new block
            blk = Block([pair])
            self.D1.append(blk)
            self.D1_bounds.append(blk.ub)
        else:
            self.D1[-1].push(pair)
            self.D1_bounds[-1] = self.D1[-1].ub
    
    def batch_prepend(self, pairs: List[Tuple[int, float]]):
        """
        Prepend a batch of pairs (all smaller than any existing values as stated in paper).
        We'll sort them ascending and add as a new block in D0.
        """
        if not pairs:
            return
        # Only keep best value per key among pairs
        best = {}
        for k, v in pairs:
            if k in best:
                if v < best[k]:
                    best[k] = v
            else:
                best[k] = v
        batch = [(k, best[k]) for k in best]
        batch.sort(key=lambda x: x[1])  # ascending by value
        # update key map
        for k, v in batch:
            old = self.key_map.get(k)
            if old is None or v < old:
                self.key_map[k] = v
        self.D0.appendleft(batch)
    
    def pull(self) -> Tuple[List[int], float]:
        """
        Return up to M keys associated with smallest values and an upper bound x separating them.
        If structure is empty, return ([], B).
        """
        collected: List[Tuple[int, float]] = []
        # Collect prefix of D0 up to M
        d0_acc = []
        for batch in self.D0:
            if not batch:
                continue
            for k, v in batch:
                d0_acc.append((k, v))
                if len(d0_acc) >= self.M:
                    break
            if len(d0_acc) >= self.M:
                break
        # Collect prefix of D1 blocks until we've got at least M candidates
        d1_acc = []
        total = len(d0_acc)
        idx = 0
        while total < self.M and idx < len(self.D1):
            blk = self.D1[idx]
            if not blk.items:
                idx += 1
                continue
            d1_acc.extend(blk.items)
            total = len(d0_acc) + len(d1_acc)
            idx += 1
        
        if not d0_acc and not d1_acc:
            # empty
            return ([], self.B)
        
        # Merge candidates and pick M smallest by value using heapq.nsmallest for stability
        candidates = d0_acc + d1_acc
        # Remove stale candidates (value != key_map[key])
        filtered = []
        for k, v in candidates:
            current = self.key_map.get(k)
            if current is None:
                continue
            if abs(current - v) < 1e-12:
                filtered.append((k, v))
            else:
                # keep only current (we will include current by pushing later if needed)
                filtered.append((k, current))
        # deduplicate by key keeping smallest
        best = {}
        for k, v in filtered:
            if k not in best or v < best[k]:
                best[k] = v
        cand_list = [(k, best[k]) for k in best]
        # select up to M smallest
        if len(cand_list) <= self.M:
            chosen = cand_list
        else:
            chosen = heapq.nsmallest(self.M, cand_list, key=lambda x: x[1])
        
        # now determine separator x
        values = [v for _, v in chosen]
        max_chosen = max(values) if values else self.B
        # remove chosen keys from D0 and D1 lazily: we only delete from key_map and leave stale entries to be ignored later
        chosen_keys = [k for k, _ in chosen]
        # Remove chosen keys from key_map so that future Pull won't return them again until re-inserted
        for k in chosen_keys:
            self.key_map.pop(k, None)
        # Determine separator x: smallest remaining value in structure if any, else B
        # Find smallest among D0 and D1 current key_map values
        smallest_remain = float('inf')
        # check D0 batches
        for batch in self.D0:
            for k, v in batch:
                cur = self.key_map.get(k)
                if cur is not None and cur < smallest_remain:
                    smallest_remain = cur
        # check D1 blocks
        for blk in self.D1:
            for k, v in blk.items:
                cur = self.key_map.get(k)
                if cur is not None and cur < smallest_remain:
                    smallest_remain = cur
        if smallest_remain == float('inf'):
            separator = self.B
        else:
            separator = smallest_remain
        return (chosen_keys, separator)
    
    def is_empty(self) -> bool:
        return len(self.key_map) == 0
