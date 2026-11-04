import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui

import config

TIPOS_ACAO = ["clique", "duplo clique", "clique direito", "clique e arraste"]


class JanelaConfiguracoes(tk.Toplevel):
    """Janela para gerenciamento visual dos pontos de tela, tipos de clique e velocidade."""

    def __init__(self, parent, on_salvar=None):
        super().__init__(parent)
        self.parent = parent
        self.on_salvar = on_salvar
        self.itens_ui = {}

        self.title("Configurações — Pontos de Tela e Velocidade")
        self.geometry("700x560")
        self.minsize(640, 480)
        self.configure(bg="#1E2024")

        # Mantém no topo se o app principal estiver no topo
        if config.GUI_SEMPRE_NO_TOPO:
            self.attributes("-topmost", True)

        self._montar_interface()
        self._carregar_dados()

    def _montar_interface(self):
        # Cabeçalho
        header_frame = tk.Frame(self, bg="#1E2024")
        header_frame.pack(fill="x", padx=16, pady=(12, 6))

        lbl_titulo = tk.Label(
            header_frame,
            text="CONFIGURAÇÃO DOS PONTOS DE INTERESSE",
            bg="#1E2024",
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
        )
        lbl_titulo.pack(anchor="w")

        lbl_sub = tk.Label(
            header_frame,
            text="Configure as posições (X, Y), o tipo de ação e a espera pós-comando em segundos.",
            bg="#1E2024",
            fg="#9DA5B1",
            font=("Segoe UI", 8),
        )
        lbl_sub.pack(anchor="w", pady=(2, 6))

        # Controle geral de velocidade do mouse (inteiro de 1 a 10)
        speed_frame = tk.Frame(header_frame, bg="#26292E", padx=10, pady=6)
        speed_frame.pack(fill="x", pady=(2, 4))

        lbl_mouse_speed = tk.Label(
            speed_frame,
            text="Velocidade Geral do Mouse (1 a 10):",
            bg="#26292E",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
        )
        lbl_mouse_speed.pack(side="left")

        self.mouse_speed_var = tk.IntVar(value=config.VELOCIDADE_MOUSE)
        self.spin_speed = tk.Spinbox(
            speed_frame,
            from_=1,
            to=10,
            textvariable=self.mouse_speed_var,
            width=5,
            bg="#1E2024",
            fg="#FFFFFF",
            buttonbackground="#3A3D43",
            insertbackground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            justify="center",
        )
        self.spin_speed.pack(side="left", padx=(8, 12))

        lbl_speed_desc = tk.Label(
            speed_frame,
            text="(1 = Lento, 3 = Padrão Rápido [+50%], 10 = Quase Instantâneo)",
            bg="#26292E",
            fg="#9DA5B1",
            font=("Segoe UI", 8),
        )
        lbl_speed_desc.pack(side="left")

        # Área rolável com Canvas
        container = tk.Frame(self, bg="#1E2024")
        container.pack(fill="both", expand=True, padx=16, pady=6)

        self.canvas = tk.Canvas(container, bg="#1E2024", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.frame_conteudo = tk.Frame(self.canvas, bg="#1E2024")
        self.frame_conteudo.bind(
            "<Configure>",
            lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.frame_conteudo,
            anchor="nw",
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Ajusta largura do frame de conteúdo quando o canvas redimensiona
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        # Suporte à rolagem com scroll do mouse
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        # Barra de status
        self.status_var = tk.StringVar(value="Pronto. Clique em 🎯 para capturar coordenadas com o mouse.")
        self.lbl_status = tk.Label(
            self,
            textvariable=self.status_var,
            bg="#16181B",
            fg="#35C98A",
            font=("Segoe UI", 8),
            anchor="w",
            padx=10,
            pady=4,
        )
        self.lbl_status.pack(fill="x", side="bottom")

        # Rodapé de botões
        rodape = tk.Frame(self, bg="#1E2024")
        rodape.pack(fill="x", padx=16, pady=(6, 10), side="bottom")

        btn_salvar = tk.Button(
            rodape,
            text="💾 Salvar Configurações",
            command=self.salvar,
            bg="#35C98A",
            fg="#10231D",
            activebackground="#4DDBA0",
            activeforeground="#10231D",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
        )
        btn_salvar.pack(side="left", padx=(0, 8))

        btn_restaurar = tk.Button(
            rodape,
            text="↺ Restaurar Padrões",
            command=self.restaurar_padroes,
            bg="#3A3D43",
            fg="#FFFFFF",
            activebackground="#4A4D53",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
        )
        btn_restaurar.pack(side="left")

        btn_fechar = tk.Button(
            rodape,
            text="Fechar",
            command=self.destroy,
            bg="#2A2D32",
            fg="#BFC4CC",
            activebackground="#3A3D43",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
        )
        btn_fechar.pack(side="right")

    def _carregar_dados(self):
        pontos = config.obter_config_pontos()
        self.mouse_speed_var.set(config.VELOCIDADE_MOUSE)
        self._construir_linhas(pontos)

    def _construir_linhas(self, pontos):
        # Limpa widgets anteriores
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        self.itens_ui.clear()

        for chave, p in pontos.items():
            card = tk.Frame(self.frame_conteudo, bg="#26292E", relief="flat", bd=1)
            card.pack(fill="x", pady=4, padx=2)

            # Linha superior do card: Label e Combobox de tipo
            top_row = tk.Frame(card, bg="#26292E")
            top_row.pack(fill="x", padx=8, pady=(6, 4))

            lbl_nome = tk.Label(
                top_row,
                text=p.get("label", chave.upper()),
                bg="#26292E",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
            )
            lbl_nome.pack(side="left")

            tipo_var = tk.StringVar(value=p.get("tipo", "clique"))
            cb_tipo = ttk.Combobox(
                top_row,
                textvariable=tipo_var,
                values=TIPOS_ACAO,
                state="readonly",
                width=16,
                font=("Segoe UI", 8),
            )
            cb_tipo.pack(side="right")

            # Linha inferior do card: coordenadas e delay
            bottom_row = tk.Frame(card, bg="#26292E")
            bottom_row.pack(fill="x", padx=8, pady=(0, 6))

            # Coordenadas primárias X, Y
            tk.Label(bottom_row, text="X:", bg="#26292E", fg="#9DA5B1", font=("Segoe UI", 8)).pack(side="left")
            entry_x = tk.Entry(bottom_row, width=5, bg="#1E2024", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Segoe UI", 8))
            entry_x.insert(0, str(p.get("x", 0)))
            entry_x.pack(side="left", padx=(2, 6))

            tk.Label(bottom_row, text="Y:", bg="#26292E", fg="#9DA5B1", font=("Segoe UI", 8)).pack(side="left")
            entry_y = tk.Entry(bottom_row, width=5, bg="#1E2024", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Segoe UI", 8))
            entry_y.insert(0, str(p.get("y", 0)))
            entry_y.pack(side="left", padx=(2, 6))

            btn_capturar = tk.Button(
                bottom_row,
                text="🎯 Posição",
                bg="#3A3D43",
                fg="#FFFFFF",
                activebackground="#4A4D53",
                activeforeground="#FFFFFF",
                font=("Segoe UI", 8),
                relief="flat",
                cursor="hand2",
                command=lambda ex=entry_x, ey=entry_y, k=chave: self._iniciar_captura(ex, ey, k),
            )
            btn_capturar.pack(side="left", padx=(0, 10))

            # Coordenadas secundárias (apenas se for clique e arraste)
            frame_arraste = tk.Frame(bottom_row, bg="#26292E")

            tk.Label(frame_arraste, text="Até X:", bg="#26292E", fg="#9DA5B1", font=("Segoe UI", 8)).pack(side="left")
            entry_x2 = tk.Entry(frame_arraste, width=5, bg="#1E2024", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Segoe UI", 8))
            entry_x2.insert(0, str(p.get("x2", p.get("x", 0))))
            entry_x2.pack(side="left", padx=(2, 6))

            tk.Label(frame_arraste, text="Y:", bg="#26292E", fg="#9DA5B1", font=("Segoe UI", 8)).pack(side="left")
            entry_y2 = tk.Entry(frame_arraste, width=5, bg="#1E2024", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Segoe UI", 8))
            entry_y2.insert(0, str(p.get("y2", p.get("y", 0))))
            entry_y2.pack(side="left", padx=(2, 6))

            btn_capturar2 = tk.Button(
                frame_arraste,
                text="🎯 Fim",
                bg="#3A3D43",
                fg="#FFFFFF",
                activebackground="#4A4D53",
                activeforeground="#FFFFFF",
                font=("Segoe UI", 8),
                relief="flat",
                cursor="hand2",
                command=lambda ex=entry_x2, ey=entry_y2, k=chave: self._iniciar_captura(ex, ey, f"{k} (Fim)"),
            )
            btn_capturar2.pack(side="left", padx=(0, 10))

            # Exibe frame_arraste condicionalmente
            if tipo_var.get() == "clique e arraste":
                frame_arraste.pack(side="left")

            # Delay pós-comando
            tk.Label(bottom_row, text="Espera (s):", bg="#26292E", fg="#9DA5B1", font=("Segoe UI", 8)).pack(side="left", padx=(6, 2))
            entry_delay = tk.Entry(bottom_row, width=6, bg="#1E2024", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Segoe UI", 8))
            entry_delay.insert(0, str(p.get("delay", config.DELAY_CAMPO)))
            entry_delay.pack(side="left")

            # Callback para alternar visualização do arraste ao mudar a combobox
            def _quando_mudar_tipo(_event=None, tv=tipo_var, fa=frame_arraste):
                if tv.get() == "clique e arraste":
                    fa.pack(side="left")
                else:
                    fa.pack_forget()

            cb_tipo.bind("<<ComboboxSelected>>", _quando_mudar_tipo)

            self.itens_ui[chave] = {
                "label": p.get("label", chave),
                "tipo_var": tipo_var,
                "entry_x": entry_x,
                "entry_y": entry_y,
                "entry_x2": entry_x2,
                "entry_y2": entry_y2,
                "entry_delay": entry_delay,
            }

    def _iniciar_captura(self, entry_x, entry_y, nome_campo):
        """Inicia contagem de 2 segundos para capturar a posição do cursor."""
        self.status_var.set(f"Posicione o cursor sobre '{nome_campo}'... Capturando em 2 segundos!")
        self.lbl_status.config(fg="#FFD15C")

        def _concluir():
            x, y = pyautogui.position()
            entry_x.delete(0, tk.END)
            entry_x.insert(0, str(x))
            entry_y.delete(0, tk.END)
            entry_y.insert(0, str(y))
            self.status_var.set(f"✓ Posição capturada para '{nome_campo}': ({x}, {y})")
            self.lbl_status.config(fg="#35C98A")

        self.after(2000, _concluir)

    def salvar(self, mostrar_popup=False):
        """Coleta os valores dos campos, valida e persiste em JSON."""
        novos_pontos = {}

        try:
            for chave, item in self.itens_ui.items():
                x = int(item["entry_x"].get().strip())
                y = int(item["entry_y"].get().strip())
                x2 = int(item["entry_x2"].get().strip()) if item["entry_x2"].get().strip() else x
                y2 = int(item["entry_y2"].get().strip()) if item["entry_y2"].get().strip() else y
                delay = float(item["entry_delay"].get().strip())
                tipo = item["tipo_var"].get().strip()

                ponto_dict = {
                    "label": item["label"],
                    "x": x,
                    "y": y,
                    "tipo": tipo,
                    "delay": delay,
                }
                if tipo == "clique e arraste":
                    ponto_dict["x2"] = x2
                    ponto_dict["y2"] = y2

                novos_pontos[chave] = ponto_dict

            config.salvar_config_pontos(novos_pontos, velocidade_mouse=self.mouse_speed_var.get())

            if self.on_salvar:
                self.on_salvar(novos_pontos)

            self.status_var.set("✓ Configurações salvas e aplicadas à automação com sucesso!")
            self.lbl_status.config(fg="#35C98A")
            if mostrar_popup:
                messagebox.showinfo("Sucesso", "Configurações de pontos e velocidade salvas com sucesso!", parent=self)

        except ValueError as e:
            messagebox.showerror("Erro de Formato", f"Certifique-se de que X, Y e Espera contêm números válidos: {e}", parent=self)

    def restaurar_padroes(self):
        """Restaura as configurações para os padrões de config.py."""
        if messagebox.askyesno("Restaurar", "Deseja restaurar todos os pontos e delays para os padrões?", parent=self):
            config.salvar_config_pontos(config.PONTOS_PADRAO, velocidade_mouse=config.VELOCIDADE_MOUSE_PADRAO)
            self._carregar_dados()
            if self.on_salvar:
                self.on_salvar(config.PONTOS_PADRAO)
            self.status_var.set("✓ Padrões restaurados com sucesso.")
            self.lbl_status.config(fg="#35C98A")
