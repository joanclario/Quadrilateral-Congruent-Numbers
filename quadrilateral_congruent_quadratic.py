#!/usr/bin/env sage
"""
Quadratic Quadrilateral Congruent Numbers (Quadratic Case: D > 1)

Generates rational quadrilaterals by gluing two quadratic Heronian triangles
sharing the same squarefree area discriminant D > 1 along a common diagonal e.
Computes pair (D, N) where the total area is N*sqrt(D).
"""

from sage.all import *

# ==============================================================================
# PARAMETERS & RATIONAL GRID (Fast execution setup)
# ==============================================================================
MAX_NUM = 10  # Maximal numerator
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
def heron_area_quad(a, b, c):
    """
    Computes the area of triangle (a,b,c) as q * sqrt(D) where D is squarefree > 1.
    Returns (q, D) if D > 1, or None if the triangle is invalid or Heronian (D=1).
    """
    if a + b <= c or a + c <= b or b + c <= a:
        return None

    s = (a + b + c) / 2
    H = s * (s - a) * (s - b) * (s - c)

    if H <= 0:
        return None

    D = squarefree_part(H)
    if D == 1:
        return None  # Rational case handled separately

    q = sqrt(H / D)
    return q, D

def normalize_quad_area(q, D):
    """
    Given area A = q*sqrt(D), normalizes N modulo rational squares so that 
    N is a squarefree integer up to rational square scaling.
    """
    M = q^2 * D
    D_sf = squarefree_part(M)
    N_raw = sqrt(M / D_sf)
    
    num = ZZ(numerator(N_raw))
    den = ZZ(denominator(N_raw))
    
    N = squarefree_part(num) * squarefree_part(den)
    return N, D_sf

# ==============================================================================
# STEP 1: PRECOMPUTE QUADRATIC HERONIAN TRIANGLES
# ==============================================================================
Triangles = {}
count = 0

for a in QQlist:
    for b in QQlist:
        if a > b:
            continue
        for e in QQlist:
            res = heron_area_quad(a, b, e)
            if res is not None:
                q, D = res
                count += 1
                Triangles.setdefault((e, D), []).append((a, b, q))

print(f"Precomputed {count} quadratic Heronian triangles.")

# ==============================================================================
# STEP 2: GLUE TRIANGLES AND SEARCH QUADRILATERALS
# ==============================================================================
Examples = {}
print("\nSearching for quadratic rational quadrilaterals (D > 1)...\n")

for (e, D) in sorted(Triangles.keys()):
    L = Triangles[(e, D)]
    m = len(L)

    for i in range(m):
        a, b, q1 = L[i]
        for j in range(i, m):
            c, d, q2 = L[j]

            q_total = q1 + q2  # Coefficient of sqrt(D)
            X = a^2 - b^2 + c^2 - d^2
            rad = X^2 + 16 * (q_total^2) * D

            if not rad.is_square():
                continue

            f = rad.sqrt() / (2 * e)

            # Normalize area to pair (D, N)
            N, DD = normalize_quad_area(q_total, D)
            key = (DD, N)

            if key not in Examples:
                Examples[key] = (a, b, c, d, e, f, q1, q2)

# ==============================================================================
# SUMMARY & OUTPUT
# ==============================================================================
byD = {}
for D, N in sorted(Examples.keys()):
    byD.setdefault(D, []).append(N)

print("=" * 60)
print("Summary of found N values per discriminant D:")
print("=" * 60)
for D in sorted(byD.keys()):
    print(f"D = {D:2d} | N values: {byD[D][:10]}")
print("=" * 60)