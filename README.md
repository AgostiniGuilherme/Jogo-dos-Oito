# 🎮 Jogo dos Oito - Métodos de Busca em IA

Projeto acadêmico implementando algoritmos de busca aplicados ao **Jogo dos Oito (8-Puzzle)**. Este projeto demonstra a diferença entre métodos de busca cegos e informados, comparando a eficiência do algoritmo **Busca em Amplitude (BFS)** com o **A* (A-estrela)**.

## 📋 Sobre o Projeto

O Jogo dos Oito é um quebra-cabeça clássico que consiste em reorganizar um tabuleiro de 3x3 contendo 8 peças numeradas e 1 espaço vazio até alcançar uma configuração objetivo.

### 🎯 Objetivos

- Implementar **Busca em Amplitude (BFS)** - método cego/não informado
- Implementar **A* (A-estrela)** - método informado com heurística
- Comparar a eficiência dos dois métodos
- Fornecer interface gráfica interativa para visualização

## 🚀 Requisitos

- **Python 3.6+**
- **tkinter** (geralmente incluído no Python)
- Não requer dependências externas

## 📦 Instalação

1. Clone ou baixe o repositório
2. Navegue até a pasta do projeto:
   ```bash
   cd jogo-dos-oito
   ```

## ▶️ Como Executar

### Método Principal (Recomendado)

Execute o arquivo principal que exibe um menu interativo:

```bash
python main.py
```

**Menu de opções:**
1. **Interface Gráfica** - Abre a interface gráfica interativa
2. **Testes via Linha de Comando** - Executa testes comparativos
3. **Sair** - Encerra o programa

> 💡 **Dica:** Ao fechar a interface gráfica, o programa retorna ao menu principal automaticamente.

### Executar Diretamente

**Apenas Interface Gráfica:**
```bash
python -c "from interface import main; main()"
```

**Apenas Testes:**
```bash
python scripts/testar.py
```

## 🎮 Como Usar

### Interface Gráfica

1. Execute `python main.py` e escolha a opção **1**
2. A janela abrirá mostrando o estado inicial do tabuleiro
3. **(Opcional)** Configure um estado inicial customizado:
   - Digite 9 números (0-8) separados por vírgula no campo de texto
   - Exemplo: `1,2,3,4,5,6,7,8,0`
   - Clique em "Aplicar Estado"
4. Selecione o método de busca (A* ou Busca em Amplitude)
5. Clique em "Buscar Solução"
6. Use os botões "◄ Anterior" e "Próximo ►" para navegar pela solução passo a passo
7. Veja as estatísticas detalhadas na área de resultados

### Testes via Linha de Comando

Execute os testes para ver uma comparação detalhada dos algoritmos:

```bash
python scripts/testar.py
```

**Resultado esperado:**
- ✅ **Busca em Amplitude**: ~91 nós expandidos, solução em 7 movimentos
- ✅ **A* (Manhattan)**: ~7 nós expandidos, solução em 7 movimentos
- ⚡ **A* é aproximadamente 13x mais eficiente!**

## 📊 Estado Inicial e Final

### Estado Inicial Padrão:
```
┌─────┬─────┬─────┐
│  2  │     │  3  │
├─────┼─────┼─────┤
│  1  │  7  │  4  │
├─────┼─────┼─────┤
│  6  │  8  │  5  │
└─────┴─────┴─────┘
```

### Estado Final (Objetivo):
```
┌─────┬─────┬─────┐
│  1  │  2  │  3  │
├─────┼─────┼─────┤
│  8  │     │  4  │
├─────┼─────┼─────┤
│  7  │  6  │  5  │
└─────┴─────┴─────┘
```

## 🏗️ Estrutura do Projeto

```
jogo-dos-oito/
├── main.py                    # Arquivo principal (menu interativo)
├── interface.py               # Interface gráfica com tkinter
├── estado_puzzle.py          # Classe para representar estados do puzzle
├── jogo_oito.py             # Lógica do jogo e movimentos
├── heuristica.py            # Funções heurísticas (Manhattan Distance)
├── busca_amplitude_bfs.py   # Implementação BFS (Busca em Amplitude)
├── busca_a_estrela.py       # Implementação A* (A-estrela)
├── README.md                # Este arquivo
├── scripts/                  # Scripts auxiliares
│   └── testar.py            # Script de testes comparativos
└── apresentacao/            # Documentação de apresentação
    ├── APRESENTACAO.md      # Guia completo para apresentação
    └── COMANDOS_RAPIDOS.md  # Comandos rápidos para demonstração
```

## 🔍 Métodos de Busca Implementados

### 1. Busca em Amplitude (BFS)

**Características:**
- ✅ Método **cego/não informado**
- ✅ Explora nível por nível (FIFO - First In, First Out)
- ✅ **Garante solução ótima** (menor número de movimentos)
- ✅ Não utiliza informações sobre o objetivo

**Desvantagens:**
- ❌ Expande muitos nós desnecessários
- ❌ Pode ser lento para problemas grandes

**Pseudocódigo:**
```
fila = [estado_inicial]
enquanto fila não vazia:
    estado = fila.remover_primeiro()
    se estado é objetivo: retornar solução
    para cada filho de estado:
        fila.adicionar(filho)
```

### 2. A* (A-estrela)

**Características:**
- ✅ Método **informado** com heurística
- ✅ Usa f(n) = g(n) + h(n)
  - **g(n)**: custo real do caminho
  - **h(n)**: heurística (distância de Manhattan)
- ✅ **Garante solução ótima** (se heurística é admissível)
- ✅ **Muito mais eficiente** que BFS

**Heurística: Distância de Manhattan**
- Calcula a distância de cada peça até sua posição correta
- Soma todas as distâncias
- É **admissível** (nunca superestima o custo)

**Comparação de Performance:**
| Método | Nós Expandidos | Tempo | Movimentos |
|--------|---------------|-------|------------|
| BFS | ~91 | ~0.002s | 7 |
| A* | ~7 | ~0.001s | 7 |

## ✨ Funcionalidades

- 🎨 **Interface gráfica interativa** com visualização do tabuleiro
- 🔧 **Configuração de estado inicial customizado**
- 📊 **Comparação em tempo real** dos dois métodos
- 📈 **Estatísticas detalhadas** (nós expandidos, tempo, profundidade)
- 🎬 **Visualização passo a passo** da solução encontrada
- 🧪 **Scripts de teste** para análise comparativa

## 🎓 Conceitos de IA Demonstrados

Este projeto demonstra conceitos fundamentais de Inteligência Artificial:

- **Busca em Espaço de Estados**
- **Busca Cega vs. Informada**
- **Heurísticas Admissíveis**
- **Otimização de Algoritmos**
- **Análise de Complexidade**

## 📝 Exemplo de Uso

```python
# Exemplo de uso programático
from busca_a_estrela import buscar_solucao_a_estrela

estado_inicial = [2, 0, 3, 1, 7, 4, 6, 8, 5]
resultado = buscar_solucao_a_estrela(estado_inicial)

if resultado.solucao_encontrada:
    print(f"Solução encontrada em {len(resultado.caminho)} movimentos!")
    print(f"Caminho: {' → '.join(resultado.caminho)}")
    print(f"Nós expandidos: {resultado.nos_expandidos}")
```

## 🤝 Contribuições

Este é um projeto acadêmico. Contribuições e sugestões são bem-vindas!

## 📄 Licença

Este projeto é de uso acadêmico/educacional.

## 👨‍💻 Autor

Guilherme Noronha de Agostini

Projeto desenvolvido para demonstração de métodos de busca em Inteligência Artificial.

