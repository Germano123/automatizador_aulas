import tkinter as tk
from tkinter import messagebox

import config


class PainelPlanos:
    """Painel flutuante sempre no topo para controlar o índice das aulas."""

    def __init__(self, root, aulas, on_inserir):
        self.root = root
        self.aulas = aulas
        self.on_inserir = on_inserir
        self.indice = 0
        self.processadas = set()
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
        titulo.pack(pady=(12, 4))

        self.contador = tk.Label(
            self.root,
            bg="#25272B",
            fg="#35C98A",
            font=("Segoe UI", 18, "bold"),
        )
        self.contador.pack()

        self.tipo = tk.Label(
            self.root,
            bg="#25272B",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            wraplength=320,
            justify="center",
        )
        self.tipo.pack(pady=(2, 2))

        self.status = tk.Label(
            self.root,
            bg="#25272B",
            fg="#BFC4CC",
            font=("Segoe UI", 9),
            wraplength=330,
            justify="center",
        )
        self.status.pack(pady=(2, 8))

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
        self.btn_inserir.pack(fill="x", padx=18, pady=(10, 6))

        self.btn_ocultar = tk.Button(
            self.root,
            text="Ocultar painel",
            command=self.ocultar,
            bg="#25272B",
            fg="#BFC4CC",
            activebackground="#25272B",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
        )
        self.btn_ocultar.pack()

        # Atalhos enquanto a GUI estiver em foco.
        self.root.bind("<Left>", lambda _event: self.anterior())
        self.root.bind("<Right>", lambda _event: self.proxima())
        self.root.bind("<Return>", lambda _event: self.inserir())
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

    def aula_atual(self):
        if not self.aulas:
            return None
        return self.aulas[self.indice]

    def atualizar(self):
        total = len(self.aulas)
        atual = self.indice + 1
        aula = self.aula_atual() or {}

        self.contador.config(text=f"AULA {atual:02d} / {total:02d}")
        self.tipo.config(text=aula.get("tipo de aula", "Sem título"))

        if self.indice in self.processadas:
            self.status.config(text="✓ Esta aula já foi inserida.", fg="#35C98A")
        else:
            self.status.config(text="Pronto — abra o Editar no Portal e clique em INSERIR.", fg="#BFC4CC")

        self.btn_anterior.config(
            state="normal" if self.indice > 0 and not self.executando else "disabled"
        )
        self.btn_proxima.config(
            state="normal" if self.indice < total - 1 and not self.executando else "disabled"
        )
        self.btn_inserir.config(state="disabled" if self.executando else "normal")

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
        self.status.config(text="Preenchendo o formulário...", fg="#FFD15C")
        self.atualizar()

        try:
            self.on_inserir(self.indice, aula, self._resultado)
        except Exception as erro:
            self.executando = False
            self.atualizar()
            messagebox.showerror("Erro ao inserir aula", str(erro), parent=self.root)

    def _resultado(self, sucesso=True, mensagem=""):
        self.executando = False

        if sucesso:
            self.processadas.add(self.indice)
            self.status.config(
                text="✓ Aula preenchida. Confira no Portal antes de salvar.",
                fg="#35C98A",
            )
        else:
            self.status.config(text=f"Erro: {mensagem}", fg="#FF6B4A")

        self.atualizar()

    def ocultar(self):
        self.root.withdraw()

    def mostrar(self):
        self.root.deiconify()
        self.root.lift()

    def fechar(self):
        self.root.destroy()
