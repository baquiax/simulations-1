import streamlit as st
import random
import math
import matplotlib.pyplot as plt
from typing import List, Tuple

st.title("Algoritmos de Metaheurística")

st.markdown('''```
Alexander Baquiax
12007988
```''')

st.markdown('''
### Problema

$Max  Z = \sum \limits _{i=1}^{N} V_i * X_i $
- $V_i$ representa la cantidad de azucar recolectable en la parcela $i$.
- $X_i$ representa una variable binaria que indica si se sembrará en la parcela $i$ o no.


### Restricciones

$\sum \limits _{i=1}^{N} P_i * X_i \leq W$
- $P_i$ representa el tiempo estimado para cosechar en a parcela $i$.
- $X_i$ representa una variable binaria que indica si se sembrará en la parcela $i$ o no.
- $W$ representa el tiempo disponible para cosechar.

$\sum \limits _{i=1}^{N} V_i * X_i \leq C$
- $V_i$ representa la cantidad de azucar recolectable en la parcela $i$.
- $X_i$ representa una variable binaria que indica si se sembrará en la parcela $i$ o no.
- $C$ representa la cantidad máxima de carga

$X_i \in \{0,1\}$
- $X_i$ representa una variable binaria que indica si se sembrará en la parcela $i$ o no.
''')

class Land:
    def __init__(self, id=0, capacity=100, cost=0.0):
        self.id: int = id
        self.capacity: float = capacity
        self.cost: float = cost

def build_lands(N = 100) -> Tuple[List[Land], float]: 
    lands: List[Land] = []
    lands_capacity: float = 0
    for i in range(1, N + 1):
        capacity = random.uniform(100.00, 1200.00)
        cost = random.uniform(1.0, 10.0)

        lands_capacity += capacity
        lands.append(Land(id=i, capacity=capacity, cost=cost))
        
    return lands, lands_capacity

def  build_pickups(min  = 50, max=100, min_capacity = 1000.00, max_capacity = 2500.00) -> float:
    total_capacity = 0.0
    for i in range(1, random.randint(min, max)):
        total_capacity += random.uniform(min_capacity, max_capacity)
    
    return total_capacity  

def build_people(min = 20, max = 100, hours_person=40) -> int:
    return random.randint(min, max) * hours_person


N = 100 # total lands
lands, V = build_lands(N=100)
W = build_people(min=20, max=40, hours_person=40)
C = build_pickups(min=20, max=30, min_capacity=1000.00, max_capacity=2500.00)

def objective(X: List[float] = []):
    return sum([x_i * v_i for x_i, v_i in zip(X, [land.capacity for land in lands])])

def restriction_a(X: List[float] = []):
    return sum([x_i * p_i for x_i, p_i in zip(X, [land.cost for land in lands])]) <= W

def restriction_b(X: List[float] = []):
    return sum([x_i * v_i for x_i, v_i in zip(X, [land.capacity for land in lands])]) <= C


PENALTY = 100

def fitness(X: List[float] = []):
    fit = objective(X)

    if not restriction_a(X):
        fit -= PENALTY

    if not restriction_b(X):
        fit -= PENALTY 
    
    return fit


genetic, annealing, bees = st.tabs(["🧬 Algoritmo genético", "🥘 Algoritmo de recocido", "🐝 Bees algorithm"])

with genetic:
    POPULATION_SIZE = st.number_input("Tamaño de la generación", min_value=2, max_value=200, value=100, step=1)
    MUTATION_RATE = st.number_input("Probabilidad de mutación", min_value=0.01, max_value=1.0, value=0.1, step=0.1)

    def genetic_algorithm():
        population: List[float] = [[random.choice([0.0, 1.0]) for _ in range(N)] for _ in range(100)]
        fits = []
        for _ in range(POPULATION_SIZE):
            fitness_values = [fitness(X) for X in population]
            
            ## Selection
            parents = random.choices(population, weights=fitness_values, k=POPULATION_SIZE)

            ## Crossover
            offspring = []
            for _ in range(POPULATION_SIZE):
                parent_a, parent_b = random.sample(parents, k=2)
                offspring.append([random.choice([a, b]) for a, b in zip(parent_a, parent_b)])

            ## Mutation
            for i in range(POPULATION_SIZE):
                for j in range(N):
                    if random.random() < MUTATION_RATE:
                        offspring[i][j] = random.choice([0.0, 1.0])

            population = offspring

            best_fit = max(population, key=fitness)
            fits.append(fitness(best_fit))

        return best_fit, fits

    best_fit, fits = genetic_algorithm()

    fig, ax = plt.subplots()
    ax.plot(fits)
    st.pyplot(fig)

    st.info(f"El valor máximo de Z es :green[**{fitness(best_fit)}**] con la solución :orange[**${best_fit}**].")

