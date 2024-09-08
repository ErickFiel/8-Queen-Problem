import random

NUMERO_DE_RAINHAS = 8
POPULACAO_PRIMITIVA = 20
TAXA_MUTACAO = 0.3
TAXA_CRUZAMENTO = 0.8  # 80% de chance de cruzar
TAM_INTERFERENCIA_PAI = int(0.1 * POPULACAO_PRIMITIVA)
TAM_INTERFERENCIA_FILHO = POPULACAO_PRIMITIVA - TAM_INTERFERENCIA_PAI
BITS_POR_RAINHA = 3  # 3 bits são suficientes para representar 8 posições

class Situacao:
    def __init__(self):
        self.posicoes_binarias = []
        self.chance = None

    def __mul__(self, outro):
        lista = []
        for _ in range(outro):
            situacao = Situacao()
            situacao.__dict__ = self.__dict__
            lista.append(situacao)
        return lista

def criar_populacao():
    populacao = []
    for _ in range(POPULACAO_PRIMITIVA):
        situacao = Situacao()
        situacao.posicoes_binarias = [random.randint(0, 2**BITS_POR_RAINHA - 1) for _ in range(NUMERO_DE_RAINHAS)]
        populacao.append(situacao)
    return populacao

def binario_para_decimal(binario):
    return int(''.join(map(str, binario)), 2)

def calcular_maximo_conflitos(k):
    return int(k * (k - 1) / 2)

def avaliar(posicoes_binarias):
    posicoes = [binario_para_decimal(list(format(pos, '0' + str(BITS_POR_RAINHA) + 'b'))) for pos in posicoes_binarias]
    conflitos = 0
    for i in range(NUMERO_DE_RAINHAS):
        for j in range(i + 1, NUMERO_DE_RAINHAS):
            diff_linha = abs(posicoes[i] - posicoes[j])
            diff_coluna = abs(i - j)
            if diff_linha == 0 or diff_linha == diff_coluna:
                conflitos += 1
    return conflitos

def calcular_fitness(populacao):
    for individuo in populacao:
        individuo.chance = calcular_maximo_conflitos(NUMERO_DE_RAINHAS) - avaliar(individuo.posicoes_binarias)
    return populacao

def selecionar(populacao):
    potenciais = []
    for individuo in populacao:
        potenciais.extend(individuo * individuo.chance)
    return random.sample(potenciais, POPULACAO_PRIMITIVA)

def cruzar(populacao):
    filhos = []
    for i in range(0, len(populacao), 2):
        pai = populacao[i].posicoes_binarias
        mae = populacao[i + 1].posicoes_binarias
        if random.uniform(0, 1) < TAXA_CRUZAMENTO:
            ponto_cruzamento = random.randrange(0, NUMERO_DE_RAINHAS * BITS_POR_RAINHA)
            menino = Situacao()
            menina = Situacao()
            menino.posicoes_binarias = pai[:ponto_cruzamento] + mae[ponto_cruzamento:]
            menina.posicoes_binarias = mae[:ponto_cruzamento] + pai[ponto_cruzamento:]
            filhos.append(menino)
            filhos.append(menina)
        else:
            # Se não cruzar, apenas adicione os pais como filhos
            filhos.append(Situacao())
            filhos[-1].posicoes_binarias = pai
            filhos.append(Situacao())
            filhos[-1].posicoes_binarias = mae
    return filhos


def mutacao_por_bit_flip(filhos):
    for filho in filhos:
        rnd = random.uniform(0.0, 1.0)
        if rnd < TAXA_MUTACAO:
            # Seleciona uma posição aleatória de bit
            pos = random.randrange(NUMERO_DE_RAINHAS * BITS_POR_RAINHA)
            # Inverte o bit na posição selecionada
            indice_rainha = pos // BITS_POR_RAINHA
            bit_pos = pos % BITS_POR_RAINHA
            binario_rainha = list(format(filho.posicoes_binarias[indice_rainha], '0' + str(BITS_POR_RAINHA) + 'b'))
            binario_rainha[bit_pos] = '1' if binario_rainha[bit_pos] == '0' else '0'
            filho.posicoes_binarias[indice_rainha] = int(''.join(binario_rainha), 2)
    return filhos

def imprimir_solucao(solucao):
    binarios = [format(pos, '0' + str(BITS_POR_RAINHA) + 'b') for pos in solucao]
    print("Solução:", binarios)


if __name__ == "__main__":
    populacao = criar_populacao()
    solucao_encontrada = False
    geracao = 0

    while not solucao_encontrada and geracao < 1000:
        geracao += 1
        populacao_ajustada = calcular_fitness(populacao)
        pais = selecionar(populacao_ajustada)
        filhos = mutacao_por_bit_flip(cruzar(pais))
        filhos_ajustados = calcular_fitness(filhos)
        filhos_ordenados = sorted(filhos_ajustados, key=lambda x: x.chance, reverse=True)  # elitista
        melhor = max(filhos_ordenados, key=lambda x: x.chance)
        pais_ordenados = sorted(pais, key=lambda x: x.chance, reverse=True)
        populacao = pais_ordenados[:TAM_INTERFERENCIA_PAI] + filhos_ordenados[:TAM_INTERFERENCIA_FILHO]
        print("Geração: {0} , melhor abordagem: {1}".format(geracao, melhor.chance))
        if melhor.chance == calcular_maximo_conflitos(NUMERO_DE_RAINHAS):
            solucao_encontrada = True
            imprimir_solucao(melhor.posicoes_binarias)
