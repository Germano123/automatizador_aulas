import csv
import threading
from pathlib import Path
import tkinter as tk

import config
from automacao import preencher_aula
from gui import PainelPlanos


def carregar_csv():
    caminho = Path(config.CSV_PATH)
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho.resolve()}")

    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def atualizar_status(indice, status, erro=""):
    """Persiste o resultado da operação no próprio CSV."""
    caminho = Path(config.CSV_PATH)

    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        registros = list(csv.DictReader(arquivo))

    if not registros:
        return

    fieldnames = list(registros[0].keys())
    if "status" not in fieldnames:
        fieldnames.append("status")
    if "erro" not in fieldnames:
        fieldnames.append("erro")

    registros[indice]["status"] = status
    registros[indice]["erro"] = erro

    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(registros)


def executar_insercao(indice, aula, callback):
    """Executa PyAutoGUI em thread para não congelar a GUI."""

    def trabalho():
        try:
            preencher_aula(aula)
            atualizar_status(indice, "preenchida", "")
            # Tkinter deve ser atualizado na thread principal.
            callback(True, "")
        except Exception as erro:
            try:
                atualizar_status(indice, "erro", str(erro))
            except Exception:
                pass
            callback(False, str(erro))

    threading.Thread(target=trabalho, daemon=True).start()


def main():
    aulas = carregar_csv()

    if not aulas:
        raise RuntimeError("O arquivo CSV não possui aulas.")

    root = tk.Tk()

    if config.GUI_SEMPRE_NO_TOPO:
        root.attributes("-topmost", True)

    painel = PainelPlanos(root, aulas, executar_insercao)

    root.lift()
    root.after(
        100,
        lambda: root.attributes("-topmost", config.GUI_SEMPRE_NO_TOPO)
    )

    root.mainloop()


if __name__ == "__main__":
    main()
