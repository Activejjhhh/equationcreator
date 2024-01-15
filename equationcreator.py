import random
import operator
from docx import Document

doc = Document()
variable_names = {
    1: 'Sector Variable Vague',
    2: 'Sector variable precise',
    3: 'Sector Variable Size',
    4: 'Market Variable Vague',
    5: 'Market variable precise',
    6: 'Market Variable Size',
    7: 'Economic Variable Vague',
    8: 'Economic variable precise',
    9: 'Economic Variable Size'
}

# Each individual in the population will be represented as a string of numbers and operations from your list, it also creates  an initial population of random individuals.
def generate_individual(numbers):
    length = random.randint(3, len(numbers))
    individual = []
    num_copy = numbers.copy()
    for _ in range(length):
        num = random.choice(num_copy)
        num_copy.remove(num)
        individual.append(num)
        individual.append(random.choice(['+', '-', '*', '/']))
    return individual[:-1]


def generate_population(numbers, pop_size): 
    return [generate_individual(numbers) for _ in range(pop_size)]


#  #The fitness of an individual will be the inverse of the absolute difference between the evaluated expression and the target number.
def calculate_fitness(individual, target):
    expr = ''.join(map(str, individual))
    try:
        value = eval(expr)
        # Penalize individuals with duplicate numbers
        numbers = [individual[i] for i in range(0, len(individual), 2)]
        if len(numbers) != len(set(numbers)):
            return 0
        return 1 / abs(target - value)
    except (SyntaxError, ZeroDivisionError):
        return 0

# Select individuals for reproduction. Individuals with higher fitness should have a higher chance of being selected.
def select(population, fitnesses):
    return random.choices(population, weights=fitnesses, k=2)

# CCreate new individuals by combining parts of two selected individuals.
def crossover(parent1, parent2):
    index = random.randint(1, len(parent1) - 2)
    child1 = parent1[:index] + parent2[index:]
    child2 = parent2[:index] + parent1[index:]
    return child1, child2

# Randomly change parts of some individuals.
def mutate(individual, numbers):
    index = random.randrange(0, len(individual), 2)
    num_copy = numbers.copy()
    [num_copy.remove(num) for num in individual if num in num_copy]
    if num_copy:
        individual[index] = random.choice(num_copy)
    else:
        individual[index] = random.choice(numbers)


# Replace some individuals in the population with the newly created individuals
def replace(population, children):
    population.sort(key=lambda x: calculate_fitness(x, target))
    population[:2] = children

numbers = [0.97, -42.64, 47.37, 0.47, 0.89, 98.51, 0.47, -783.95, 48.88 ]
target = 346.98

# Assuming 'numbers' is your list of variables
variable_mapping = {numbers[i]: i+1 for i in range(len(numbers))}

def standardize_equation(individual):
    standardized_individual = []
    for item in individual:
        if item in variable_mapping:
            # Replace the number with the corresponding variable name
            standardized_individual.append(variable_names[variable_mapping[item]])
        else:
            standardized_individual.append(item)
    return standardized_individual


# Genetic Algorithm
def genetic_algorithm(numbers, target, pop_size, generations):
    population = generate_population(numbers, pop_size)
    for _ in range(generations):
        fitnesses = [calculate_fitness(individual, target) for individual in population]
        parents = select(population, fitnesses)
        children = crossover(*parents)
        for child in children:
            if random.random() < 0.1:
                mutate(child, numbers)
        replace(population, children)
    best_individual = max(population, key=lambda x: calculate_fitness(x, target))
    standardized_best_individual = standardize_equation(best_individual)

    return ''.join(map(str, best_individual)), ''.join(map(str, standardized_best_individual))  # return both equations


for _ in range(5): #change this for how many equations you want
    original, standardized = genetic_algorithm(numbers, target, pop_size=100, generations=2000)
    standardized_equation = ''.join(standardized)  # Convert list to string
    print(standardized_equation)
    # Add the equation to the Word document
    doc.add_paragraph(standardized_equation)

# Save the document
doc.save("equations.docx")




'''
import itertools
import operator

def calculate(numbers, target):
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    ops_perm = list(itertools.product(ops.keys(), repeat=len(numbers)-1))
    num_perm = list(itertools.permutations(numbers))
    closest = None
    closest_expr = None
    for num in num_perm:
        for op in ops_perm:
            expr = str(num[0])
            for i in range(len(op)):
                expr += op[i] + str(num[i+1])
            try:
                result = eval(expr)
                print(f"Calculation: {expr} = {result}")
                if closest is None or abs(target - result) < abs(target - closest):
                    closest = result
                    closest_expr = expr
            except ZeroDivisionError:
                continue
    return closest, closest_expr

numbers = [float(x) for x in input("Enter a list of numbers separated by space: ").split()]
target = float(input("Enter the target number: "))
closest_value, closest_expr = calculate(numbers, target)
print("The closest value to the target is: ", closest_value)
print("The operations to get to this value are: ", closest_expr)
'''