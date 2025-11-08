# algorithms/dstructs.py
"""
Practical implementation of the partial-sorting data structure D described in the BMSSP paper.
Supports:
 - insert(pair)
 - batch_prepend(list_of_pairs)
 - pull() -> (subset_keys, separator_value)

This is a pragmatic implementation designed to be efficient enough for ~50k nodes.
"""

import heapq
from collections import deque
from typing import List, Tuple, Dict

class Block:
    def __init__(self, items: List[Tuple[int, float]] = None):
        self.items = items or []
        self.update_bound()

    def update_bound(self):
        if not self.items:
            self.ub = float('inf')
        else:
            self.ub = max(v for _, v in self.items)

    def push(self, pair):
        self.items.append(pair)
        if pair[1] > self.ub:
            self.ub = pair[1]

    def extend(self, pairs):
        if pairs:
            self.items.extend(pairs)
            self.ub = max(self.ub, max(v for _, v in pairs))

class PartialSortingDS:
    def __init__(self, M: int, B: float):
        self.M = max(1, int(M))
        self.B = B
        self.D0 = deque()   # prepended batches (each sorted ascending)
        self.D1 = []        # list of Block()
        self.D1_bounds = [] # list of upper bounds of blocks
        self.key_map = {}   # current best value for key

    def _rebuild_bounds(self):
        self.D1_bounds = [blk.ub for blk in self.D1]

    def insert(self, pair):
        key, value = pair
        old = self.key_map.get(key)
        if old is not None and value >= old:
            return
        self.key_map[key] = value
        # Add to last block (create if necessary)
        if not self.D1 or len(self.D1[-1].items) >= 2 * self.M:
            blk = Block([pair])
            self.D1.append(blk)
            self.D1_bounds.append(blk.ub)
        else:
            self.D1[-1].push(pair)
            self.D1_bounds[-1] = self.D1[-1].ub

    def batch_prepend(self, pairs: List[Tuple[int, float]]):
        if not pairs:
            return
        best = {}
        for k, v in pairs:
            if k in best:
                if v < best[k]:
                    best[k] = v
            else:
                best[k] = v
        batch = [(k, best[k]) for k in best]
        batch.sort(key=lambda x: x[1])
        # update current map with batch values if better
        for k, v in batch:
            old = self.key_map.get(k)
            if old is None or v < old:
                self.key_map[k] = v
        self.D0.appendleft(batch)

    def pull(self):
        # collect prefix of D0 up to M
        d0_acc = []
        for batch in self.D0:
            for k, v in batch:
                # only consider current map value
                cur = self.key_map.get(k)
                if cur is not None:
                    d0_acc.append((k, cur))
                if len(d0_acc) >= self.M:
                    break
            if len(d0_acc) >= self.M:
                break

        # collect blocks from D1 until we have at least M candidates
        d1_acc = []
        idx = 0
        while len(d0_acc) + len(d1_acc) < self.M and idx < len(self.D1):
            blk = self.D1[idx]
            for k, v in blk.items:
                cur = self.key_map.get(k)
                if cur is not None:
                    d1_acc.append((k, cur))
            idx += 1

        if not d0_acc and not d1_acc:
            return [], self.B

        # deduplicate and choose best per key
        cand = d0_acc + d1_acc
        best = {}
        for k, v in cand:
            if k not in best or v < best[k]:
                best[k] = v
        cand_list = [(k, best[k]) for k in best]

        if len(cand_list) <= self.M:
            chosen = cand_list
        else:
            chosen = heapq.nsmallest(self.M, cand_list, key=lambda x: x[1])

        chosen_keys = [k for k, _ in chosen]
        max_chosen = max(v for _, v in chosen) if chosen else self.B

        # remove chosen keys from key_map so they won't be returned again until re-inserted
        for k in chosen_keys:
            self.key_map.pop(k, None)

        # find smallest remaining value (separator) among key_map
        smallest_remain = float('inf')
        for val in self.key_map.values():
            if val < smallest_remain:
                smallest_remain = val
        separator = smallest_remain if smallest_remain != float('inf') else self.B

        return chosen_keys, separator

    def is_empty(self):
        return len(self.key_map) == 0
