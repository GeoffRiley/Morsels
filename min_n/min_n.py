import heapq
from typing import Any, List
from heapq import heapify, heappop, heappush, nsmallest


def min_n(a_list: List[Any], count: int, *, key: callable = None) -> List[Any]:
    myheap = heapq.merge(a_list)
    return nsmallest(count, myheap, key=key)


class MinHeap:
    def __init__(self, a_list: List[Any]) -> None:
        myheap = a_list.copy()
        heapify(myheap)
        self.heap = myheap

    def __len__(self):
        return self.heap.__len__()

    def pop(self):
        return heappop(self.heap)

    def push(self, value: Any):
        heappush(self.heap, value)

    def peek(self, pos=0):
        return self.heap[pos]
