"""
Script para testar os algoritmos de busca via linha de comando.
"""
import sys
import os

# Adiciona o diretório pai ao path para importar os módulos principais
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from estado_puzzle import EstadoPuzzle
from jogo_oito import JogoOito
from busca_amplitude import buscar_solucao_amplitude, imprimir_resultado
from busca_a_estrela import buscar_solucao_a_estrela, imprimir_resultado_a_estrela


def formatar_tabuleiro(estado: list) -> str:
    """Formata o tabuleiro para exibição."""
    linhas = []
    for i in range(0, 9, 3):
        linha = estado[i:i+3]
        linhas.append(' | '.join(str(x) if x != 0 else ' ' for x in linha))
    return '\n'.join(linhas)


def testar_buscas():
    """Testa ambos os algoritmos de busca."""
    # Estado inicial conforme especificação
    estado_inicial = [2, 0, 3, 1, 7, 4, 6, 8, 5]
    
    print("\n" + "="*60)
    print("JOGO DOS OITO - TESTE DOS ALGORITMOS DE BUSCA")
    print("="*60)
    
    print("\n📋 ESTADO INICIAL:")
    print(formatar_tabuleiro(estado_inicial))
    
    print("\n🎯 ESTADO OBJETIVO:")
    print(formatar_tabuleiro(EstadoPuzzle.ESTADO_FINAL))
    
    print("\n" + "="*60)
    print("TESTE 1: BUSCA EM AMPLITUDE (BFS)")
    print("="*60 + "\n")
    
    resultado_bfs = buscar_solucao_amplitude(estado_inicial)
    imprimir_resultado(resultado_bfs)
    
    if resultado_bfs.solucao_encontrada:
        print("\n📊 Caminho da solução:")
        print(" → ".join(resultado_bfs.caminho))
        print(f"\nTotal de movimentos: {len(resultado_bfs.caminho)}")
    
    print("\n" + "="*60)
    print("TESTE 2: BUSCA A* (A-ESTRELA)")
    print("="*60 + "\n")
    
    resultado_astar = buscar_solucao_a_estrela(estado_inicial, metodo_heuristica='manhattan')
    imprimir_resultado_a_estrela(resultado_astar, metodo_heuristica='manhattan')
    
    if resultado_astar.solucao_encontrada:
        print("\n📊 Caminho da solução:")
        print(" → ".join(resultado_astar.caminho))
        print(f"\nTotal de movimentos: {len(resultado_astar.caminho)}")
    
    print("\n" + "="*60)
    print("COMPARAÇÃO DOS MÉTODOS")
    print("="*60)
    print(f"\n{'Método':<25} {'Nós Expandidos':<20} {'Tempo (s)':<15} {'Movimentos':<10}")
    print("-"*70)
    print(f"{'Busca em Amplitude':<25} {resultado_bfs.nos_expandidos:<20} {resultado_bfs.tempo_execucao:<15.6f} {len(resultado_bfs.caminho) if resultado_bfs.solucao_encontrada else 'N/A':<10}")
    print(f"{'A* (Manhattan)':<25} {resultado_astar.nos_expandidos:<20} {resultado_astar.tempo_execucao:<15.6f} {len(resultado_astar.caminho) if resultado_astar.solucao_encontrada else 'N/A':<10}")
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS!")
    print("="*60 + "\n")


def testar_validacao():
    """Testa a validação de estados."""
    print("\n" + "="*60)
    print("TESTE DE VALIDAÇÃO")
    print("="*60)
    
    jogo = JogoOito([2, 0, 3, 1, 7, 4, 6, 8, 5])
    
    # Teste com estado válido
    estado_valido = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    print(f"\nEstado válido: {jogo.validar_estado(estado_valido)}")
    print(formatar_tabuleiro(estado_valido))
    
    # Teste com estado inválido
    estado_invalido = [1, 2, 3, 8, 0, 4, 7, 6]  # Faltando um elemento
    print(f"\nEstado inválido (faltando elemento): {jogo.validar_estado(estado_invalido)}")
    
    # Teste de movimentos
    print("\n" + "="*60)
    print("TESTE DE MOVIMENTOS")
    print("="*60)
    
    estado_teste = [2, 0, 3, 1, 7, 4, 6, 8, 5]
    print("\nEstado inicial:")
    print(formatar_tabuleiro(estado_teste))
    
    movimentos = ['Cima', 'Baixo', 'Esquerda', 'Direita']
    for movimento in movimentos:
        novo_estado = jogo.mover(estado_teste, movimento)
        if novo_estado:
            print(f"\nMovimento: {movimento}")
            print(formatar_tabuleiro(novo_estado))
        else:
            print(f"\nMovimento {movimento}: Inválido (fora dos limites)")


if __name__ == "__main__":
    print("\n🚀 Iniciando testes do Jogo dos Oito...\n")
    
    # Testa validação e movimentos
    testar_validacao()
    
    # Testa os algoritmos de busca
    testar_buscas()
    
    print("\n💡 DICA: Para usar a interface gráfica, execute:")
    print("   python main.py")
    print("   ou")
    print("   python scripts/executar.py\n")

