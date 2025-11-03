"""
Implementação da Busca em Amplitude (BFS - Breadth-First Search).
Método de busca cego/não informado.
"""
import time
from collections import deque
from typing import List, Optional, Tuple
from estado_puzzle import EstadoPuzzle
from jogo_oito import JogoOito


class ResultadoBusca:
    """Armazena os resultados de uma busca."""
    
    def __init__(self):
        self.solucao_encontrada = False
        self.caminho = []
        self.nos_expandidos = 0
        self.profundidade_solucao = 0
        self.profundidade_maxima = 0
        self.tamanho_maximo_fronteira = 0
        self.tempo_execucao = 0.0


def buscar_solucao_amplitude(estado_inicial: List[int]) -> ResultadoBusca:
    """
    Realiza busca em amplitude (BFS) para encontrar solução do Jogo dos Oito.
    
    A busca em amplitude explora todos os nós de um nível antes de passar
    para o próximo nível, garantindo encontrar a solução com menor número de movimentos.
    
    Args:
        estado_inicial: Estado inicial do tabuleiro
        
    Returns:
        ResultadoBusca com informações da busca
    """
    resultado = ResultadoBusca()
    inicio_tempo = time.time()
    
    jogo = JogoOito(estado_inicial)
    estado_inicial_puzzle = EstadoPuzzle(tabuleiro=estado_inicial)
    
    # Verifica se já é o estado objetivo
    if estado_inicial_puzzle.eh_objetivo():
        resultado.solucao_encontrada = True
        resultado.profundidade_solucao = 0
        resultado.tempo_execucao = time.time() - inicio_tempo
        return resultado
    
    # Fila para BFS (FIFO)
    fila = deque([estado_inicial_puzzle])
    estados_visitados = set()
    estados_visitados.add(estado_inicial_puzzle._chave)
    
    while fila:
        # Atualiza tamanho máximo da fronteira
        if len(fila) > resultado.tamanho_maximo_fronteira:
            resultado.tamanho_maximo_fronteira = len(fila)
        
        # Remove o primeiro da fila (FIFO)
        estado_atual = fila.popleft()
        resultado.nos_expandidos += 1
        
        # Atualiza profundidade máxima
        if estado_atual.profundidade > resultado.profundidade_maxima:
            resultado.profundidade_maxima = estado_atual.profundidade
        
        # Gera filhos
        filhos = jogo.gerar_filhos(estado_atual)
        
        for filho in filhos:
            # Verifica se é o objetivo
            if filho.eh_objetivo():
                resultado.solucao_encontrada = True
                resultado.profundidade_solucao = filho.profundidade
                
                # Reconstrói o caminho
                resultado.caminho = _reconstruir_caminho(filho)
                resultado.tempo_execucao = time.time() - inicio_tempo
                return resultado
            
            # Adiciona à fila se não foi visitado
            if filho._chave not in estados_visitados:
                estados_visitados.add(filho._chave)
                fila.append(filho)
    
    # Não encontrou solução (não deveria acontecer para o Jogo dos Oito)
    resultado.tempo_execucao = time.time() - inicio_tempo
    return resultado


def _reconstruir_caminho(estado_final: EstadoPuzzle) -> List[str]:
    """
    Reconstrói o caminho do estado inicial até o estado final.
    
    Args:
        estado_final: Estado objetivo encontrado
        
    Returns:
        Lista de movimentos do estado inicial ao final
    """
    caminho = []
    estado_atual = estado_final
    
    while estado_atual.estado_pai is not None:
        caminho.insert(0, estado_atual.movimento)
        estado_atual = estado_atual.estado_pai
    
    return caminho


def imprimir_resultado(resultado: ResultadoBusca):
    """Imprime os resultados da busca de forma formatada."""
    print("=" * 50)
    print("BUSCA EM AMPLITUDE (BFS)")
    print("=" * 50)
    
    if resultado.solucao_encontrada:
        print(f"✓ Solução encontrada!")
        print(f"Caminho: {resultado.caminho}")
        print(f"Número de movimentos: {len(resultado.caminho)}")
    else:
        print("✗ Solução não encontrada")
    
    print(f"Nós expandidos: {resultado.nos_expandidos}")
    print(f"Profundidade da solução: {resultado.profundidade_solucao}")
    print(f"Profundidade máxima explorada: {resultado.profundidade_maxima}")
    print(f"Tamanho máximo da fronteira: {resultado.tamanho_maximo_fronteira}")
    print(f"Tempo de execução: {resultado.tempo_execucao:.8f} segundos")
    print("=" * 50)