with annealing:
    INITIAL_TEMPERATURE = st.number_input("Temperatura inicial", min_value=2, max_value=10000, value=1000, step=1)
    FINAL_TEMPERATURE = st.number_input("Temperatura final", min_value=0.01, max_value=1.0, value=0.1, step=0.1)
    ALPHA = st.number_input("Alpha", min_value=0.0100, max_value=1.000, value=0.995, step=0.005)

    def simulated_annealing():
        fits = []
        current_solution = [random.choice([0.0, 1.0]) for _ in range(N)]
        current_value = objective(current_solution)
        best_solution = current_solution.copy()
        best_value = current_value  

        temperature = INITIAL_TEMPERATURE

        while temperature > FINAL_TEMPERATURE:
            next_solution = current_solution
            swap_index = random.randint(0, N - 1)

            next_solution[swap_index] = 1 - next_solution[swap_index]

            if not (restriction_a(next_solution) and restriction_b(next_solution)):
                temperature *= ALPHA
                continue

            next_value = objective(next_solution)

            if next_value > current_value or random.random() < math.exp((next_value - current_value) / temperature):
                current_solution = next_solution
                current_value = next_value

            if current_value > best_value:
                best_solution = current_solution.copy()
                best_value = current_value

            temperature *= ALPHA

            fits.append(current_value)
            
        return best_solution, best_value, fits

    best_solution, best_value, fits = simulated_annealing()

    st.info(f"El valor máximo de Z es :green[**{best_value}**] con la solución :orange[**${best_solution}**].")

    fig, ax = plt.subplots()
    ax.plot(fits)
    st.pyplot(fig)

with bees:
    NUM_BEES = st.number_input("Número de abejas", min_value=2, max_value=100, value=50, step=1)
    NUM_SITES = st.number_input("Número de sitios", min_value=2, max_value=100, value=10, step=1)
    MAX_SITE_VISITS = st.number_input("Máximas visitas", min_value=2, max_value=50, value=10, step=1)
    MAX_ITER = st.number_input("Máximo de simulaciones", min_value=2, max_value=200, value=100, step=1)

    is_valid = lambda x: restriction_a(x) and restriction_b(x)

    def mutate(solution):
        mutated = solution.copy()
        idx = random.randint(0, N-1)
        mutated[idx] = 1 - mutated[idx]
        

        return mutated if is_valid(mutated) else solution

    def bee_algorithm():
        fits = []
        bees = [[random.choice([0.0, 1.0]) for _ in range(N)] for _ in range(NUM_BEES)]
        best_solution = max(bees, key=objective)
        best_value = objective(best_solution)

        for _ in range(MAX_ITER):
            for i in range(NUM_SITES):
                new_solution = mutate(bees[i])
                if objective(new_solution) > objective(bees[i]):
                    bees[i] = new_solution
                    fits.append(objective(new_solution))

            best_sites = sorted(bees, key=objective, reverse=True)[:NUM_SITES]
            for i in range(NUM_BEES - NUM_SITES):
                site = random.choice(best_sites)
                new_solution = mutate(site)
                if objective(new_solution) > objective(site):
                    site = new_solution

            for i in range(NUM_BEES):
                if random.uniform(0, 1) < 0.1:  # 10% probability
                    bees[i] = [random.choice([0, 1]) for _ in range(N)]
                    if not is_valid(bees[i]):
                        bees[i] = best_solution

            current_best = max(bees, key=objective)
            if objective(current_best) > best_value:
                best_solution, best_value = list(current_best), objective(current_best)

        return best_solution, best_value, fits

    best_solution, best_value, fits = bee_algorithm()
    st.info(f"El valor máximo de Z es :green[**{best_value}**] con la solución :orange[**${best_solution}**].")

    fig, ax = plt.subplots()
    ax.plot(fits)
    st.pyplot(fig)