"""
Classe principal do Jogo dos Oito com lógica de movimentos.
"""

from typing import List, Optional
from estado_puzzle import EstadoPuzzle


class JogoOito:
    """Gerencia a lógica do Jogo dos Oito."""

    # Movimentos possíveis
    MOVIMENTOS = {
        "Cima": (-1, 0),
        "Baixo": (1, 0),
        "Esquerda": (0, -1),
        "Direita": (0, 1),
    }

    def __init__(self, estado_inicial: List[int]):
        """
        Inicializa o jogo com um estado inicial.

        Args:
            estado_inicial: Lista de 9 elementos representando o estado inicial
        """
        self.estado_inicial = estado_inicial[:]

    def validar_estado(self, estado: List[int]) -> bool:
        """
        Valida se um estado é válido (9 elementos, contém 0-8, sem repetições).

        Args:
            estado: Lista representando o tabuleiro

        Returns:
            True se o estado é válido
        """
        if len(estado) != 9:
            return False
        if set(estado) != set(range(9)):
            return False
        return True

    def mover(self, estado: List[int], movimento: str) -> Optional[List[int]]:
        """
        Realiza um movimento no tabuleiro.

        Args:
            estado: Estado atual do tabuleiro
            movimento: Direção do movimento ('Cima', 'Baixo', 'Esquerda', 'Direita')

        Returns:
            Novo estado após o movimento ou None se movimento inválido
        """
        if movimento not in self.MOVIMENTOS:
            return None

        novo_estado = estado[:]
        linha_atual, coluna_atual = self._obter_posicao_vazia(estado)

        delta_linha, delta_coluna = self.MOVIMENTOS[movimento]
        nova_linha = linha_atual + delta_linha
        nova_coluna = coluna_atual + delta_coluna

        # Verifica se o movimento é válido (dentro dos limites)
        if not (0 <= nova_linha < 3 and 0 <= nova_coluna < 3):
            return None

        # Realiza a troca
        indice_vazio = self._linha_coluna_para_indice(linha_atual, coluna_atual)
        indice_troca = self._linha_coluna_para_indice(nova_linha, nova_coluna)

        novo_estado[indice_vazio], novo_estado[indice_troca] = (
            novo_estado[indice_troca],
            novo_estado[indice_vazio],
        )

        return novo_estado

    def gerar_filhos(self, estado: EstadoPuzzle) -> List[EstadoPuzzle]:
        """
        Gera todos os estados filhos possíveis a partir de um estado.

        Args:
            estado: Estado atual

        Returns:
            Lista de estados filhos válidos
        """
        filhos = []

        for movimento in self.MOVIMENTOS.keys():
            novo_tabuleiro = self.mover(estado.tabuleiro, movimento)

            if novo_tabuleiro is not None:
                filho = EstadoPuzzle(
                    tabuleiro=novo_tabuleiro,
                    estado_pai=estado,
                    movimento=movimento,
                    profundidade=estado.profundidade + 1,
                    custo=estado.custo + 1,
                )
                filhos.append(filho)

        return filhos

    def _obter_posicao_vazia(self, estado: List[int]) -> tuple:
        """Retorna a posição (linha, coluna) do espaço vazio."""
        indice = estado.index(0)
        linha = indice // 3
        coluna = indice % 3
        return (linha, coluna)

    def _linha_coluna_para_indice(self, linha: int, coluna: int) -> int:
        """Converte posição (linha, coluna) para índice linear."""
        return linha * 3 + coluna

    def formatar_tabuleiro(self, estado: List[int]) -> str:
        """
        Formata o tabuleiro para exibição.

        Args:
            estado: Lista representando o tabuleiro

        Returns:
            String formatada do tabuleiro
        """
        linhas = []
        for i in range(0, 9, 3):
            linha = estado[i : i + 3]
            linhas.append(" | ".join(str(x) if x != 0 else " " for x in linha))
        return "\n".join(linhas)
