"""
Classe para representar um estado do puzzle no Jogo dos Oito.
"""
from typing import List, Optional, Tuple


class EstadoPuzzle:
    """Representa um estado do tabuleiro do Jogo dos Oito."""
    
    # Estado final desejado
    ESTADO_FINAL = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    
    def __init__(
        self, 
        tabuleiro: List[int], 
        estado_pai: Optional['EstadoPuzzle'] = None,
        movimento: Optional[str] = None,
        profundidade: int = 0,
        custo: int = 0,
        heuristica: int = 0
    ):
        """
        Inicializa um estado do puzzle.
        
        Args:
            tabuleiro: Lista de 9 elementos representando o tabuleiro (linha por linha)
            estado_pai: Estado que gerou este estado
            movimento: Direção do movimento ('Cima', 'Baixo', 'Esquerda', 'Direita')
            profundidade: Profundidade na árvore de busca
            custo: Custo acumulado até este estado
            heuristica: Valor da heurística para este estado
        """
        self.tabuleiro = tabuleiro[:]  # Cópia para evitar referências
        self.estado_pai = estado_pai
        self.movimento = movimento
        self.profundidade = profundidade
        self.custo = custo
        self.heuristica = heuristica
        self.f = custo + heuristica  # f(n) = g(n) + h(n) para A*
        
        # Representação única do estado como string
        self._chave = ''.join(str(e) for e in self.tabuleiro)
    
    def __eq__(self, other) -> bool:
        """Compara dois estados pela chave."""
        if not isinstance(other, EstadoPuzzle):
            return False
        return self._chave == other._chave
    
    def __hash__(self) -> int:
        """Permite usar EstadoPuzzle em sets e dicts."""
        return hash(self._chave)
    
    def __lt__(self, other) -> bool:
        """Comparação para ordenação em filas de prioridade."""
        return self.f < other.f
    
    def __str__(self) -> str:
        """Representação em string do tabuleiro formatado."""
        linhas = []
        for i in range(0, 9, 3):
            linha = self.tabuleiro[i:i+3]
            linhas.append(' '.join(str(x) if x != 0 else ' ' for x in linha))
        return '\n'.join(linhas)
    
    def __repr__(self) -> str:
        """Representação para debug."""
        return f"EstadoPuzzle({self.tabuleiro}, f={self.f})"
    
    def eh_objetivo(self) -> bool:
        """Verifica se este estado é o estado objetivo."""
        return self.tabuleiro == self.ESTADO_FINAL
    
    def obter_posicao_vazia(self) -> Tuple[int, int]:
        """
        Retorna a posição (linha, coluna) do espaço vazio (0).
        
        Returns:
            Tupla (linha, coluna) onde linha e coluna são de 0 a 2
        """
        indice = self.tabuleiro.index(0)
        linha = indice // 3
        coluna = indice % 3
        return (linha, coluna)
    
    def obter_indice(self, linha: int, coluna: int) -> int:
        """Converte posição (linha, coluna) para índice linear."""
        return linha * 3 + coluna
    
    def obter_posicao(self, indice: int) -> Tuple[int, int]:
        """Converte índice linear para posição (linha, coluna)."""
        return (indice // 3, indice % 3)

