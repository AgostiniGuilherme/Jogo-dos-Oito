"""
Arquivo principal do Jogo dos Oito.
Menu principal com opções de execução.
"""
import sys
import os

def mostrar_menu():
    """Mostra o menu de opções."""
    print("\n" + "="*60)
    print("JOGO DOS OITO - MÉTODOS DE BUSCA")
    print("="*60)
    print("\nEscolha uma opção:")
    print("1. Interface Gráfica (Recomendado)")
    print("2. Testes via Linha de Comando")
    print("3. Sair")
    print("\n" + "="*60)

def executar_interface():
    """Executa a interface gráfica."""
    print("\n🚀 Iniciando interface gráfica...")
    print("💡 A janela abrirá em breve. Use os controles para:")
    print("   - Selecionar o método de busca (A* ou Busca em Amplitude)")
    print("   - Executar a busca")
    print("   - Visualizar a solução passo a passo\n")
    
    try:
        from interface import main
        main()
    except ImportError as e:
        print(f"❌ Erro ao importar interface: {e}")
        print("💡 Certifique-se de estar executando da pasta jogo-dos-oito")
    except Exception as e:
        print(f"❌ Erro ao executar interface: {e}")

def executar_testes():
    """Executa os testes via linha de comando."""
    try:
        # Adiciona o diretório atual ao path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from scripts.testar import testar_buscas, testar_validacao
        
        testar_validacao()
        testar_buscas()
    except ImportError as e:
        print(f"❌ Erro ao importar testes: {e}")
        print("💡 Certifique-se de que o arquivo scripts/testar.py existe")
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")

def main():
    """Função principal com menu interativo."""
    while True:
        mostrar_menu()
        escolha = input("Digite sua escolha (1-3): ").strip()
        
        if escolha == "1":
            executar_interface()
            print("\n✅ Interface gráfica fechada. Voltando ao menu...")
            # Continua o loop para mostrar o menu novamente
        elif escolha == "2":
            executar_testes()
            continuar = input("\nPressione ENTER para voltar ao menu ou 'q' para sair: ").strip().lower()
            if continuar == 'q':
                break
        elif escolha == "3":
            print("\n👋 Até logo!")
            sys.exit(0)
        else:
            print("\n❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()

