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
        expr_part = query.split("solve")[-1].strip()
        try:
            expr = sympify(expr_part.split("=")[0].strip())
            solutions = solve(expr, x)
            exp = f"Simplify: {simplify(expr)}. Solve: {solutions}. Steps: Set to zero, factor if quadratic."
            return f"Solutions: {solutions}. Explanation: {exp} (LaTeX: {latex(solutions)})"
        except (SympyException, IndexError, ValueError) as e:
            return f"Error: Could not solve {expr_part}. Please use a valid equation like 'x**2 - 4 = 0'. Details: {str(e)}"
    elif "differentiate" in query_lower or "derivative" in query_lower:
        expr = (query.split("differentiate")[-1].strip() if "differentiate" in query_lower
                else query.split("of")[-1].strip() if "derivative" in query_lower else "")
        if not expr:
            return "Error: Please provide an expression to differentiate, e.g., 'differentiate x**3'."
        try:
            result, exp = differentiate(expr)
            if result is not None:
                plot = (plot_function(expr, "Original Function") + " & " + plot_function(result, "Derivative")
                        if "plot" in query_lower else "")
                return (f"Result: {result}. Explanation: {exp} (LaTeX: {latex(result)}). Visuals: {plot}"
                        if plot else f"Result: {result}. Explanation: {exp} (LaTeX: {latex(result)})")
            else:
                return exp
        except (SympyException, ValueError) as e:
            return f"Error: Could not differentiate {expr}. Please use a valid expression. Details: {str(e)}"
    elif "integrate" in query_lower or "integral" in query_lower:
        expr = (query.split("integrate")[-1].strip() if "integrate" in query_lower
                else query.split("of")[-1].strip() if "integral" in query_lower else "")
        if not expr:
            return "Error: Please provide an expression to integrate, e.g., 'integrate x**2'."
        try:
            result, exp = integrate_expr(expr)
            if result is not None:
                plot = (plot_function(expr, "Original Function") + " & " + plot_function(result, "Integral")
                        if "plot" in query_lower else "")
                return (f"Result: {result} + C. Explanation: {exp} (LaTeX: {latex(result)}). Visuals: {plot}"
                        if plot else f"Result: {result} + C. Explanation: {exp} (LaTeX: {latex(result)})")
            else:
                return exp
        except (SympyException, ValueError) as e:
            return f"Error: Could not integrate {expr}. Please use a valid expression. Details: {str(e)}"
    elif "limit" in query_lower:
        try:
            parts = query_lower.split("limit of")[-1].strip().split("at")
            if len(parts) < 2:
                return "Error: Please specify a limit point, e.g., 'limit sin(x)/x at 0'."
            expr, point = parts[0].strip(), parts[1].strip()
            result, exp = compute_limit(expr, point)
            if result is not None:
                return f"Result: {result}. Explanation: {exp}"
            else:
                return exp
        except (SympyException, IndexError, ValueError) as e:
            return f"Error: Could not compute limit for {query}. Please use format 'limit <expr> at <point>'. Details: {str(e)}"
    elif "simplify" in query_lower:
        expr = query.split("simplify")[-1].strip()
        try:
            result, exp = simplify_expr(expr)
            if result is not None:
                return f"Result: {result}. Explanation: {exp} (LaTeX: {latex(result)})"
            else:
                return exp
        except (SympyException, ValueError) as e:
            return f"Error: Could not simplify {expr}. Please use a valid expression. Details: {str(e)}"
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