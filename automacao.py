import time

import pyautogui
import pyperclip

import config

pyautogui.FAILSAFE = True
pyautogui.PAUSE = config.PAUSE


def escrever(texto):
    """Insere texto via clipboard para preservar acentos e caracteres especiais."""
    pyperclip.copy(str(texto or ""))
    pyautogui.hotkey("ctrl", "v")


def clicar(posicao):
    pyautogui.click(posicao[0], posicao[1])


def preencher_campo(nome, valor):
    """Clica no campo configurado e substitui seu conteúdo."""
    if config.IGNORAR_CAMPOS_VAZIOS and not str(valor or "").strip():
        return

    clicar(config.CAMPOS[nome])
    pyautogui.hotkey("ctrl", "a")
    escrever(valor)
    time.sleep(config.DELAY_CAMPO)


def preencher_aula(aula, log=None):
    """
    Preenche a aula atualmente aberta no Portal.

    IMPORTANTE:
    O usuário deve clicar manualmente em Editar antes de executar esta ação.
    """
    def registrar(msg):
        print(msg)
        if log:
            log(msg)

    registrar("Aguardando o modal de edição...")
    time.sleep(config.DELAY_MODAL)

    preencher_campo(
        "titulo",
        aula.get(config.MAPEAMENTO_CSV["titulo"], "")
    )
    registrar("Título preenchido.")

    preencher_campo(
        "conteudo",
        aula.get(config.MAPEAMENTO_CSV["conteudo"], "")
    )
    registrar("Conteúdo preenchido.")

    # Campo/controle previsto.
    if "previsto" in config.CAMPOS:
        clicar(config.CAMPOS["previsto"])
        time.sleep(config.DELAY_CAMPO)

    # Scroll do modal para revelar os campos inferiores.
    if "scroll_start" in config.CAMPOS and "scroll_end" in config.CAMPOS:
        pyautogui.moveTo(*config.CAMPOS["scroll_start"])
        pyautogui.dragTo(
            *config.CAMPOS["scroll_end"],
            duration=0.4,
            button="left"
        )
        time.sleep(config.DELAY_CAMPO)

    preencher_campo(
        "metodologia",
        aula.get(config.MAPEAMENTO_CSV["metodologia"], "")
    )
    registrar("Lição de casa preenchida.")

    preencher_campo(
        "recursos",
        aula.get(config.MAPEAMENTO_CSV["recursos"], "")
    )
    registrar("Observação preenchida.")

    if not config.MODO_TESTE:
        clicar(config.CAMPOS["salvar"])
        registrar("Plano salvo automaticamente.")
        time.sleep(config.DELAY_SALVAR)
    else:
        registrar("Modo teste: não foi realizado o salvamento.")
