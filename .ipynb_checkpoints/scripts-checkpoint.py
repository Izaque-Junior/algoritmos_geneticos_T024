import numpy as np 

############################################################################################################################################
#                                                       Código Inicial                                                                    #
############################################################################################################################################

def minimiza_energia(quantidade_atomos):
    """
    Cria matrizes a partir da quantidade de possíveis combinações entre o número de átomos que formarão a molécula.
    Args:
        quantidade_atomos: número inteiro de átomos que compõem a molécula desejada.
        
    return:
        retorna uma lista de matrizes candidatas.
    """
    matrizes = []
    
    # Gerar todas as possíveis matrizes
    for i in range(2 ** (quantidade_atomos * (quantidade_atomos - 1) // 2)):
        H = np.zeros((quantidade_atomos, quantidade_atomos))
        bits = list(format(i, 'b').zfill(quantidade_atomos * (quantidade_atomos - 1) // 2))
        bit_index = 0
        
        # Preencher a matriz com os valores adequados
        for j in range(quantidade_atomos):
            for k in range(j + 1, quantidade_atomos):
                if bits[bit_index] == '1':
                    H[j][k] = -1
                    H[k][j] = -1
                bit_index += 1
        
        matrizes.append(H)
    
    return matrizes

def testar_matrizes(matrizes):
    """
    Calcula a energia total de uma molécula.
    
    Args:
        matrizes: lista contendo as matrizes candidatas para a molécula buscada.
    
    return:
        retorna a matriz com menor energia total.
    """
    t_menor = float('inf')  # Set initial smallest t_total to infinity
    melhor_matrix = None  # Initialize the matrix with the smallest t_total

    for H in matrizes:
        eigenvals = np.linalg.eigvals(H)
        autovalores = sorted(eigenvals.real)
        
        e = H.shape[0]
        
        if e % 2 == 0:
            ocupados = e // 2 
        elif e % 2 == 1:
            ocupados = e // 2 + 1
        
        t_total = 0
        for n in range(e//2):
            t_total += 2 * autovalores[n]
        if(e%2==1):
            t_total += autovalores[e//2]

        if t_total < t_menor:
            melhor_auto = autovalores
            t_menor = t_total
            melhor_matrix = H

    print(60 * '-', 'Resultado', 60 * '-')
    print(f'A matriz com o menor t_total associado é:')
    print(melhor_matrix)
    print(f'Com os autovalores {melhor_auto}')
    print(f'E com o valor associado de {t_menor}')
    
    return melhor_matrix

############################################################################################################################################
#                                                       From Molecules to Molecules                                                        #
############################################################################################################################################

def create_upper_triangular_binary_matrix(size):
    '''
    Cria uma matrix triangular superior, com diagonal principal igual a 0.
    
    Args: 
        size = Ordem da matriz desejada
    
    return:
        matriz triangular superior de ordem igual a desejada
    '''
    
    matrix = np.random.randint(2, size=(size, size))
    np.fill_diagonal(matrix, 0)  # Diagonal = 0
    upper_triangular_matrix = np.triu(matrix)
    
    return upper_triangular_matrix

def initialize_population(pop_size, matrix_size):
    '''
    Inicializa a população, e já transforma uma matriz triangular
    superior em uma matriz simétrica somando ela com a sua transposta.
    
    Args: 
        tamanho da população: quantidade de indivíduos requisitados para a população
        ordem da matriz: quantidade de átomos da molécula
    
    return: 
        retorna uma população de matrizes simétricas
    '''
    population = []
    for _ in range(pop_size):
        upper_triangular = create_upper_triangular_binary_matrix(matrix_size)
        combined_matrix = upper_triangular + upper_triangular.T
        population.append((upper_triangular, combined_matrix))
        
    return population

def fitness(combined_matrix):
    '''
    Calcula a energia total em uma matriz.
    
    Arg: 
        combined_matrix: matriz simétrica NxN.
        
    return: 
        retorna o valor da energia da matriz dada.
    '''
    eigenvals = np.linalg.eigvals(combined_matrix)
    autovalores = sorted(eigenvals.real)
    
    e = combined_matrix.shape[0]
    
    if e % 2 == 0:
        ocupados = e // 2 
        
    elif e % 2 == 1:
        ocupados = (e // 2) + 1
        
    #CÁLCULO DA ENERGIA TOTAL SEGUNDO O MÉTODO DE HUCKEL
    t_total = 0
    
    for n in range(e//2):
        t_total += 2 * autovalores[n]
        
    if(e%2==1):
        t_total += autovalores[e//2]
        
    return t_total

############################################################################################################################################
#                                                       Seleção                                                                            #
############################################################################################################################################

# Tournament selection
def tournament_selection(population, fitnesses, k=3):
    '''
    Seleciona um indivíduo da população utilizando o método de seleção por torneio.

    Args: 
        population: Lista de matrizes simétricas.
        fitnesses: Lista de valores de fitness correspondentes à população.
        k: Número de indivíduos a serem selecionados para o torneio (default = 3).
    
    return: 
        retorna o indivíduo da população com maior valor de fitness entre os selecionados para o torneio.
    '''
    
    selected_indices = np.random.choice(len(population), k, replace=False)
    selected = [population[i] for i in selected_indices]
    selected_fitnesses = [fitnesses[i] for i in selected_indices]
    
    return selected[np.argmin(selected_fitnesses)]

############################################################################################################################################
#                                                       Cruzamento                                                                         #
############################################################################################################################################

def crossover(parent1, parent2, chance_cruzamento):
    '''
    Realiza o cruzamento entre dois pais para gerar um filho.

    Args:
        parent1: Tupla contendo a matriz triangular superior e a matriz simétrica correspondente do primeiro pai.
        parent2: Tupla contendo a matriz triangular superior e a matriz simétrica correspondente do segundo pai.
    
    return: 
        retorna uma tupla contendo a matriz triangular superior e a matriz simétrica correspondente do filho gerado.
    '''
    
    upper_tri1, _ = parent1
    upper_tri2, _ = parent2
    if random.random() < chance_cruzamento:
        child1 = []
        child2 = []
        size = upper_tri1.shape[0]
        
        crossover_point = np.random.randint(1, size)
        
        child1 = np.zeros((size, size)) #criando matriz de zeros para o filho 1
        child2 = np.zeros((size, size)) #criando matriz de zeros para o filho 2
        

        # Copy upper part from parent1 and lower part from parent2
        for i in range(size):
            for j in range(size):
                if j >= crossover_point:
                    child1[i, j] = upper_tri1[i, j]
                    child2[i, j] = upper_tri2[i, j]
                else:
                    child1[i, j] = upper_tri2[i, j]
                    child2[i, j] = upper_tri2[i, j]

        child1_combined = child1 + child1.T
        child2_combined = child2 + child2.T
        
        filho1 = (child1, child1_combined)
        filho2 = (child2, child2_combined)
        
        return filho1, filho2
    
    else:
        return parent1, parent2
    
############################################################################################################################################
#                                                       Mutação                                                                            #

def mutate_upper_triangular_binary(individuos, chance_mutacao):
    '''
    Muta uma matrix triangular superior, trocando um elemento 
    aleatório (fora da diagonal) de 0 para 1, ou vice-versa.

    Args: 
        individuos: lista contendo as matrizes triangulares superiores
        chance_mutacao: float que define o limiar da chance de ocorrer mutação no indivíduo
        
    return: 
        retorna uma matriz triangular superior com uma mutação
    '''
    size = 0
    for individuo in individuos:
        size = individuo.shape[0]
        if random.random() < chance_mutacao:

            # Escolhe um elemento aleatório (tirando a diagonal)
            i = np.random.randint(0, size - 1)
            j = np.random.randint(i + 1, size)  # Assegura que estará acima da diagonal principal

            # Flipa o valor do elemento escolhido
            individuo[i, j] = 1 - individuo[i, j]

############################################################################################################################################


