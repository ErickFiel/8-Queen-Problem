from random import *

# Constantes
POPULATION_SIZE = 20
MUTATION_PROBABILITY = 0.03
GENERATIONS_NUMBER = 1000
n = 8

# Seleção dos pais
def roulette_wheel_selection(population: list[int], fitness_values: list[int], population_size: int) -> list[int]:
    """
    Roulette Wheel is a Parent Selection technique. The chromosome is selected according to its fitness probability.
    The wheel position is generated as a random number between 0 and 1, because we are dealing with probabilities.
    """
    fitness_sum = sum(fitness_values)
    fitness_probs = [(fitness / fitness_sum) for fitness in fitness_values]
    wheel_position = uniform(0, 1)
    cumulative_prob = 0

    for i in range(population_size):
        cumulative_prob += fitness_probs[i]
        if cumulative_prob >= wheel_position:
            return population[i]

# Conversor decimal para binário
def decimal_to_binary(chromosome: list[int]) -> list[int]:
    """
    Converte uma lista de números decimais para uma lista binária,
    onde cada número decimal é representado por exatamente 3 bits.
    """
    binary_chromosome = []
    for num in chromosome:
        binary_rep = format(num, '03b')  # Sempre gera exatamente 3 bits
        binary_chromosome.extend([int(bit) for bit in binary_rep])
    return binary_chromosome

# Conversor binário para decimal
def binary_to_decimal(chromosome: list[int], size: int = 8) -> list[int]:
    """
    Converte um cromossomo binário de volta para uma lista de inteiros,
    onde cada conjunto de 3 bits representa a posição de uma rainha (0-7).
    """
    decimal_chromosome = []
    for i in range(0, size * 3, 3):  # Itera em blocos de 3 bits
        decimal_value = chromosome[i] * 4 + chromosome[i+1] * 2 + chromosome[i+2]
        decimal_chromosome.append(decimal_value)
    
    return decimal_chromosome

# Mutação
def bit_flip_mutation(chromosome: list[int]) -> list[int]:
    
    # Converter de decimal para binário
    binary_chromosome = decimal_to_binary(chromosome)
    
    # Seleciona um índice aleatório do cromossomo binário
    index = randint(0, len(binary_chromosome) - 1)
    
    # Realiza o flip do bit selecionado
    binary_chromosome[index] = 1 - binary_chromosome[index]

    # Converter de binário para decimal
    decimal_chromosome = binary_to_decimal(binary_chromosome)
    
    return decimal_chromosome

# Cruzamento
def one_point_crossover(chromosome1: list[int], chromosome2: list[int], size: int) -> tuple[list[int], list[int]]:
    """
    Perform one-point crossover and ensure resulting chromosomes stay within valid range.
    """
    point = randint(1, size-2)

    child1 = chromosome1[:point] + chromosome2[point:]
    child2 = chromosome2[:point] + chromosome1[point:]

    # Garante que os valores dos filhos estão entre 0 e 7
    child1 = [min(max(0, gene), 7) for gene in child1]
    child2 = [min(max(0, gene), 7) for gene in child2]
    
    return child1, child2

 
# Cromossomo
def generate_chromosome(size: int):
    """
    Generates new random chromosome using sample() function from random library.
    Chromosomes will now range from 0 to 7.
    """
    return sample(range(0, size), size)

def generate_population(population_size: int, chromosome_size: int, mutation_probability: float, old_population: list[list[int]], fitness_values: list[list[int]]) -> list[list[int]]:
    """
    Generate new population using the old one and its fitness values. It iterates until the new population
    reaches the desired population size, But here it only iterates the half because in each iteration we
    produce two new childs. Steps of generating new childs are as following:
    1. Select the parents using Roulette Wheel Selection method.
    2. Make crossover between these parents using Two-Point Crossover.
    3. For each child generate a random number between 0 and 1 to know if we should mutate it or not.
    4. If the mutation will happen we use the Random Reset Mutation.
    5. Add these childs to the new population.
    """
    new_population = []
    
    for _ in range(int(population_size/2)):
        parent1 = roulette_wheel_selection(old_population, fitness_values, population_size)
        parent2 = roulette_wheel_selection(old_population, fitness_values, population_size)

        child1, child2 = one_point_crossover(parent1, parent2, chromosome_size)
        if random() < mutation_probability:
            child1 = bit_flip_mutation(child1)
        if random() < mutation_probability:
            child2 = bit_flip_mutation(child2)
        
        new_population.append(child1)
        new_population.append(child2)

    return new_population

# Fitness
def fitness(n: int, chromosome: list[int], max_fitness: int) -> int:
    """
    It checks for each queen if there is a conflict with the other queens or not, sum those conflicts, then
    subtract them from the max fitness to get the chromosome fitness.
    """
    conflicts = 0

    for i in range(n):
        for j in range(i+1, n):
            if chromosome[i] == chromosome[j] or abs(chromosome[i]-chromosome[j]) == abs(i-j):
                conflicts += 1

    return int(max_fitness-conflicts)

if n != 2 and n != 3:  # Check if the problem can be solved or not
	
	max_fitness = (n * (n-1)) / 2  # get the max fitness can be reached for n
	
	# Generate the initial population
	population = [generate_chromosome(n) for _ in range(POPULATION_SIZE)]
	
	# Evaluate the fitness value for each chromosome 
	fitness_values = [fitness(n, chromosome, max_fitness) for chromosome in population]
	
	# Save the fittest found chromosome, it's used when there is no solution found
	fittest_found = population[fitness_values.index(max(fitness_values))]
	
	generation = 0
	
	while generation != GENERATIONS_NUMBER and max_fitness != fitness(n, fittest_found, max_fitness):
		population = generate_population(POPULATION_SIZE, n, MUTATION_PROBABILITY, population, fitness_values)
		fitness_values = [fitness(n, chromosome, max_fitness) for chromosome in population]
		
		# Check if the fittest one in the current population is more fit than the saved one
		current_fittest = population[fitness_values.index(max(fitness_values))]
		if fitness(n, current_fittest, max_fitness) > fitness(n, fittest_found, max_fitness):
			fittest_found = current_fittest
		
		generation += 1

	# Check if there is a solution in the last population to show
	if max_fitness in fitness_values:
		print(f"Solved in generation {generation}")
		solution = population[fitness_values.index(max_fitness)]
		print(f"Found solution = {solution}") 
	
	else:
		print(f"No solution is found in {GENERATIONS_NUMBER} generations!!")
		print(f"Fittest found solution = {fittest_found}")
