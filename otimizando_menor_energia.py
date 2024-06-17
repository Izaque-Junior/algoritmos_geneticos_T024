import numpy as np 
import networkx as nx
from pyvis import network as net

############################################################################################################################################
#                                                       Código Inicial                                                                     #
############################################################################################################################################

def draw_graph(networkx_graph,notebook=True,output_filename='graph.html',show_buttons=True,only_physics_buttons=True):
    """
    This function accepts a networkx graph object,
    converts it to a pyvis network object preserving its node and edge attributes,
    and both returns and saves a dynamic network visualization.
    
    Args:
        networkx_graph: The graph to convert and display
        notebook: Display in Jupyter? #(isso aqui continua??)
        output_filename: Where to save the converted network
        show_buttons: Show buttons in saved version of network? #(isso aqui continua??)
        only_physics_buttons: Show only buttons controlling physics of network?
    """
    
    # make a pyvis network
    pyvis_graph = net.Network(notebook=notebook)
    
    # for each node and its attributes in the networkx graph
    for node,node_attrs in networkx_graph.nodes(data=True):
        pyvis_graph.add_node(str(node),**node_attrs)
        
    # for each edge and its attributes in the networkx graph
    for source,target,edge_attrs in networkx_graph.edges(data=True):
        # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
        if not 'value' in edge_attrs and not 'width' in edge_attrs and 'weight' in edge_attrs:
            # place at key 'value' the weight of the edge
            edge_attrs['value']=edge_attrs['weight']
        # add the edge
        pyvis_graph.add_edge(str(source),str(target),**edge_attrs)
        
    # turn buttons on
    if show_buttons:
        if only_physics_buttons:
            pyvis_graph.show_buttons(filter_=['physics'])
        else:
            pyvis_graph.show_buttons()
    
    # return and also save
    return pyvis_graph.show(output_filename)

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
        
    #CÁLCULO ENERGIA TOTAL SEGUNDO O MÉTODO DE HUCKEL
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


############################################################################################################################################
#                                                       Mutação                                                                            #
############################################################################################################################################


