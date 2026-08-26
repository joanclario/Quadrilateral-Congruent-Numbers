# Quadrilateral Congruent Numbers

SageMath implementation for finding rational quadrilaterals constructed by gluing two Heronian triangles along a common diagonal.

This repository supports the computational search for quadrilateral congruent numbers, covering both the **rational case** ($D = 1$) and the **quadratic case** ($D > 1$).

## Mathematical Overview

A rational quadrilateral with side lengths $a, b, c, d$ and diagonals $e, f$ is constructed by gluing two Heronian triangles along a shared diagonal $e$. 

- **Rational Case ($D = 1$):** The total area $N = A_1 + A_2$ is a rational number. The script rescales the quadrilateral so that $N$ becomes a squarefree integer.
- **Quadratic Case ($D > 1$):** The total area is of the form $N\sqrt{D}$, where $D > 1$ is a squarefree integer representing the area discriminant of the component triangles.

## Repository Structure

- `quadrilateral_congruent_rational.py`  
  Searches for quadrilaterals in the rational case ($D = 1$). Outputs minimal rational representatives for each squarefree area $N$.

- `quadrilateral_congruent_quadratic.py`  
  Searches for quadrilaterals in the quadratic case ($D > 1$). Categorizes found examples by discriminant $D$ and rational factor $N$.

## Requirements

- [SageMath](https://www.sagemath.org/) (version 9.0 or higher recommended)

## Execution

Run the scripts directly from your terminal using SageMath:

```bash
# Run the rational case (D = 1)
sage quadrilateral_congruent_rational.py

# Run the quadratic case (D > 1)
sage quadrilateral_congruent_quadratic.py
