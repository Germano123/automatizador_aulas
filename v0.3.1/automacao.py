import time

import pyautogui
import pyperclip

import config

pyautogui.FAILSAFE = True
pyautogui.PAUSE = config.PAUSE


def registrar(msg, log=None):
    print(msg, flush=True)
    if log:
        log(msg)

def digitar_texto(texto, descricao="", log=None):
    texto = str(texto or "")

    registrar(
        f"    → Digitando {descricao or 'texto'}: {texto[:60]}",
        log
    )

    pyautogui.write(texto, interval=0.05)
    time.sleep(config.DELAY_CAMPO)


def colar_texto(texto, descricao="", log=None):
    texto = str(texto or "")

    registrar(
        f"    → Colando {descricao or 'texto'} ({len(texto)} caracteres)",
        log
    )

    pyperclip.copy(texto)
    time.sleep(0.15)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(config.DELAY_CAMPO)


def clicar(posicao, descricao="", log=None):
    registrar(
        f"    → Movendo para {descricao or posicao}: {posicao}",
        log
    )

    pyautogui.moveTo(
        posicao[0],
        posicao[1],
        duration=0.25
    )

    time.sleep(0.2)

    registrar(
        f"    → Clique em {descricao or posicao}",
        log
    )

    pyautogui.click()
    time.sleep(config.DELAY_CAMPO)


def preencher_campo(nome, valor, log=None):
    """Clica no campo e insere o valor correspondente ao CSV."""
    valor = str(valor or "")

    if config.IGNORAR_CAMPOS_VAZIOS and not valor.strip():
        registrar(f"    → {nome}: vazio — ignorado", log)
        return

    if nome not in config.CAMPOS:
        raise KeyError(f"Campo não configurado: {nome}")

    clicar(config.CAMPOS[nome], nome, log)
    colar_texto(valor, nome, log)

    registrar(f"    ✓ {nome} preenchido.", log)


def arrastar_scroll(log=None):
    """
    Faz o arraste da barra de rolagem de forma explícita:
    move → mouseDown → arrasta → mouseUp.
    """
    inicio = config.CAMPOS["scroll_start"]
    fim = config.CAMPOS["scroll_end"]

    registrar(f"    → Posicionando no scroll: {inicio}", log)
    pyautogui.moveTo(inicio[0], inicio[1], duration=0.25)
    time.sleep(0.3)

    registrar(f"    → mouseDown no scroll", log)
    pyautogui.mouseDown(button="left")
    time.sleep(0.25)

    registrar(f"    → Arrastando scroll até: {fim}", log)
    pyautogui.moveTo(fim[0], fim[1], duration=0.9)

    time.sleep(0.25)
    pyautogui.mouseUp(button="left")
    registrar("    ✓ Scroll arrastado.", log)

    time.sleep(config.DELAY_SCROLL)



def preencher_aula(aula, log=None):
    registrar("=== INÍCIO DA INSERÇÃO ===", log)

    titulo = aula.get(
        config.MAPEAMENTO_CSV["titulo"],
        ""
    )

    conteudo = aula.get(
        config.MAPEAMENTO_CSV["conteudo"],
        ""
    )

    metodologia = aula.get(
        config.MAPEAMENTO_CSV["metodologia"],
        ""
    )

    recursos = aula.get(
        config.MAPEAMENTO_CSV["recursos"],
        ""
    )

    registrar(f"  tipo de aula: {titulo}", log)
    registrar(
        f"  conteúdo previsto: {conteudo[:120]}",
        log
    )
    registrar(
        f"  lição de casa: {metodologia[:120]}",
        log
    )
    registrar(
        f"  observação: {recursos[:120]}",
        log
    )

    registrar(
        f"  Aguardando {config.DELAY_MODAL:.1f}s para o modal estar pronto...",
        log
    )

    time.sleep(config.DELAY_MODAL)

    # =========================================================
    # 1. TÍTULO
    # =========================================================

    registrar("  [1/7] Preenchendo TÍTULO...", log)

    clicar(
        config.CAMPOS["titulo"],
        "titulo",
        log
    )

    primeiras_letras = titulo.strip()[:3]

    registrar(
        f"    → Digitando as 3 primeiras letras: '{primeiras_letras}'",
        log
    )

    pyautogui.write(
        primeiras_letras,
        interval=0.1
    )

    time.sleep(config.DELAY_CAMPO)

    registrar(
        "    → Pressionando ENTER para confirmar opção.",
        log
    )

    pyautogui.press("enter")

    time.sleep(config.DELAY_CAMPO)

    # =========================================================
    # 2. CONTEÚDO
    # =========================================================

    registrar("  [2/7] Preenchendo CONTEÚDO...", log)

    clicar(
        config.CAMPOS["conteudo"],
        "conteudo",
        log
    )

    colar_texto(
        conteudo,
        "conteúdo previsto",
        log
    )

    # =========================================================
    # 3. PREVISTO
    # =========================================================

    registrar("  [3/7] Clicando em PREVISTO...", log)

    clicar(
        config.CAMPOS["previsto"],
        "previsto",
        log
    )

    # =========================================================
    # 4. SCROLL
    # =========================================================

    registrar("  [4/7] Executando SCROLL...", log)

    arrastar_scroll(log)

    # =========================================================
    # 5. METODOLOGIA
    # =========================================================

    registrar("  [5/7] Preenchendo METODOLOGIA...", log)

    clicar(
        config.CAMPOS["metodologia"],
        "metodologia",
        log
    )

    colar_texto(
        metodologia,
        "metodologia",
        log
    )

    # =========================================================
    # 6. RECURSOS
    # =========================================================

    registrar("  [6/7] Preenchendo RECURSOS...", log)

    clicar(
        config.CAMPOS["recursos"],
        "recursos",
        log
    )

    colar_texto(
        recursos,
        "recursos",
        log
    )

    # =========================================================
    # 7. SALVAR
    # =========================================================

    registrar("  [7/7] Clicando em SALVAR...", log)

    clicar(
        config.CAMPOS["salvar"],
        "salvar",
        log
    )

    time.sleep(config.DELAY_SALVAR)

    registrar("  ✓ Plano salvo.", log)
    registrar("=== FIM DA INSERÇÃO ===", log)

