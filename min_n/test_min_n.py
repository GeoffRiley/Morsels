import timeit
from random import randint
import unittest


from min_n import min_n


BIG_NUMBERS = [
    3748, 7250, 140, 7669, 5711, 2284, 3322, 6435, 8138, 6920, 9634, 7511,
    5295, 5456, 7458, 5618, 102, 7747, 4638, 46, 4532, 1483, 944, 3542, 6641,
    9091, 693, 836, 3099, 3385, 7798, 758, 8407, 4756, 8801, 3936, 5301, 5744,
    6454, 1156, 7686, 5664, 2568, 6414, 3469, 2867, 8875, 6097, 2546, 4658,
    7027, 9437, 755, 8536, 8186, 9539, 661, 6706, 265, 2254, 2402, 3355, 9141,
    5091, 1727, 6739, 4599, 5599, 9007, 2925, 2894, 5333, 9586, 7409, 916,
    6420, 8493, 9531, 5083, 5350, 3346, 1378, 6260, 3143, 7216, 684, 170, 6721,
    418, 7013, 7729, 7484, 5355, 4850, 8073, 1389, 2084, 1856, 9740, 2747,
]
MANY_BIG_NUMBERS = [randint(100, 1000) for n in range(2500)]


class MinNTests(unittest.TestCase):

    """Tests for min_n."""

    def test_no_elements_n_of_zero(self):
        self.assertEqual(min_n([], 0), [])

    def test_no_elements_positive_n(self):
        self.assertEqual(min_n([], 5), [])

    def test_n_bigger_than_iterable(self):
        self.assertEqual(min_n([2, 1, 3, 4], 5), [1, 2, 3, 4])

    def test_original_unchanged(self):
        numbers = [2, 1, 3, 4]
        min_n(numbers, 3)
        self.assertEqual(numbers, [2, 1, 3, 4])

    def test_n_of_one(self):
        self.assertEqual(
            min_n([11, 3, 18, 47, 76, 4, 29, 2, 7, 1, 123, 199, 322], 1),
            [1],
        )
        self.assertEqual(min_n(range(1000, 1, -1), 1), [2])

    def test_small_n(self):
        self.assertEqual(
            min_n(['watermelon', 'blueberry', 'lime', 'lemon'], 2),
            ['blueberry', 'lemon'],
        )
        self.assertEqual(
            min_n([4, 123, 29, 47, 76, 199, 7, 1, 11, 18, 2, 3, 322], 2),
            [1, 2],
        )
        self.assertEqual(
            min_n([7, 18, 2, 199, 47, 3, 322, 76, 11, 4, 29, 1, 123], 4),
            [1, 2, 3, 4],
        )
        self.assertEqual(
            min_n([3, 199, 76, 7, 29, 2, 47, 1, 11, 123, 4, 18, 322], 7),
            [1, 2, 3, 4, 7, 11, 18],
        )
        self.assertEqual(
            min_n(BIG_NUMBERS, 8),
            [46, 102, 140, 170, 265, 418, 661, 684],
        )

    def test_bigger_n(self):
        self.assertEqual(
            min_n(BIG_NUMBERS, 50),
            [46, 102, 140, 170, 265, 418, 661, 684, 693, 755, 758, 836, 916,
                944, 1156, 1378, 1389, 1483, 1727, 1856, 2084, 2254, 2284,
                2402, 2546, 2568, 2747, 2867, 2894, 2925, 3099, 3143, 3322,
                3346, 3355, 3385, 3469, 3542, 3748, 3936, 4532, 4599, 4638,
                4658, 4756, 4850, 5083, 5091, 5295, 5301],
        )

    def test_other_iterables(self):
        self.assertEqual(
            min_n((n**2 for n in BIG_NUMBERS), 3),
            [46**2, 102**2, 140**2],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_key_function(self):
        fruits = ['Watermelon', 'blueberry', 'lime', 'Lemon']
        self.assertEqual(
            min_n(fruits, 2),
            ['Lemon', 'Watermelon'],
        )
        self.assertEqual(
            min_n(fruits, 2, key=str.lower),
            ['blueberry', 'Lemon'],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_faster_than_sorting(self):
        sort_time = min(timeit.repeat(
            "sorted(numbers)",
            number=30,
            repeat=15,
            globals={'numbers': MANY_BIG_NUMBERS},
        ))
        min_n_time = min(timeit.repeat(
            "min_n(numbers, 5)",
            number=30,
            repeat=15,
            globals={'min_n': min_n, 'numbers': MANY_BIG_NUMBERS},
        ))
        self.assertLess(min_n_time, sort_time*0.93)


# To test the Bonus part of this exercise, comment out the following line
# @unittest.expectedFailure
class MinHeapTests(unittest.TestCase):

    """Tests for MinHeap."""

    def test_create_heap(self):
        from min_n import MinHeap
        MinHeap([322, 76, 4, 7, 2, 123, 47, 1, 18, 3, 29, 199, 11])
        MinHeap(BIG_NUMBERS)

    def test_length(self):
        from min_n import MinHeap
        numbers = [322, 76, 4, 7, 2, 123, 47, 1, 18, 3, 29, 199, 11]
        self.assertEqual(len(MinHeap(numbers)), len(numbers))
        self.assertEqual(len(MinHeap(BIG_NUMBERS)), len(BIG_NUMBERS))

    def test_peek_at_smallest(self):
        from min_n import MinHeap
        numbers = [11, 322, 3, 199, 29, 7, 1, 18, 76, 4, 2, 47, 123]
        h = MinHeap(numbers)
        self.assertEqual(h.peek(), 1)
        self.assertEqual(len(h), len(numbers))
        self.assertEqual(len(numbers), 13)
        i = MinHeap(BIG_NUMBERS)
        self.assertEqual(i.peek(), 46)
        self.assertEqual(len(i), len(BIG_NUMBERS))

    def test_pop_from_heap(self):
        from min_n import MinHeap
        numbers = [11, 322, 3, 199, 29, 7, 1, 18, 76, 4, 2, 47, 123]
        h = MinHeap(numbers)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(len(h), len(numbers)-1)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(h.pop(), 3)
        self.assertEqual(h.pop(), 4)
        self.assertEqual(len(h), len(numbers)-4)
        self.assertEqual(h.pop(), 7)
        self.assertEqual(h.pop(), 11)
        self.assertEqual(len(h), len(numbers)-6)
        i = MinHeap(BIG_NUMBERS)
        self.assertEqual(i.pop(), 46)

    def test_push_onto_heap(self):
        from min_n import MinHeap
        numbers = [11, 322, 3, 199, 29, 7, 1, 18, 76, 4, 2, 47, 123]
        i = MinHeap(BIG_NUMBERS)
        i.push(17)
        self.assertEqual(i.peek(), 17)
        i.push(24)
        self.assertEqual(i.pop(), 17)
        self.assertEqual(i.pop(), 24)
        self.assertEqual(i.pop(), 46)
        h = MinHeap(numbers)
        h.push(6)
        self.assertEqual(len(h), len(numbers)+1)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(h.pop(), 3)
        self.assertEqual(h.pop(), 4)
        self.assertEqual(h.pop(), 6)

    def test_faster_than_sorting(self):
        from min_n import MinHeap
        sort_time = min(timeit.repeat(
            "sorted(numbers)",
            number=4,
            repeat=4,
            globals={'numbers': MANY_BIG_NUMBERS},
        ))
        min_n_time = min(timeit.repeat(
            "heap = MinHeap(numbers)\n" +
            "items = [heap.pop() for _ in range(10)]",
            number=4,
            repeat=4,
            globals={'MinHeap': MinHeap, 'numbers': MANY_BIG_NUMBERS},
        ))
        self.assertLess(min_n_time, sort_time*0.93)


if __name__ == "__main__":
    unittest.main(verbosity=2)
