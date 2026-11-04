import tkinter as tk
from tkinter import messagebox, ttk

import config
from painel_config import JanelaConfiguracoes


class PainelPlanos:
    """Painel flutuante sempre no topo para controlar a navegação e inserção das aulas."""

    def __init__(
        self,
        root,
        aulas,
        on_inserir,
        estrutura_dados=None,
        curso_inicial="",
        unidade_inicial="",
        on_trocar_plano=None,
    ):
        self.root = root
        self.aulas = aulas or []
        self.on_inserir = on_inserir
        self.estrutura_dados = estrutura_dados or {}
        self.curso_atual = curso_inicial
        self.unidade_atual = unidade_inicial
        self.on_trocar_plano = on_trocar_plano

        self.indice = 0
        self.processadas = {
            i for i, a in enumerate(self.aulas)
            if a.get("status") == "preenchida"
        }
        self.executando = False

        self.root.title(config.GUI_TITULO)
        self.root.geometry(
            f"{config.GUI_LARGURA}x{config.GUI_ALTURA}+{config.GUI_X}+{config.GUI_Y}"
        )
        self.root.resizable(False, False)

        if config.GUI_SEMPRE_NO_TOPO:
            self.root.attributes("-topmost", True)

        self._montar_interface()
        self.atualizar()

    def _montar_interface(self):
        self.root.configure(bg="#25272B")

        titulo = tk.Label(
            self.root,
            text="AUTOMATIZADOR DE PLANOS DE AULA",
            bg="#25272B",
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
        )
        titulo.pack(pady=(10, 4))

        # Seletores de Curso e Unidade Curricular
        if self.estrutura_dados:
            seletor_frame = tk.Frame(self.root, bg="#25272B")
            seletor_frame.pack(fill="x", padx=18, pady=(2, 6))

            lbl_curso = tk.Label(
                seletor_frame,
                text="Curso:",
                bg="#25272B",
                fg="#BFC4CC",
                font=("Segoe UI", 8, "bold"),
            )
            lbl_curso.grid(row=0, column=0, sticky="w", pady=(0, 3))

            self.cb_curso = ttk.Combobox(
                seletor_frame,
                values=list(self.estrutura_dados.keys()),
                state="readonly",
                font=("Segoe UI", 8),
            )
            self.cb_curso.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 3))
            seletor_frame.columnconfigure(1, weight=1)

            lbl_uc = tk.Label(
                seletor_frame,
                text="Unidade:",
                bg="#25272B",
                fg="#BFC4CC",
                font=("Segoe UI", 8, "bold"),
            )
            lbl_uc.grid(row=1, column=0, sticky="w", pady=(3, 0))

            self.cb_uc = ttk.Combobox(
                seletor_frame,
                state="readonly",
                font=("Segoe UI", 8),
            )
            self.cb_uc.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(3, 0))

            if self.curso_atual in self.estrutura_dados:
                self.cb_curso.set(self.curso_atual)
                unidades = self.estrutura_dados[self.curso_atual]
                self.cb_uc["values"] = unidades
                if self.unidade_atual in unidades:
                    self.cb_uc.set(self.unidade_atual)
                elif unidades:
                    self.cb_uc.set(unidades[0])
                    self.unidade_atual = unidades[0]

            self.cb_curso.bind("<<ComboboxSelected>>", self._quando_mudar_curso)
            self.cb_uc.bind("<<ComboboxSelected>>", self._quando_mudar_uc)

        # Header do Contador com Navegação Direta de Aula
        contador_frame = tk.Frame(self.root, bg="#25272B")
        contador_frame.pack(pady=(2, 0))

        tk.Label(
            contador_frame,
            text="AULA",
            bg="#25272B",
            fg="#35C98A",
            font=("Segoe UI", 15, "bold"),
        ).pack(side="left")

        self.entry_numero_aula = tk.Entry(
            contador_frame,
            width=3,
            bg="#1E2024",
            fg="#35C98A",
            insertbackground="#35C98A",
            font=("Segoe UI", 14, "bold"),
            justify="center",
            relief="solid",
            bd=1,
        )
        self.entry_numero_aula.pack(side="left", padx=4)
        self.entry_numero_aula.bind("<Return>", lambda _e: self._ir_para_aula_digitada())

        self.lbl_total_aulas = tk.Label(
            contador_frame,
            text="/ 00",
            bg="#25272B",
            fg="#35C98A",
            font=("Segoe UI", 15, "bold"),
        )
        self.lbl_total_aulas.pack(side="left")

        btn_ir = tk.Button(
            contador_frame,
            text="Ir",
            command=self._ir_para_aula_digitada,
            bg="#3A3D43",
            fg="#FFFFFF",
            activebackground="#4A4D53",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2",
            padx=6,
            pady=0,
        )
        btn_ir.pack(side="left", padx=(6, 0))

        self.tipo = tk.Label(
            self.root,
            bg="#25272B",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            wraplength=380,
            justify="center",
        )
        self.tipo.pack(pady=(2, 2))

        self.status = tk.Label(
            self.root,
            bg="#25272B",
            fg="#BFC4CC",
            font=("Segoe UI", 9),
            wraplength=380,
            justify="center",
        )
        self.status.pack(pady=(2, 6))

        nav = tk.Frame(self.root, bg="#25272B")
        nav.pack(fill="x", padx=18)

        self.btn_anterior = tk.Button(
            nav,
            text="◀ ANTERIOR",
            command=self.anterior,
            width=13,
            bg="#3A3D43",
            fg="#FFFFFF",
            activebackground="#4A4D53",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
        )
        self.btn_anterior.pack(side="left", padx=(0, 6))

        self.btn_proxima = tk.Button(
            nav,
            text="PRÓXIMA ▶",
            command=self.proxima,
            width=13,
            bg="#3A3D43",
            fg="#FFFFFF",
            activebackground="#4A4D53",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
        )
        self.btn_proxima.pack(side="right", padx=(6, 0))

        self.btn_inserir = tk.Button(
            self.root,
            text="INSERIR ESTA AULA",
            command=self.inserir,
            height=2,
            bg="#35C98A",
            fg="#10231D",
            activebackground="#4DDBA0",
            activeforeground="#10231D",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
        )
        self.btn_inserir.pack(fill="x", padx=18, pady=(8, 4))

        frame_botoes_secundarios = tk.Frame(self.root, bg="#25272B")
        frame_botoes_secundarios.pack(fill="x", padx=18, pady=(4, 6))

        self.btn_config = tk.Button(
            frame_botoes_secundarios,
            text="⚙ Configurações",
            command=self.abrir_configuracoes,
            bg="#3A3D43",
            fg="#FFFFFF",
            activebackground="#4A4D53",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9),
            padx=8,
            pady=2,
        )
        self.btn_config.pack(side="left")

        self.btn_ocultar = tk.Button(
            frame_botoes_secundarios,
            text="Ocultar painel",
            command=self.ocultar,
            bg="#25272B",
            fg="#BFC4CC",
            activebackground="#25272B",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9),
            padx=8,
            pady=2,
        )
        self.btn_ocultar.pack(side="right")

        self.root.bind("<Left>", lambda _event: self.anterior())
        self.root.bind("<Right>", lambda _event: self.proxima())
        self.root.bind("<Return>", lambda _event: self.inserir())
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

    def abrir_configuracoes(self):
        if hasattr(self, "janela_cfg") and self.janela_cfg is not None and self.janela_cfg.winfo_exists():
            self.janela_cfg.lift()
            return
        self.janela_cfg = JanelaConfiguracoes(
            self.root,
            on_salvar=self._quando_salvar_configuracoes,
        )

    def _quando_salvar_configuracoes(self, _novos_pontos):
        self.status.config(
            text="✓ Configurações de pontos e velocidade atualizadas.",
            fg="#35C98A",
        )

    def _quando_mudar_curso(self, _event=None):
        curso = self.cb_curso.get()
        if curso in self.estrutura_dados:
            self.curso_atual = curso
            unidades = self.estrutura_dados[curso]
            self.cb_uc["values"] = unidades
            if unidades:
                self.cb_uc.set(unidades[0])
                self.unidade_atual = unidades[0]
                self._quando_mudar_uc()

    def _quando_mudar_uc(self, _event=None):
        curso = self.cb_curso.get()
        uc = self.cb_uc.get()
        self.curso_atual = curso
        self.unidade_atual = uc
        if self.on_trocar_plano:
            try:
                novas_aulas = self.on_trocar_plano(curso, uc)
                self.redefinir_aulas(novas_aulas)
            except Exception as erro:
                messagebox.showerror("Erro ao carregar plano", str(erro), parent=self.root)

    def redefinir_aulas(self, novas_aulas):
        self.aulas = novas_aulas or []
        self.indice = 0
        self.processadas = {
            i for i, a in enumerate(self.aulas)
            if a.get("status") == "preenchida"
        }
        self.executando = False
        self.atualizar()

    def aula_atual(self):
        if not self.aulas or self.indice >= len(self.aulas):
            return None
        return self.aulas[self.indice]

    def _ir_para_aula_digitada(self):
        """Pula diretamente para o número da aula digitado no campo Entry."""
        if self.executando or not self.aulas:
            return

        texto = self.entry_numero_aula.get().strip()
        try:
            num = int(texto)
            total = len(self.aulas)
            if 1 <= num <= total:
                self.indice = num - 1
                self.atualizar()
            else:
                messagebox.showwarning(
                    "Número Inválido",
                    f"Por favor, digite um número entre 1 e {total}.",
                    parent=self.root,
                )
                self.atualizar()
        except ValueError:
            messagebox.showwarning(
                "Entrada Inválida",
                "Digite apenas números inteiros para a aula.",
                parent=self.root,
            )
            self.atualizar()

    def atualizar(self):
        total = len(self.aulas)
        atual = self.indice + 1 if total > 0 else 0
        aula = self.aula_atual() or {}

        # Atualiza o campo de número da aula e o total
        self.entry_numero_aula.delete(0, tk.END)
        self.entry_numero_aula.insert(0, f"{atual:02d}")
        self.lbl_total_aulas.config(text=f"/ {total:02d}")

        self.tipo.config(text=aula.get("tipo de aula", "Nenhuma aula carregada"))

        if not self.aulas:
            self.status.config(
                text="Nenhuma aula encontrada para esta unidade.",
                fg="#FF6B4A",
            )
        elif self.indice in self.processadas:
            self.status.config(
                text="✓ Esta aula já foi inserida.",
                fg="#35C98A",
            )
        elif self.executando:
            self.status.config(
                text="Preenchendo o formulário...",
                fg="#FFD15C",
            )
        else:
            self.status.config(
                text="Pronto — abra o Editar no Portal e clique em INSERIR.",
                fg="#BFC4CC",
            )

        self.btn_anterior.config(
            state="normal"
            if self.indice > 0 and not self.executando and total > 0
            else "disabled"
        )
        self.btn_proxima.config(
            state="normal"
            if self.indice < total - 1 and not self.executando and total > 0
            else "disabled"
        )
        self.btn_inserir.config(
            state="disabled" if self.executando or total == 0 else "normal"
        )

    def anterior(self):
        if self.indice > 0 and not self.executando:
            self.indice -= 1
            self.atualizar()

    def proxima(self):
        if self.indice < len(self.aulas) - 1 and not self.executando:
            self.indice += 1
            self.atualizar()

    def inserir(self):
        if self.executando or not self.aulas:
            return

        aula = self.aula_atual()
        self.executando = True
        self.atualizar()
        self.ocultar()

        try:
            self.on_inserir(
                self.indice,
                aula,
                lambda sucesso=True, mensagem="": self.root.after(
                    0,
                    lambda: self._resultado(sucesso, mensagem),
                ),
            )
        except Exception as erro:
            self.executando = False
            self.mostrar()
            self.atualizar()
            messagebox.showerror(
                "Erro ao inserir aula",
                str(erro),
                parent=self.root,
            )

    def _resultado(self, sucesso=True, mensagem=""):
        self.executando = False
        self.mostrar()

        if sucesso:
            self.processadas.add(self.indice)
            total = len(self.aulas)
            # Avança automaticamente para a próxima aula se houver
            if self.indice < total - 1:
                self.indice += 1
                self.atualizar()
                self.status.config(
                    text=f"✓ Aula anterior preenchida! Pronto para a AULA {self.indice + 1:02d}.",
                    fg="#35C98A",
                )
            else:
                self.atualizar()
                self.status.config(
                    text="✓ Última aula preenchida com sucesso! Todas as aulas concluídas.",
                    fg="#35C98A",
                )
        else:
            self.atualizar()
            self.status.config(
                text=f"Erro: {mensagem}",
                fg="#FF6B4A",
            )

    def ocultar(self):
        self.root.withdraw()
        self.root.update_idletasks()

    def mostrar(self):
        self.root.deiconify()
        if config.GUI_SEMPRE_NO_TOPO:
            self.root.attributes("-topmost", True)
        self.root.lift()
        self.root.update_idletasks()

    def fechar(self):
        self.root.destroy()
