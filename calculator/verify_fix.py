# calculator/verify_fix.py
"""Ad-hoc verification of operator precedence and associativity."""

from pkg.calculator import Calculator

c = Calculator()

cases = [
    ("3 + 7 * 2", 17),        # the reported bug
    ("2 * 3 + 8 / 2 - 5", 5),
    ("3 * 4 + 5", 17),
    ("10 - 4 - 3", 3),        # left associativity for '-'
    ("100 / 10 / 2", 5),      # left associativity for '/'
    ("2 + 3 * 4 - 6 / 3", 12),
    ("1 + 2 * 3 * 4", 25),
    ("8 / 4 * 2", 4),         # '*' and '/' same precedence, left to right
    ("5 - 2 - 1 * 2", 1),
    ("2 * 3 - 8 / 2 + 5", 7),
    ("7 * 2 + 3", 17),
    ("3 + 2 * 7", 17),
]

failed = 0
for expr, expected in cases:
    got = c.evaluate(expr)
    ok = got == expected
    if not ok:
        failed += 1
    print(f"{'PASS' if ok else 'FAIL'}: {expr!r} -> {got} (expected {expected})")

print("\nAll good!" if not failed else f"\n{failed} failure(s)")
