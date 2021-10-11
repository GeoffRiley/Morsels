from time import perf_counter
import unittest


from timer2 import Timer


class TimerTests(unittest.TestCase):

    """Tests for Timer."""

    _baseline = None

    @staticmethod
    def get_baseline(count=100):
        times = 0
        for i in range(count):
            with Timer() as timer:
                sleep(0)
            times += timer.elapsed
        return times / count

    def assertTimeEqual(self, actual, expected):
        if self._baseline is None:
            self._baseline = self.get_baseline()
        self.assertAlmostEqual(actual, self._baseline+expected, delta=0.01)

    def test_short_time(self):
        with Timer() as timer:
            sleep(0.1)
        self.assertGreater(timer.elapsed, 0.009)
        self.assertLess(timer.elapsed, 0.8)

    def test_very_short_time(self):
        with Timer() as timer:
            pass
        self.assertTimeEqual(timer.elapsed, 0)

    def test_two_timers(self):
        with Timer() as timer1:
            sleep(0.005)
            with Timer() as timer2:
                sleep(0.05)
            sleep(0.05)
        self.assertLess(timer2.elapsed, timer1.elapsed)

    def test_reusing_same_timer(self):
        timer = Timer()
        with timer:
            sleep(0.01)
        elapsed1 = timer.elapsed
        with timer:
            sleep(0.1)
        elapsed2 = timer.elapsed
        self.assertLess(elapsed1, elapsed2)

    def test_runs_recorded(self):
        timer1 = Timer()
        timer2 = Timer()
        with timer1:
            with timer2:
                sleep(0.001)
            with timer2:
                sleep(0.002)
        with timer1:
            sleep(0.005)
        with timer1:
            pass
        self.assertEqual(len(timer1.runs), 3)
        self.assertEqual(len(timer2.runs), 2)
        self.assertGreater(timer1.runs[0], sum(timer2.runs))
        self.assertTimeEqual(timer1.runs[2], 0.000)

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_split(self):
        with Timer() as timer1:
            with timer1.split() as timer2:
                sleep(0.001)
            with timer1.split() as timer3:
                sleep(0.002)
            with timer1.split() as timer4:
                sleep(0.003)
        self.assertTimeEqual(
            timer1.elapsed,
            timer2.elapsed+timer3.elapsed+timer4.elapsed,
        )
        self.assertEqual(timer1[0].elapsed, timer2.elapsed)
        self.assertEqual(timer1[1].elapsed, timer3.elapsed)
        self.assertEqual(timer1[2].elapsed, timer4.elapsed)
        self.assertEqual(len(timer1.runs), 1)
        self.assertEqual(len(timer2.runs), 1)
        self.assertEqual(len(timer3.runs), 1)
        self.assertEqual(len(timer4.runs), 1)
        with self.assertRaises(Exception):
            with timer1.split():
                print("timer split when it wasn't running!")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_named_split(self):
        sleeps = [0.002, 0.001, 0.004, 0.003]
        checker1 = Timer()
        checker2 = Timer()
        with Timer() as timer:
            for n in sleeps:
                with checker1:
                    with timer.split('sleep'):
                        with checker2:
                            sleep(n)
        self.assertEqual(len(timer['sleep'].runs), 4)
        runs = timer['sleep'].runs
        self.assertLess(runs[0], checker1.runs[0])
        self.assertLess(runs[1], checker1.runs[1])
        self.assertLess(runs[2], checker1.runs[2])
        self.assertLess(runs[3], checker1.runs[3])
        self.assertGreater(runs[0], checker2.runs[0])
        self.assertGreater(runs[1], checker2.runs[1])
        self.assertGreater(runs[2], checker2.runs[2])
        self.assertGreater(runs[3], checker2.runs[3])

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_globally_named_timer(self):
        timer1 = Timer('t1')
        timer2 = Timer('t1')
        timer3 = Timer('t2')
        with timer1:
            sleep(0.001)
        self.assertEqual(len(timer1.runs), 1)
        self.assertEqual(len(timer2.runs), 1)
        self.assertEqual(len(timer3.runs), 0)
        with timer2:
            pass
        self.assertEqual(len(timer1.runs), 2)
        self.assertEqual(len(timer2.runs), 2)
        self.assertEqual(len(timer3.runs), 0)
        with timer3:
            sleep(0.001)
        self.assertEqual(len(timer1.runs), 2)
        self.assertEqual(len(timer3.runs), 1)
        self.assertGreater(timer1.runs[0], timer1.runs[1])
        self.assertEqual(timer1.runs, timer2.runs)
        self.assertEqual(timer1.elapsed, timer2.elapsed)


def sleep(duration):
    now = perf_counter()
    end = now + duration
    while now < end:
        now = perf_counter()


if __name__ == "__main__":
    unittest.main(verbosity=2)
