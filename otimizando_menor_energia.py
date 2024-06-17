import numpy as np 
import networkx as nx
from pyvis import network as net

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