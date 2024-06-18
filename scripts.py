import numpy as np 
import random

############################################################################################################################################
#                                                       Código 'Hamiltonian for n-site molecules' [2]                                                                    #
############################################################################################################################################

def energiaMin(qtdAtomos):
    """
    Cria matrizes a partir da quantidade de possíveis combinações entre o número de átomos que formarão a molécula.
    Args:
        qtdAtomos: número inteiro de átomos que compõem a molécula desejada.
         
    return:
        retorna uma lista de matrizes candidatas.
    """
    matrizes = []
    
    # Gerar todas as possíveis matrizes
    for i in range(2 ** (qtdAtomos * (qtdAtomos - 1) // 2)):
        H = np.zeros((qtdAtomos, qtdAtomos))
        bits = list(format(i, 'b').zfill(qtdAtomos * (qtdAtomos - 1) // 2)) #[5]
        bit_index = 0
        
        # Preencher a matriz com os valores adequados
        for j in range(qtdAtomos):
            for k in range(j + 1, qtdAtomos):
                if bits[bit_index] == '1':
                    H[j][k] = -1
                    H[k][j] = -1
                bit_index += 1
        
        matrizes.append(H)
    
    return matrizes

def testaMatriz(matrizes):
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
#                                                       Criando matriz triangular superior [13]                                            #
############################################################################################################################################

def criaTriu(size):
    '''
    Cria uma matrix triangular superior, com diagonal principal igual a 0.
    
    Args: 
        size = Ordem da matriz desejada
    
    return:
        matriz triangular superior de ordem igual a desejada
    '''
    
    matrix = np.random.randint(2, size=(size, size))
    np.fill_diagonal(matrix, 0)  # Diagonal = 0
    Triu = np.triu(matrix)
    
    return Triu

############################################################################################################################################
#                                                       Iniciando população                                                                #
############################################################################################################################################

def iniciaPopu(pop_size, matrix_size):
    '''
    Inicializa a população, e já transforma uma matriz triangular
    superior em uma matriz simétrica somando ela com a sua transposta.
    
    Args: 
        tamanho da população: quantidade de indivíduos requisitados para a população
        ordem da matriz: quantidade de átomos da molécula
    
    return: 
        retorna uma população de matrizes simétricas
    '''
    populacao = []
    for _ in range(pop_size):
        upper_triangular = criaTriu(matrix_size)
        hamiltoniano = upper_triangular + upper_triangular.T
        populacao.append((upper_triangular, hamiltoniano))
        
    return populacao

############################################################################################################################################
#                                                       Calculando função objetivo                                                        #
############################################################################################################################################

def fitness(hamiltoniano):
    '''
    Calcula a energia total em uma matriz.
    
    Arg: 
        hamiltoniano: matriz simétrica NxN.
        
    return: 
        retorna o valor da energia da matriz dada.
    '''
    eigenvals = np.linalg.eigvals(hamiltoniano)
    autovalores = sorted(eigenvals.real)
    
    e = hamiltoniano.shape[0]
        
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
def selecaoTorneio(populacao, valoresFit, k=3):
    '''
    Seleciona um indivíduo da população utilizando o método de seleção por torneio.

    Args: 
        populacao: Lista de matrizes simétricas.
        valoresFit: Lista de valores de fitness correspondentes à população.
        k: Número de indivíduos a serem selecionados para o torneio (default = 3).
    
    return: 
        retorna o indivíduo da população com maior valor de fitness entre os selecionados para o torneio.
    '''
    
    indexSelecionados = np.random.choice(len(populacao), k, replace=False)
    selecionados = [populacao[i] for i in indexSelecionados]
    valoresFitSelecionados = [valoresFit[i] for i in indexSelecionados]
    
    return selecionados[np.argmin(valoresFitSelecionados)] #[4]

############################################################################################################################################
#                                                       Cruzamento                                                                         #
############################################################################################################################################

def cruzamento(pai1, pai2, chanceCruzamento):
    '''
    Realiza o cruzamento entre dois pais para gerar um filho.

    Args:
        pai1: Tupla contendo a matriz triangular superior e a matriz simétrica correspondente do primeiro pai.
        pai2: Tupla contendo a matriz triangular superior e a matriz simétrica correspondente do segundo pai.
    
    return: 
        retorna uma tupla contendo a matriz triangular superior e a matriz simétrica correspondente do filho gerado.
    '''
    
    upper_tri1, _ = pai1
    upper_tri2, _ = pai2
    if random.random() < chanceCruzamento:
        child1 = []
        child2 = []
        size = upper_tri1.shape[0]
        
        pontoCruzamento = np.random.randint(1, size)
            
        child1 = np.zeros((size, size)) #criando matriz de zeros para o filho 1
        child2 = np.zeros((size, size)) #criando matriz de zeros para o filho 2
        

        # Copy upper part from pai1 and lower part from pai2
        for i in range(size):
            for j in range(size):
                if j >= pontoCruzamento:
                    child1[i, j] = upper_tri1[i, j]
                    child2[i, j] = upper_tri2[i, j]
                else:
                    child1[i, j] = upper_tri2[i, j]
                    child2[i, j] = upper_tri1[i, j]

        child1_combined = child1 + child1.T
        child2_combined = child2 + child2.T
        
        filho1 = (child1, child1_combined)
        filho2 = (child2, child2_combined)
        
        return filho1, filho2
    
    else:
        return pai1, pai2
    
############################################################################################################################################
#                                                       Mutação                                                                            #
############################################################################################################################################

def mutaTriu(individuos, chance_mutacao):
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
