from random import *

# Constantes
TAMANHO_POPULACAO = 20
PROBABILIDADE_MUTACAO = 0.03
NUMERO_GERACOES = 1000
n = 8

# Seleção dos pais
def selecao_roleta(populacao: list[int], valores_fitness: list[int], tamanho_populacao: int) -> list[int]:
    soma_fitness = sum(valores_fitness)
    prob_fitness = [(fitness / soma_fitness) for fitness in valores_fitness]
    posicao_roda = uniform(0, 1)
    prob_cumulativa = 0

    for i in range(tamanho_populacao):
        prob_cumulativa += prob_fitness[i]
        if prob_cumulativa >= posicao_roda:
            return populacao[i]

# Conversor decimal para binário
def decimal_para_binario(cromossomo: list[int]) -> list[int]:
    cromossomo_binario = []
    for num in cromossomo:
        rep_binaria = format(num, '03b') # Sempre gera exatamente 3 bits
        cromossomo_binario.extend([int(bit) for bit in rep_binaria])
    return cromossomo_binario

# Conversor binário para decimal
def binario_para_decimal(cromossomo: list[int], tamanho: int = 8) -> list[int]:

    cromossomo_decimal = [] 
    for i in range(0, tamanho * 3, 3):  # Itera em blocos de 3 bits
        valor_decimal = cromossomo[i] * 4 + cromossomo[i+1] * 2 + cromossomo[i+2]
        cromossomo_decimal.append(valor_decimal)
    
    return cromossomo_decimal

# Mutação
def mutacao_bit_flip(cromossomo: list[int]) -> list[int]:
    
    # Converter de decimal para binário
    cromossomo_binario = decimal_para_binario(cromossomo)
    
    # Seleciona um índice aleatório do cromossomo binário
    index = randint(0, len(cromossomo_binario) - 1)
    
    # Realiza o flip do bit selecionado
    cromossomo_binario[index] = 1 - cromossomo_binario[index]

    # Converter de binário para decimal
    cromossomo_decimal = binario_para_decimal(cromossomo_binario)
    
    return cromossomo_decimal

# Cruzamento
def cruzamento_ponto_corte(cromossomo1: list[int], cromossomo2: list[int], tamanho: int) -> tuple[list[int], list[int]]:

    ponto = randint(1, tamanho-2)

    filho1 = cromossomo1[:ponto] + cromossomo2[ponto:]
    filho2 = cromossomo2[:ponto] + cromossomo1[ponto:]
    
    return filho1, filho2

# Cromossomo
def gerar_cromossomo (tamanho: int):

    return sample(range(0, tamanho), tamanho)

# Gerar a população
def gerar_populacao(tamanho_populacao: int, tamanho_cromossomo: int, probabilidade_mutacao: float, antiga_populacao: list[list[int]], valores_fitness: list[list[int]]) -> list[list[int]]:

    nova_populacao = []
    
    for _ in range(int(tamanho_populacao/2)):
        pai1 = selecao_roleta(antiga_populacao, valores_fitness, tamanho_populacao)
        pai2 = selecao_roleta(antiga_populacao, valores_fitness, tamanho_populacao)  

        filho1, filho2 = cruzamento_ponto_corte(pai1, pai2, tamanho_cromossomo)
        if random() < probabilidade_mutacao:
            filho1 = mutacao_bit_flip(filho1)
        if random() < probabilidade_mutacao:
            filho2 = mutacao_bit_flip(filho2)
        
        nova_populacao.append(filho1)
        nova_populacao.append(filho2)

    return nova_populacao

# Fitness
def fitness(n: int, cromossomo: list[int], fitness_max: int) -> int:

    conflitos = 0

    for i in range(n):
        for j in range(i+1, n):
            if cromossomo[i] == cromossomo[j] or abs(cromossomo[i]- cromossomo[j]) == abs(i-j):
                conflitos += 1

    return int(fitness_max - conflitos)

def queen_problem(n: int):
    
    fitness_max = (n * (n - 1)) / 2

    # Gerar a população incial
    populacao = [gerar_cromossomo(n) for _ in range(TAMANHO_POPULACAO)]
    
    # Avalia o valor fitness para cada cromossomo
    valores_fitness = [fitness(n, cromossomo, fitness_max) for cromossomo in populacao] 
	
	  # Salva o cromossomo mais apto encontrado , é usado quando não tem uma solução encontrada
    mais_apto_encontrado = populacao[valores_fitness.index(max(valores_fitness))]
    
    geracao = 0

    while geracao != NUMERO_GERACOES and fitness_max != fitness(n, mais_apto_encontrado, fitness_max):
      populacao = gerar_populacao(TAMANHO_POPULACAO, n, PROBABILIDADE_MUTACAO, populacao, valores_fitness)
      valores_fitness = [fitness(n, cromossomo, fitness_max) for cromossomo in populacao]
      
      mais_apto_atual = populacao[valores_fitness.index(max(valores_fitness))]
      
      if fitness(n, mais_apto_atual, fitness_max) > fitness(n, mais_apto_encontrado, fitness_max):
        mais_apto_encontrado = mais_apto_atual
    
      geracao += 1

	  # Check if there is a solution in the last population to show 
    if fitness_max in valores_fitness:
      print(f"Solucionado na geração:{geracao}") 
      solucao = populacao[valores_fitness.index(fitness_max)]
      print(f"Solução encontrada = {solucao}")
    else:
      print(f"Nenhuma solução encontrada em {NUMERO_GERACOES} gerações!!") 
      print(f"Solução mais apta encontrada: {mais_apto_encontrado}")


for i in range(50):
  queen_problem(n)
  print("\n")
