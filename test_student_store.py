# test_student_store.py
# ============================================================
# Lab 2 – Part A: Write tests that FAIL first, then fix them.
#
# YOUR TASKS:
#   1. Push this file as-is → CI should show RED (failing tests)
#   2. Read each failing test carefully — it tells you what's wrong
#   3. Fix the bug in THIS file (not in student_store.py)
#   4. Push again → CI should show GREEN (all passing)
#
# There are 3 bugs hidden in this test file.
# The source code (student_store.py) is correct — the bugs are here.
# ============================================================

import unittest
from student_store import Item, total_value, cheapest, search


class TestItem(unittest.TestCase):

    def setUp(self):
        """Fresh items before every test."""
        self.pen   = Item("Blue Pen",   price=5.0,  stock=10)
        self.ruler = Item("Ruler",      price=12.0, stock=5)
        self.book  = Item("Notebook",   price=35.0, stock=0)

    # ── restock ──────────────────────────────────────────────

    def test_restock_increases_stock(self):
        self.pen.restock(20)
        self.assertEqual(self.pen.stock, 30)

    def test_restock_zero_raises(self):
        with self.assertRaises(ValueError):
            self.pen.restock(0)

    def test_restock_negative_raises(self):
        with self.assertRaises(ValueError):
            self.pen.restock(-5)

    # ── sell ─────────────────────────────────────────────────

    def test_sell_reduces_stock(self):
        self.pen.sell(3)
        self.assertEqual(self.pen.stock, 7)

    def test_sell_exact_stock(self):
        """Selling exactly what's in stock should leave stock at 0."""
        self.pen.sell(10)
        self.assertEqual(self.pen.stock, 0)

    def test_sell_overdraft_raises(self):
        with self.assertRaises(ValueError):
            self.pen.sell(99)

    def test_sell_zero_raises(self):
        with self.assertRaises(ValueError):
            self.pen.sell(0)

    # ── BUG 1 ────────────────────────────────────────────────
    def test_sell_negative_raises(self):
        """
        Selling a negative quantity should raise ValueError.
        Fix: change sell(-1) to the correct value that triggers the error.
        """
        with self.assertRaises(ValueError):
            self.pen.sell(-10)          # ← BUG: 1 is a valid quantity, not negative

    # ── apply_discount ───────────────────────────────────────

    def test_discount_reduces_price(self):
        self.pen.apply_discount(20)
        self.assertAlmostEqual(self.pen.price, 4.0, places=2)

    def test_discount_zero_no_change(self):
        self.pen.apply_discount(0)
        self.assertAlmostEqual(self.pen.price, 5.0, places=2)

    def test_discount_100_makes_free(self):
        self.pen.apply_discount(100)
        self.assertAlmostEqual(self.pen.price, 0.0, places=2)

    # ── BUG 2 ────────────────────────────────────────────────
    def test_discount_above_100_raises(self):
        """
        A discount above 100% is invalid and must raise ValueError.
        Fix: pass a value above 100 to trigger the error.
        """
        with self.assertRaises(ValueError):
            self.pen.apply_discount(120)   # ← BUG: 50% is a valid discount


class TestStoreFunctions(unittest.TestCase):

    def setUp(self):
        self.items = [
            Item("Blue Pen",   price=5.0,  stock=10),
            Item("Ruler",      price=12.0, stock=5),
            Item("Notebook",   price=35.0, stock=3),
            Item("Eraser",     price=2.0,  stock=20),
        ]

    # ── total_value ──────────────────────────────────────────

    def test_total_value_correct(self):
        # 5*10 + 12*5 + 35*3 + 2*20 = 50 + 60 + 105 + 40 = 255
        self.assertAlmostEqual(total_value(self.items), 255.0, places=2)

    def test_total_value_empty(self):
        self.assertEqual(total_value([]), 0.0)

    # ── cheapest ─────────────────────────────────────────────

    def test_cheapest_correct(self):
        result = cheapest(self.items)
        self.assertEqual(result.name, "Eraser")

    def test_cheapest_single(self):
        result = cheapest([Item("Pen", 5.0, 1)])
        self.assertEqual(result.name, "Pen")

    def test_cheapest_empty_raises(self):
        with self.assertRaises(ValueError):
            cheapest([])

    # ── search ───────────────────────────────────────────────

    def test_search_finds_match(self):
        result = search(self.items, "pen")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Blue Pen")

    def test_search_case_insensitive(self):
        result = search(self.items, "PEN")
        self.assertEqual(len(result), 1)

    def test_search_no_match(self):
        result = search(self.items, "stapler")
        self.assertEqual(result, [])

    # ── BUG 3 ────────────────────────────────────────────────
    def test_search_partial_keyword(self):
        """
        Searching for 'note' should find 'Notebook'.
        Fix: change the keyword to something that actually matches.
        """
        result = search(self.items, "note")   # ← BUG: 'xyz' matches nothing
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Notebook")


if __name__ == "__main__":
    unittest.main(verbosity=2)
