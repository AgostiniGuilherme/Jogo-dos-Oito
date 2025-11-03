"""
Implementação do algoritmo A* (A-estrela).
Método de busca informado que usa heurística.
"""
import time
import heapq
from typing import List
from estado_puzzle import EstadoPuzzle
from jogo_oito import JogoOito
from heuristica import calcular_heuristica
from busca_amplitude import ResultadoBusca, imprimir_resultado


def buscar_solucao_a_estrela(
    estado_inicial: List[int], 
    metodo_heuristica: str = 'manhattan'
) -> ResultadoBusca:
    """
    Realiza busca A* para encontrar solução do Jogo dos Oito.
    
    O algoritmo A* combina o custo real (g) com uma heurística (h)
    usando f(n) = g(n) + h(n) para escolher o próximo nó a expandir.
    
    Args:
        estado_inicial: Estado inicial do tabuleiro
        metodo_heuristica: Método de heurística ('manhattan' ou 'pecas_fora')
        
    Returns:
        ResultadoBusca com informações da busca
    """
    resultado = ResultadoBusca()
    inicio_tempo = time.time()
    
    jogo = JogoOito(estado_inicial)
    estado_inicial_puzzle = EstadoPuzzle(tabuleiro=estado_inicial)
    
    # Calcula heurística inicial
    estado_inicial_puzzle.heuristica = calcular_heuristica(
        estado_inicial_puzzle, 
        metodo_heuristica
    )
    estado_inicial_puzzle.f = estado_inicial_puzzle.custo + estado_inicial_puzzle.heuristica
    
    # Verifica se já é o estado objetivo
    if estado_inicial_puzzle.eh_objetivo():
        resultado.solucao_encontrada = True
        resultado.profundidade_solucao = 0
        resultado.tempo_execucao = time.time() - inicio_tempo
        return resultado
    
    # Fila de prioridade (heap) para A*
    # Usa (f, contador, estado) para garantir ordenação estável
    contador = 0
    fila_prioridade = [(estado_inicial_puzzle.f, contador, estado_inicial_puzzle)]
    estados_visitados = set()
    estados_visitados.add(estado_inicial_puzzle._chave)
    
    while fila_prioridade:
        # Atualiza tamanho máximo da fronteira
        if len(fila_prioridade) > resultado.tamanho_maximo_fronteira:
            resultado.tamanho_maximo_fronteira = len(fila_prioridade)
        
        # Remove o estado com menor f (prioridade)
        _, _, estado_atual = heapq.heappop(fila_prioridade)
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
            
            # Calcula heurística para o filho
            filho.heuristica = calcular_heuristica(filho, metodo_heuristica)
            filho.f = filho.custo + filho.heuristica
            
            # Adiciona à fila se não foi visitado
            if filho._chave not in estados_visitados:
                estados_visitados.add(filho._chave)
                contador += 1
                heapq.heappush(fila_prioridade, (filho.f, contador, filho))
    
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


def imprimir_resultado_a_estrela(resultado: ResultadoBusca, metodo_heuristica: str = 'manhattan'):
    """Imprime os resultados da busca A* de forma formatada."""
    print("=" * 50)
    print("BUSCA A* (A-ESTRELA)")
    print(f"Heurística: {metodo_heuristica.upper()}")
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

