#!/usr/bin/env sage
"""
Rational Quadrilateral Congruent Numbers (Rational Case: D = 1)

Generates rational quadrilaterals by gluing two Heronian triangles (D = 1)
along a common diagonal e. Computes the resulting squarefree integer area N
and optionally outputs a minimal example for each found N.
"""

from sage.all import *

# ==============================================================================
# PARAMETERS & RATIONAL GRID (Fast execution setup)
# ==============================================================================
MAX_NUM = 15  # Maximal numerator
MAX_DEN = 5   # Maximal denominator

QQlist = []
for q in range(1, MAX_DEN + 1):
    for p in range(1, MAX_NUM * q + 1):
        if gcd(p, q) == 1:
            QQlist.append(QQ(p) / QQ(q))

QQlist = sorted(set(QQlist))
print(f"Generated {len(QQlist)} rational search coordinates.")

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def heron_area(a, b, c):
    """
    Returns the rational area of triangle (a,b,c) if it is Heronian (D=1).
    Returns None otherwise.
    """
    if a + b <= c or a + c <= b or b + c <= a:
        return None

    s = (a + b + c) / 2
    H = s * (s - a) * (s - b) * (s - c)

    if H <= 0:
        return None

    if H.is_square():
        return H.sqrt()

    return None

def format_latex(N, a, b, c, d, e, f, A1, A2):
    """Formats the quadrilateral data as a LaTeX table row."""
    def texQ(x):
        if x.denominator() == 1:
            return str(x)
        return f"\\tfrac{{{x.numerator()}}}{{{x.denominator()}}}"
    
    return f"{N} & \\left({texQ(a)},{texQ(b)},{texQ(c)},{texQ(d)},{texQ(e)},{texQ(f)}\\right) & \\left({texQ(A1)},{texQ(A2)}\\right) \\\\"

# ==============================================================================
# STEP 1: PRECOMPUTE HERONIAN TRIANGLES
# ==============================================================================
Triangles = {}
count = 0

for a in QQlist:
    for b in QQlist:
        if a > b:
            continue
        for e in QQlist:
            A = heron_area(a, b, e)
            if A is not None:
                count += 1
                Triangles.setdefault(e, []).append((a, b, A))

print(f"Precomputed {count} Heronian triangles.")

# ==============================================================================
# STEP 2: GLUE TRIANGLES AND SEARCH QUADRILATERALS
# ==============================================================================
Examples = {}
print("\nSearching for rational quadrilaterals (D = 1)...\n")

for e in sorted(Triangles.keys()):
    L = Triangles[e]
    m = len(L)

    for i in range(m):
        a, b, A1 = L[i]
        for j in range(i, m):
            c, d, A2 = L[j]

            N_total = A1 + A2
            X = a^2 - b^2 + c^2 - d^2
            rad = X^2 + 16 * N_total^2

            if not rad.is_square():
                continue

            f = rad.sqrt() / (2 * e)
            sf = squarefree_part(N_total)

            # Rescale quadrilateral to standard area N = sf
            scale = QQ(sqrt(sf / N_total))
            a_s, b_s, c_s, d_s = a * scale, b * scale, c * scale, d * scale
            e_s, f_s = e * scale, f * scale
            A1_s, A2_s = A1 * scale^2, A2 * scale^2

            if sf not in Examples:
                Examples[sf] = (a_s, b_s, c_s, d_s, e_s, f_s, A1_s, A2_s)

# ==============================================================================
# SUMMARY & OUTPUT
# ==============================================================================
print("=" * 60)
print(f"Found {len(Examples)} rational quadrilateral congruent numbers:")
found_N = sorted(Examples.keys())
print(found_N)
print("=" * 60)

print("\nSample LaTeX output for small N:")
for N in found_N[:10]:
    data = Examples[N]
    print(format_latex(N, *data))
