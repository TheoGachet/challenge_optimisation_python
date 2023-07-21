**Surveillance Optimization Algorithms in Python**

This repository contains multiple Python implementations of algorithms aimed at solving the surveillance optimization problem. The goal is to strategically position surveillance agents to monitor targets while minimizing the number of agents used.

### Implemented Algorithms:

1. **Local Search Algorithm (algorithme_de_recherche_locale.py)**: This algorithm iteratively explores neighboring solutions to improve the objective function. It starts with an initial solution and iteratively makes small adjustments to find local optima.

2. **Greedy Algorithm (algorithme_glouton.py)**: The greedy algorithm makes locally optimal choices at each step in the hope of finding a global optimal solution. It selects the best possible decision at each stage without considering long-term consequences.

3. **Genetic Algorithm (algorithme_genetique.py)**: Inspired by natural selection, the genetic algorithm creates a population of potential solutions, applies genetic operations (mutation and crossover), and selects the best-fit individuals for the next generation.

4. **Heuristic Algorithm (algorithme_heuristique.py)**: The heuristic algorithm employs a rule-based approach to make educated guesses and approximate solutions efficiently, though not guaranteed to be optimal.

5. **Recursive Algorithm (algorithme_recursif.py)**: The recursive algorithm calls itself with smaller subsets of the problem until reaching a base case and then backtracks to find the optimal solution.

### Instructions:

1. Ensure you have Python 3 installed on your system.

2. Clone the repository and navigate to the Python versions directory.

3. Each Python file contains a separate implementation of the corresponding algorithm. Run the desired algorithm's file to see the results.

4. The output will display the surveillance agents' positions and the optimal solution found by the algorithm.

### Dependencies:

The algorithms use basic Python libraries and do not require any external dependencies.

### Contribution:

Feel free to contribute by improving the existing algorithms or implementing new surveillance optimization strategies. Create a pull request to propose your changes.

### Credits:

These implementations were developed by [Your Name] and Timothé Dupuch during a contest in our promotion, where we secured the first position among 95 students, achieving the best scores for every instance. However, we eventually discovered that the linear programming approach using Julia outperformed these Python implementations and provided more optimal solutions for the problem.
