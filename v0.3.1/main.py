import threading
from pathlib import Path
import tkinter as tk

import config
from automacao import preencher_aula
from gui import PainelPlanos
import gerenciador_dados

plano_ativo = {
    "caminho_csv": None,
    "curso": "",
    "unidade": "",
}


def trocar_plano(curso, unidade):
    """Callback disparado pela interface quando o usuário troca de Curso/UC."""
    caminho = gerenciador_dados.obter_caminho_csv(curso, unidade, config.DADOS_DIR)
    plano_ativo["caminho_csv"] = caminho
    plano_ativo["curso"] = curso
    plano_ativo["unidade"] = unidade
    print(f"\n[INFO] Plano selecionado: {curso} — {unidade}")
    print(f"[INFO] Arquivo: {caminho.resolve()}")
    return gerenciador_dados.carregar_csv(caminho)


def executar_insercao(indice, aula, callback):
    """Executa PyAutoGUI em thread para não congelar a GUI."""

    def trabalho():
        caminho_csv = plano_ativo.get("caminho_csv")
        try:
            preencher_aula(aula)
            if caminho_csv:
                gerenciador_dados.atualizar_status(caminho_csv, indice, "preenchida", "")
            # Tkinter deve ser atualizado na thread principal.
            callback(True, "")
        except Exception as erro:
            if caminho_csv:
                try:
                    gerenciador_dados.atualizar_status(caminho_csv, indice, "erro", str(erro))
                except Exception:
                    pass
            callback(False, str(erro))

    threading.Thread(target=trabalho, daemon=True).start()


def main():
    estrutura = gerenciador_dados.listar_estrutura(config.DADOS_DIR)

    curso_inicial = ""
    unidade_inicial = ""
    aulas = []

    if estrutura:
        curso_inicial = list(estrutura.keys())[0]
        unidades = estrutura[curso_inicial]
        unidade_inicial = unidades[0] if unidades else ""

        if unidade_inicial:
            caminho_inicial = gerenciador_dados.obter_caminho_csv(
                curso_inicial,
                unidade_inicial,
                config.DADOS_DIR,
            )
            plano_ativo["caminho_csv"] = caminho_inicial
            plano_ativo["curso"] = curso_inicial
            plano_ativo["unidade"] = unidade_inicial
            aulas = gerenciador_dados.carregar_csv(caminho_inicial)
    else:
        # Fallback para caminho clássico único se não houver pastas estruturadas
        caminho_fallback = Path(config.CSV_PATH)
        if caminho_fallback.exists():
            plano_ativo["caminho_csv"] = caminho_fallback
            aulas = gerenciador_dados.carregar_csv(caminho_fallback)
        else:
            raise RuntimeError(
                f"Nenhuma estrutura de cursos encontrada em '{config.DADOS_DIR}' "
                f"nem arquivo CSV em '{config.CSV_PATH}'."
            )

    print(f"[INFO] Iniciando com {len(aulas)} aulas carregadas.")
    if curso_inicial:
        print(f"[INFO] Curso: {curso_inicial} | Unidade: {unidade_inicial}")

    root = tk.Tk()

    if config.GUI_SEMPRE_NO_TOPO:
        root.attributes("-topmost", True)

    painel = PainelPlanos(
        root=root,
        aulas=aulas,
        on_inserir=executar_insercao,
        estrutura_dados=estrutura,
        curso_inicial=curso_inicial,
        unidade_inicial=unidade_inicial,
        on_trocar_plano=trocar_plano,
    )

    root.lift()
    root.after(
        100,
        lambda: root.attributes("-topmost", config.GUI_SEMPRE_NO_TOPO)
    )

    root.mainloop()


if __name__ == "__main__":
    main()
