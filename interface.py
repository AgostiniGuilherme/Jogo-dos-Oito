"""
Interface gráfica para o Jogo dos Oito usando tkinter.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Optional
from estado_puzzle import EstadoPuzzle
from jogo_oito import JogoOito
from busca_amplitude import buscar_solucao_amplitude, ResultadoBusca
from busca_a_estrela import buscar_solucao_a_estrela, imprimir_resultado_a_estrela


class InterfaceJogoOito:
    """Interface gráfica para o Jogo dos Oito."""
    
    # Estado inicial conforme especificação
    ESTADO_INICIAL = [2, 0, 3, 1, 7, 4, 6, 8, 5]
    
    # Estado final padrão (sempre o mesmo, ordenado)
    ESTADO_FINAL = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa a interface.
        
        Args:
            root: Janela principal do tkinter
        """
        self.root = root
        self.root.title("Jogo dos Oito - Métodos de Busca")
        self.root.geometry("650x650")
        self.root.resizable(True, True)
        self.root.minsize(650, 650)
        
        self.estado_atual = self.ESTADO_INICIAL[:]  # Estado atual (pode ser modificado)
        self.jogo = JogoOito(self.estado_atual)
        self.resultado_busca: Optional[ResultadoBusca] = None
        self.indice_caminho_atual = 0
        self.estados_animacao: List[List[int]] = []
        
        self._criar_interface()
        self._atualizar_tabuleiro(self.estado_atual, "Estado Inicial")
    
    def _criar_interface(self):
        """Cria todos os componentes da interface."""
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="8")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(
            frame_principal, 
            text="Jogo dos Oito - Métodos de Busca",
            font=("Arial", 14, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Frame do tabuleiro
        frame_tabuleiro = ttk.LabelFrame(frame_principal, text="Tabuleiro", padding="8")
        frame_tabuleiro.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        self.frame_celulas = ttk.Frame(frame_tabuleiro)
        self.frame_celulas.grid(row=0, column=0)
        
        self.label_estado = ttk.Label(
            frame_tabuleiro, 
            text="Estado Inicial",
            font=("Arial", 10, "bold")
        )
        self.label_estado.grid(row=1, column=0, pady=(10, 0))
        
        # Frame para configuração do estado inicial
        frame_config = ttk.LabelFrame(frame_tabuleiro, text="Configurar Estado Inicial", padding="5")
        frame_config.grid(row=2, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Estado inicial
        ttk.Label(frame_config, text="Estado:").grid(row=0, column=0, padx=5)
        self.entry_estado = ttk.Entry(frame_config, width=30, font=("Arial", 9))
        self.entry_estado.insert(0, ",".join(map(str, self.ESTADO_INICIAL)))
        self.entry_estado.grid(row=0, column=1, padx=5)
        
        # Botões
        btn_aplicar = ttk.Button(
            frame_config,
            text="Aplicar Estado",
            command=self._aplicar_estado_customizado
        )
        btn_aplicar.grid(row=0, column=2, padx=5)
        
        btn_padrao = ttk.Button(
            frame_config,
            text="Usar Padrão",
            command=self._usar_estado_padrao
        )
        btn_padrao.grid(row=0, column=3, padx=5)
        
        # Label de ajuda
        ttk.Label(
            frame_config, 
            text="Digite 9 números (0-8) separados por vírgula. Ex: 2,0,3,1,7,4,6,8,5",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=1, column=0, columnspan=4, pady=(5, 0))
        
        # Cria células do tabuleiro
        self.celulas = []
        for i in range(9):
            linha = i // 3
            coluna = i % 3
            celula = tk.Label(
                self.frame_celulas,
                text="",
                width=3,
                height=1,
                font=("Arial", 20, "bold"),
                relief=tk.RAISED,
                borderwidth=2,
                bg="white"
            )
            celula.grid(row=linha, column=coluna, padx=2, pady=2)
            self.celulas.append(celula)
        
        # Frame de controles
        frame_controles = ttk.LabelFrame(frame_principal, text="Busca", padding="8")
        frame_controles.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Seleção de método
        ttk.Label(frame_controles, text="Método de Busca:").grid(row=0, column=0, padx=5, pady=5)
        self.var_metodo = tk.StringVar(value="A*")
        combo_metodo = ttk.Combobox(
            frame_controles,
            textvariable=self.var_metodo,
            values=["A*", "Busca em Amplitude"],
            state="readonly",
            width=20
        )
        combo_metodo.grid(row=0, column=1, padx=5, pady=5)
        
        # Botão de busca
        btn_buscar = ttk.Button(
            frame_controles,
            text="Buscar Solução",
            command=self._executar_busca
        )
        btn_buscar.grid(row=0, column=2, padx=10, pady=5)
        
        # Botão de reset
        btn_reset = ttk.Button(
            frame_controles,
            text="Reset",
            command=self._resetar
        )
        btn_reset.grid(row=0, column=3, padx=5, pady=5)
        
        # Frame de animação
        frame_animacao = ttk.LabelFrame(frame_principal, text="Visualização da Solução", padding="8")
        frame_animacao.grid(row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Controles de animação
        self.btn_anterior = ttk.Button(
            frame_animacao,
            text="◄ Anterior",
            command=self._anterior_passo,
            state=tk.DISABLED
        )
        self.btn_anterior.grid(row=0, column=0, padx=5)
        
        self.label_passo = ttk.Label(
            frame_animacao,
            text="Passo: 0 / 0",
            font=("Arial", 10)
        )
        self.label_passo.grid(row=0, column=1, padx=10)
        
        self.btn_proximo = ttk.Button(
            frame_animacao,
            text="Próximo ►",
            command=self._proximo_passo,
            state=tk.DISABLED
        )
        self.btn_proximo.grid(row=0, column=2, padx=5)
        
        # Frame de resultados
        frame_resultados = ttk.LabelFrame(frame_principal, text="Resultados da Busca", padding="8")
        frame_resultados.grid(row=5, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.texto_resultados = scrolledtext.ScrolledText(
            frame_resultados,
            width=60,
            height=8,
            font=("Consolas", 8),
            wrap=tk.WORD
        )
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração de grid weights
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(5, weight=1)
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)
    
    def _atualizar_tabuleiro(self, estado: List[int], titulo: str = ""):
        """
        Atualiza a visualização do tabuleiro.
        
        Args:
            estado: Estado do tabuleiro a exibir
            titulo: Título/descrição do estado
        """
        for i, valor in enumerate(estado):
            if valor == 0:
                self.celulas[i].config(text="", bg="#f0f0f0")
            else:
                self.celulas[i].config(text=str(valor), bg="white")
        
        if titulo:
            self.label_estado.config(text=titulo)
    
    def _validar_estado(self, numeros: List[int]) -> bool:
        """Valida se um estado é válido."""
        if len(numeros) != 9:
            return False
        if set(numeros) != set(range(9)):
            return False
        return True
    
    def _aplicar_estado_customizado(self):
        """Aplica um estado inicial customizado inserido pelo usuário."""
        try:
            texto = self.entry_estado.get().strip()
            numeros = [int(x.strip()) for x in texto.split(',')]
            
            # Valida estado
            if not self._validar_estado(numeros):
                messagebox.showerror(
                    "Erro", 
                    "O estado deve ter exatamente 9 números (0-8) sem repetições.\n"
                    "Exemplo: 2,0,3,1,7,4,6,8,5"
                )
                return
            
            # Aplica o estado
            self.estado_atual = numeros[:]
            self.jogo = JogoOito(self.estado_atual)
            self._atualizar_tabuleiro(self.estado_atual, "Estado Inicial Customizado")
            
            # Limpa resultados anteriores
            self._limpar_resultados()
            
            messagebox.showinfo("Sucesso", "Estado inicial aplicado com sucesso!")
            
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Formato inválido! Use apenas números separados por vírgula.\n"
                "Exemplo: 2,0,3,1,7,4,6,8,5"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar estado: {str(e)}")
    
    def _limpar_resultados(self):
        """Limpa os resultados da busca anterior."""
        self.resultado_busca = None
        self.estados_animacao = []
        self.indice_caminho_atual = 0
        self.btn_anterior.config(state=tk.DISABLED)
        self.btn_proximo.config(state=tk.DISABLED)
        self.label_passo.config(text="Passo: 0 / 0")
        self.texto_resultados.delete(1.0, tk.END)
    
    def _usar_estado_padrao(self):
        """Restaura o estado inicial padrão."""
        self.estado_atual = self.ESTADO_INICIAL[:]
        self.jogo = JogoOito(self.estado_atual)
        
        # Atualiza o campo de entrada
        self.entry_estado.delete(0, tk.END)
        self.entry_estado.insert(0, ",".join(map(str, self.ESTADO_INICIAL)))
        
        self._atualizar_tabuleiro(self.estado_atual, "Estado Inicial (Padrão)")
        self._limpar_resultados()
    
    def _executar_busca(self):
        """Executa a busca selecionada."""
        metodo = self.var_metodo.get()
        
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, f"Executando busca {metodo}...\n\n")
        self.root.update()
        
        try:
            if metodo == "A*":
                self.resultado_busca = buscar_solucao_a_estrela(self.estado_atual)
            else:  # Busca em Amplitude
                self.resultado_busca = buscar_solucao_amplitude(self.estado_atual)
            
            if self.resultado_busca.solucao_encontrada:
                # Prepara animação
                self._preparar_animacao()
                
                # Exibe resultados
                self._exibir_resultados()
                
                messagebox.showinfo(
                    "Sucesso",
                    f"Solução encontrada!\n\n"
                    f"Método: {metodo}\n"
                    f"Movimentos: {len(self.resultado_busca.caminho)}\n"
                    f"Nós expandidos: {self.resultado_busca.nos_expandidos}\n"
                    f"Tempo: {self.resultado_busca.tempo_execucao:.4f}s"
                )
            else:
                messagebox.showerror("Erro", "Solução não encontrada!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante a busca:\n{str(e)}")
    
    def _preparar_animacao(self):
        """Prepara os estados para animação do caminho."""
        if not self.resultado_busca or not self.resultado_busca.solucao_encontrada:
            return
        
        # Reconstrói todos os estados do caminho
        self.estados_animacao = [self.estado_atual[:]]
        estado_atual = self.estado_atual[:]
        
        for movimento in self.resultado_busca.caminho:
            novo_estado = self.jogo.mover(estado_atual, movimento)
            if novo_estado:
                self.estados_animacao.append(novo_estado)
                estado_atual = novo_estado
        
        # Vai direto para o último passo (estado final)
        self.indice_caminho_atual = len(self.estados_animacao) - 1
        self._atualizar_controles_animacao()
        
        # Mostra o estado final
        estado_final = self.estados_animacao[self.indice_caminho_atual]
        total_passos = len(self.estados_animacao) - 1
        
        if self.indice_caminho_atual > 0:
            movimento = self.resultado_busca.caminho[self.indice_caminho_atual - 1]
            titulo = f"Passo {self.indice_caminho_atual}/{total_passos} - Movimento: {movimento} (Estado Final)"
        else:
            titulo = f"Estado Final (Passo {self.indice_caminho_atual}/{total_passos})"
        
        self._atualizar_tabuleiro(estado_final, titulo)
    
    def _atualizar_controles_animacao(self):
        """Atualiza os controles de animação."""
        total = len(self.estados_animacao)
        passo_atual = self.indice_caminho_atual
        
        self.label_passo.config(text=f"Passo: {passo_atual} / {total-1}")
        
        self.btn_anterior.config(state=tk.NORMAL if passo_atual > 0 else tk.DISABLED)
        self.btn_proximo.config(
            state=tk.NORMAL if passo_atual < total - 1 else tk.DISABLED
        )
    
    def _anterior_passo(self):
        """Volta para o passo anterior da animação."""
        if self.indice_caminho_atual > 0:
            self.indice_caminho_atual -= 1
            self._atualizar_tabuleiro(
                self.estados_animacao[self.indice_caminho_atual],
                f"Passo {self.indice_caminho_atual}/{len(self.estados_animacao)-1}"
            )
            self._atualizar_controles_animacao()
    
    def _proximo_passo(self):
        """Avança para o próximo passo da animação."""
        if self.indice_caminho_atual < len(self.estados_animacao) - 1:
            self.indice_caminho_atual += 1
            estado = self.estados_animacao[self.indice_caminho_atual]
            
            # Informa o movimento se não for o último
            if self.indice_caminho_atual > 0:
                movimento = self.resultado_busca.caminho[self.indice_caminho_atual - 1]
                titulo = f"Passo {self.indice_caminho_atual}/{len(self.estados_animacao)-1} - Movimento: {movimento}"
            else:
                titulo = f"Passo {self.indice_caminho_atual}/{len(self.estados_animacao)-1}"
            
            if self.indice_caminho_atual == len(self.estados_animacao) - 1:
                titulo += " (Estado Final)"
            
            self._atualizar_tabuleiro(estado, titulo)
            self._atualizar_controles_animacao()
    
    def _exibir_resultados(self):
        """Exibe os resultados da busca na área de texto."""
        if not self.resultado_busca:
            return
        
        resultado = self.resultado_busca
        metodo = self.var_metodo.get()
        
        texto = f"{'='*60}\n"
        texto += f"RESULTADOS DA BUSCA - {metodo}\n"
        texto += f"{'='*60}\n\n"
        
        if resultado.solucao_encontrada:
            texto += f"✓ Solução encontrada!\n\n"
            texto += f"Caminho da solução:\n"
            texto += f"{' → '.join(resultado.caminho)}\n\n"
            texto += f"Número de movimentos: {len(resultado.caminho)}\n"
        else:
            texto += f"✗ Solução não encontrada\n\n"
        
        texto += f"\nEstatísticas:\n"
        texto += f"  • Nós expandidos: {resultado.nos_expandidos}\n"
        texto += f"  • Profundidade da solução: {resultado.profundidade_solucao}\n"
        texto += f"  • Profundidade máxima explorada: {resultado.profundidade_maxima}\n"
        texto += f"  • Tamanho máximo da fronteira: {resultado.tamanho_maximo_fronteira}\n"
        texto += f"  • Tempo de execução: {resultado.tempo_execucao:.8f} segundos\n"
        
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(1.0, texto)
    
    def _resetar(self):
        """Reseta a interface para o estado inicial atual."""
        self.resultado_busca = None
        self.indice_caminho_atual = 0
        self.estados_animacao = []
        self._atualizar_tabuleiro(self.estado_atual, "Estado Inicial")
        self.btn_anterior.config(state=tk.DISABLED)
        self.btn_proximo.config(state=tk.DISABLED)
        self.label_passo.config(text="Passo: 0 / 0")
        self.texto_resultados.delete(1.0, tk.END)


def main():
    """Função principal para iniciar a interface."""
    root = tk.Tk()
    app = InterfaceJogoOito(root)
    root.mainloop()


if __name__ == "__main__":
    main()

