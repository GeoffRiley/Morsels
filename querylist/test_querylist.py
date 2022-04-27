import unittest

from querylist import QueryList


class Item:
    def __init__(self, id, name=None, color="purple", version=1):
        self.id = id
        self.name = name
        self.color = color
        self.version = version

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __repr__(self):
        attrs = (f"{name}={value!r}" for name, value in self.__dict__.items())
        return f"Item({', '.join(attrs)})"


class QueryListTests(unittest.TestCase):
    """Tests for QueryList."""

    four_items = [
        Item(id=1, name="duck"),
        Item(id=2, name="monkey", color="blue"),
        Item(id=3, name="parrot"),
        Item(id=4, name="snake", color="yellow"),
    ]

    ten_items = [
        Item(id=1, name="duck"),
        Item(id=2, name="monkey", color="blue"),
        Item(id=3, name="parrot", version=3),
        Item(id=4, name="snake", color="yellow", version=3),
        Item(id=5, name="spam", color="pink"),
        Item(id=6, name="pony", color="pink", version=3),
        Item(id=7, name="guitar", color="green", version=3),
        Item(id=8, name="car", color="black"),
        Item(id=9, name="balloon", color="red"),
        Item(id=10, name="cheese", color="yellow"),
    ]

    def test_iterating(self):
        items = QueryList(self.four_items)
        self.assertEqual(list(items), self.four_items)

    def test_appending(self):
        a_copy = list(self.four_items)
        pony = Item(id=5, name="pony", color="pink")

        items = QueryList(self.four_items)
        items.append(pony)

        self.assertEqual(list(items), [*self.four_items, pony])
        self.assertEqual(self.four_items, a_copy, "Original list is unchanged")

    def test_filtering_on_nothing(self):
        items = QueryList(self.four_items)
        self.assertEqual(list(items.filter()), list(items))

    def test_filtering_on_one_attribute(self):
        items = QueryList(self.four_items)
        duck, monkey, parrot, snake = self.four_items

        self.assertEqual(list(items.filter(color="purple")), [duck, parrot])
        self.assertEqual(list(items.filter(version=1)), self.four_items)
        self.assertEqual(list(items.filter(id=2)), [monkey])

    def test_filtering_on_multiple_attributes(self):
        duck, monkey, parrot, snake = self.four_items
        pink_pony = Item(id=5, name="pony", color="pink")
        pink_parrot = Item(id=6, name="parrot", color="pink")

        items = QueryList(self.four_items)
        items.append(pink_pony)
        items.append(pink_parrot)

        self.assertEqual(list(items.filter(color="purple", version=2)), [])
        self.assertEqual(
            list(items.filter(color="purple", version=1)),
            [duck, parrot],
        )
        self.assertEqual(list(items.filter(name="parrot", color="pink")),
                         [pink_parrot])

    def test_attrs_method(self):
        items = QueryList(self.ten_items)
        self.assertEqual(
            items.filter(version=3).attrs("name"),
            ["parrot", "snake", "pony", "guitar"],
        )
        self.assertEqual(
            items.filter(version=3).attrs("id", "name"),
            [(3, "parrot"), (4, "snake"), (6, "pony"), (7, "guitar")],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_double_underscore_queries(self):
        items = QueryList(self.ten_items)
        self.assertEqual(
            items.filter(version__gt=2).attrs("name"),
            ["parrot", "snake", "pony", "guitar"],
        )
        self.assertEqual(
            items.filter(version__lt=2).attrs("name"),
            ["duck", "monkey", "spam", "car", "balloon", "cheese"],
        )
        self.assertEqual(
            items.filter(color__in="purple-pink").attrs("name"),
            ["duck", "parrot", "spam", "pony"],
        )
        self.assertEqual(
            items.filter(version__ne=1).attrs("name"),
            ["parrot", "snake", "pony", "guitar"],
        )
        self.assertEqual(
            items.filter(name__contains="p", color__ne="purple").attrs("name"),
            ["spam", "pony"],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_filter_objects(self):
        from querylist import F
        items = QueryList(self.ten_items)
        self.assertEqual(
            items.filter(F.version > 2).attrs("name"),
            ["parrot", "snake", "pony", "guitar"],
        )
        self.assertEqual(
            items.filter(F.version < 2).attrs("name"),
            ["duck", "monkey", "spam", "car", "balloon", "cheese"],
        )
        self.assertEqual(
            items.filter(
                F.version == 1,
                F.color != "purple",
                F.color != "pink",
            ).attrs("name"),
            ["monkey", "car", "balloon", "cheese"],
        )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_bitwise_operations_when_filtering(self):
        from querylist import F
        items = QueryList(self.ten_items)
        self.assertEqual(
            items.filter((F.version > 2)
                         | (F.color == "purple")).attrs("name"),
            ["duck", "parrot", "snake", "pony", "guitar"],
        )
        self.assertEqual(
            items.filter((F.version < 2)
                         & (F.color != "purple")).attrs("name"),
            ["monkey", "spam", "car", "balloon", "cheese"],
        )
        self.assertEqual(
            items.filter(((F.color == "purple") | (F.color == "blue"))
                         & (F.version == 1)).attrs("name"),
            ["duck", "monkey"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
