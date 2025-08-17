# Enhanced EdTech Math AI Tutor
# Uses SymPy for solving/explaining math, Matplotlib for visualizations.
# Supports equations, derivatives, integrals, limits, simplifications.
# Author: Shah Abrar Ul Haq

import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, solve, diff, integrate, limit, simplify, sympify, latex

x = symbols('x')


def solve_equation(expr):
    try:
        eq = sympify(expr)
        solutions = solve(eq, x)
        exp = f"Simplify: {simplify(eq)}. Solve: {solutions}. Steps: Set to zero, factor if quadratic."
        return solutions, exp
    except Exception as e:
        return None, f"Error: {str(e)}"


def differentiate(expr):
    try:
        der = diff(sympify(expr), x)
        exp = f"Derivative: {der}. Steps: Power rule for polynomials, chain rule for composites."
        return der, exp
    except:
        return None, "Error"


def integrate_expr(expr):
    try:
        integ = integrate(sympify(expr), x)
        exp = f"Integral: {integ} + C. Steps: Reverse differentiation rules."
        return integ, exp
    except:
        return None, "Error"


def compute_limit(expr, point):
    try:
        lim = limit(sympify(expr), x, point)
        exp = f"Limit as x->{point}: {lim}. Steps: Substitute if direct, or L'Hôpital if indeterminate."
        return lim, exp
    except:
        return None, "Error"


def simplify_expr(expr):
    try:
        simp = simplify(sympify(expr))
        exp = f"Simplified: {simp}. Steps: Combine like terms, factor."
        return simp, exp
    except:
        return None, "Error"


def plot_function(expr, title):
    try:
        f = sp.lambdify(x, sympify(expr), 'numpy')
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)
        plt.plot(x_vals, y_vals)
        plt.title(title)
        plt.savefig(f"{title.lower().replace(' ', '_')}.png")
        plt.close()
        return f"Plot saved as {title.lower().replace(' ', '_')}.png"
    except:
        return "Plotting error"


def get_math_response(query):
    query_lower = query.lower()

    if "solve" in query_lower:
        expr = query.split("solve")[-1].strip()
        result, exp = solve_equation(expr)
        if result is not None:
            return f"Solutions: {result}. Explanation: {exp} (LaTeX: {latex(result)})"
    elif "differentiate" in query_lower or "derivative" in query_lower:
        expr = query.split("differentiate")[-1].strip() if "differentiate" in query_lower else query.split("of")[
            -1].strip()
        result, exp = differentiate(expr)
        if result is not None:
            plot = plot_function(expr, "Original Function") + " & " + plot_function(result, "Derivative")
            return f"Result: {result}. Explanation: {exp} (LaTeX: {latex(result)}). Visuals: {plot}"
    elif "integrate" in query_lower or "integral" in query_lower:
        expr = query.split("integrate")[-1].strip() if "integrate" in query_lower else query.split("of")[-1].strip()
        result, exp = integrate_expr(expr)
        if result is not None:
            plot = plot_function(expr, "Original Function") + " & " + plot_function(result, "Integral")
            return f"Result: {result} + C. Explanation: {exp} (LaTeX: {latex(result)}). Visuals: {plot}"
    elif "limit" in query_lower:
        parts = query_lower.split("limit of")[-1].strip().split("at")
        expr, point = parts[0].strip(), parts[1].strip() if len(parts) > 1 else "0"
        result, exp = compute_limit(expr, point)
        if result is not None:
            return f"Result: {result}. Explanation: {exp}"
    elif "simplify" in query_lower:
        expr = query.split("simplify")[-1].strip()
        result, exp = simplify_expr(expr)
        if result is not None:
            return f"Result: {result}. Explanation: {exp} (LaTeX: {latex(result)})"
    else:
        return "I handle solve, differentiate, integrate, limit, simplify. E.g., 'integrate x**2', 'limit sin(x)/x at 0'."


# Main loop
print(
    "Welcome to Enhanced Math AI Tutor! Solve, differentiate, integrate, find limits, simplify. Add 'plot' for visuals. Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye! Happy studying.")
        break
    response = get_math_response(user_input)
    print("AI Tutor: " + response)