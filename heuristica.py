"""
Funções heurísticas para o Jogo dos Oito.
"""
from typing import List
from estado_puzzle import EstadoPuzzle


def distancia_manhattan(estado: List[int]) -> int:
    """
    Calcula a distância de Manhattan para um estado do puzzle.
    
    A distância de Manhattan é a soma das distâncias horizontais e verticais
    de cada peça até sua posição correta.
    
    Args:
        estado: Lista representando o tabuleiro atual
        
    Returns:
        Valor da heurística (soma das distâncias de Manhattan)
    """
    estado_objetivo = EstadoPuzzle.ESTADO_FINAL
    
    distancia_total = 0
    
    # Para cada posição no tabuleiro atual
    for indice_atual, valor in enumerate(estado):
        if valor == 0:  # Ignora o espaço vazio
            continue
        
        # Encontra onde este valor deveria estar
        indice_objetivo = estado_objetivo.index(valor)
        
        # Calcula posições (linha, coluna)
        linha_atual = indice_atual // 3
        coluna_atual = indice_atual % 3
        linha_objetivo = indice_objetivo // 3
        coluna_objetivo = indice_objetivo % 3
        
        # Distância de Manhattan: |linha_atual - linha_objetivo| + |coluna_atual - coluna_objetivo|
        distancia = abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)
        distancia_total += distancia
    
    return distancia_total


def pecas_fora_do_lugar(estado: List[int]) -> int:
    """
    Conta quantas peças estão fora de lugar (sem contar o espaço vazio).
    
    Esta é uma heurística mais simples, mas menos informativa que Manhattan.
    
    Args:
        estado: Lista representando o tabuleiro atual
        
    Returns:
        Número de peças fora de lugar
    """
    estado_objetivo = EstadoPuzzle.ESTADO_FINAL
    
    pecas_fora = 0
    for i, valor in enumerate(estado):
        if valor != 0 and estado[i] != estado_objetivo[i]:
            pecas_fora += 1
    
    return pecas_fora


def calcular_heuristica(estado: EstadoPuzzle, metodo: str = 'manhattan') -> int:
    """
    Calcula a heurística para um estado usando o método especificado.
    
    Args:
        estado: Estado do puzzle
        metodo: Método de heurística ('manhattan' ou 'pecas_fora')
        
    Returns:
        Valor da heurística
    """
    if metodo == 'manhattan':
        return distancia_manhattan(estado.tabuleiro)
    elif metodo == 'pecas_fora':
        return pecas_fora_do_lugar(estado.tabuleiro)
    else:
        raise ValueError(f"Método de heurística desconhecido: {metodo}")

