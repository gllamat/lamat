"""Synthetic session-date join; the prices are invented."""
from datetime import date
from lamat_quant.date_alignment import align_by_date


left = [(date(2020, 1, 1), 100), (date(2020, 1, 2), 101),
        (date(2020, 1, 3), 102)]
right = [(date(2020, 1, 1), 200), (date(2020, 1, 3), 202)]
result = align_by_date(left, right)
print("Matched:", result.matched)
print("Left-only sessions:", result.left_only)
print("Right-only sessions:", result.right_only)
