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

line_items = [
    "Cash & Equivalents",
    "Accounts Receivable",
    "Prepaid Expense",
    "PP&E",
    "Right Of Use Assets",
    "Goodwill",
    "Deferred Tax",
    "Accounts Payable",
    "Accrued Liabilities",
    "Taxes Payable",
    "Short Term Debt",
    "Long Term Debt",
    "Lease Liabilities",
    "Retained Earnings",
    "Net Sales/Revenue",
    "COGS",
    "R&D",
    "SG&A",
    "Interest Expense",
    "Nonoperating Income",
    "Tax Provision",
    "Net Income",
    "EPS",
    "Net Income",
    "Depreciation & Amortization",
    "Share-based Compensation",
    "Deferred Tax",
    "Income From Investments",
    "Accounts Receivable",
    "Inventory",
    "Prepaid Expense",
    "Accounts Payable",
    "Purchase of PP&E",
    "Proceeds from Asset Sales",
    "Issuance Of Debts",
    "Payments of Debts"
]


# Each individual in the population will be represented as a string of numbers and operations from your list, it also creates  an initial population of random individuals.
def generate_individual(numbers):
    length = random.randint(3, len(numbers))
    individual = []
    num_copy = [num for num in numbers if num != 0]  # Exclude zero
    for _ in range(length):
        if not num_copy:  # If num_copy is empty
            break  # Skip the current iteration
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



list_of_lists = [
    [0.83, -31.57, 47.07, 0.41, 0.91, 98.35, 0.41, -671.58, 48.73, 90.43],
    [0.99, -44.27, 47.41, 0.48, 0.89, 98.53, 0.48, -811.90, 48.90, -5],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -100],
    [0.97, -42.64, 47.37, 0.47, 0.89, 98.51, 0.47, -793.95, 48.88, 346.98],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -100],
    [0.90, -37.34, 47.23, 0.44, 0.90, 98.44, 0.44, -735.36, 48.81, 86.8],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -100],
    [0.91, -37.71, 47.24, 0.44, 0.90, 98.44, 0.44, -739.49, 48.81, -86.4],
    [0.00, -41.62, 47.35, 0.47, 0.89, 98.50, 0.47, -782.66, 48.87, 17.13],
    [0.87, -35.06, 47.17, 0.43, 0.90, 98.41, 0.43, -710.15, 48.78, -93.77],
    [-0.36, 66.68, 0.00, -0.18, 1.06, 0.00, -0.18, 414.04, 0.00, -100],
    [0.52, -5.89, 46.14, 0.25, 0.95, 97.87, 0.25, -387.88, 48.26, -100],
    [0.96, -42.55, 47.37, 0.47, 0.89, 98.51, 0.47, -792.90, 48.88, -92.02],
    [0.92, -39.11, 47.28, 0.45, 0.90, 98.46, 0.45, -754.97, 48.83, 455.86],
    [1.86, -116.13, 48.71, 0.91, 0.78, 99.18, 0.91, -1605.97, 49.55, 26.61],
    [1.83, -113.44, 48.67, 0.89, 0.78, 99.17, 0.89, -1576.27, 49.53, 36.5],
    [1.62, -96.24, 48.42, 0.79, 0.81, 99.04, 0.79, -1386.21, 49.40, 32,39],
    [1.75, -107.00, 48.58, 0.85, 0.79, 99.12, 0.85, -1505.12, 49.48,  80.06],
    [-0.40, 69.83, 0.00, -0.19, 1.07, 0.00, -0.19, 448.83, 0.00, 84.38],
    [1.88, -117.98, 48.73, 0.92, 0.78, 99.20, 0.92, -1626.43, 49.56, 27.07],
    [0.78, -27.62, 46.95, 0.38, 0.91, 98.29, 0.38, -627.99, 48.67, 94.74],
    [2.73, -188.01, 49.51, 1.33, 0.67, 99.58, 1.33, -2400.27, 49.94, -16.4],
    [2.64, -180.41, 49.44, 1.29, 0.68, 99.55, 1.29, -2316.32, 49.91, -15.29],
    [2.73, -188.01, 49.51, 1.33, 0.67, 99.58, 1.33, -2400.27, 49.94, -53.79],
    [1.50, -86.87, 48.27, 0.73, 0.82, 98.96, 0.73,  -1282.68, 49.33, -45.72],
    [0.98, -43.46, 47.39, 0.48, 0.89, 98.52, 0.48, -803.04, 48.89, -22.5],
    [-0.14, 48.20, 0.00, -0.07, 1.03, 0.00, -0.07, 209.90, 0.00, -259.79],
    [-0.59, 85.60, 0.00, -0.29, 1.09, 0.00, -0.29, 623.10, 0.00, 1.17],
    [-0.29, 60.98, 0.00, -0.14, 1.05, 0.00, -0.14, 351.10, 0.00, -21.3],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0],
    [-1.03, 121.65, 0.00, -0.50, 1.15, 0.00, -0.50, 1021.53, 0.00, -76.96],
    [10.27, -809.78, 52.38, 5.01, -0.29, 100.97, 5.01, -9270.97, 51.33, -78.57],
    [-2.57, 248.56, 0.00, -1.25, 1.34, 0.00, -1.25, 2423.83, 0.00, -67.73],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0],
    [0.00, 0.00,0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0],
]

numbers = list_of_lists[0][:-1] 
target = list_of_lists[0][-1]

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
        if sum(fitnesses) == 0:  # If all fitnesses are zero
            print("All individuals have zero fitness. Skipping...")
            continue  # Skip to the next iteration
        parents = select(population, fitnesses)
        children = crossover(*parents)
        for child in children:
            if random.random() < 0.1:
                mutate(child, numbers)
        replace(population, children)
    best_individual = max(population, key=lambda x: calculate_fitness(x, target))
    standardized_best_individual = standardize_equation(best_individual)

    return ''.join(map(str, best_individual)), ''.join(map(str, standardized_best_individual))  # return both equations



for line_item, sublist in zip(line_items, list_of_lists):
    numbers_in_loop = sublist[:-1]  # All elements except the last one
    target_in_loop = sublist[-1]  # The last element
    variable_mapping = {numbers_in_loop[i]: i+1 for i in range(len(numbers_in_loop))}  # Update the variable mapping
    print(f"Processing {line_item}...")
    for _ in range(2): #change this for how many equations you want
        original, standardized = genetic_algorithm(numbers_in_loop, target_in_loop, pop_size=100, generations=3500)
        standardized_equation = ''.join(standardized)  # Convert list to string
        print(standardized_equation)
        # Add the equation to the Word document
        doc.add_paragraph(standardized_equation)
