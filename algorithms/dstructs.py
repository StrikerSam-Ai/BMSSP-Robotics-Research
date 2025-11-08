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

