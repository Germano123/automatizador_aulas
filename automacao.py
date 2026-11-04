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


def clicar(posicao, descricao="", log=None):
    registrar(
        f"    → Clique: {descricao or posicao} em {posicao}",
        log,
    )
    pyautogui.click(posicao[0], posicao[1])
    time.sleep(config.DELAY_CAMPO)


def colar_texto(texto, descricao="", log=None):
    """
    Cola o texto usando o clipboard do sistema.
    Isso preserva acentos e caracteres especiais do CSV.
    """
    texto = str(texto or "")

    registrar(
        f"    → Inserindo {descricao or 'texto'} ({len(texto)} caracteres)",
        log,
    )

    # Coloca o conteúdo no clipboard ANTES de enviar Ctrl+V.
    pyperclip.copy(texto)
    time.sleep(0.15)

    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.15)

    pyautogui.hotkey("ctrl", "v")
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
    """
    Preenche a aula atualmente aberta no Portal.

    O usuário deve:
      1. localizar a aula;
      2. clicar manualmente em Editar;
      3. esperar o modal abrir;
      4. clicar em INSERIR ESTA AULA na GUI.

    O programa NÃO procura o botão Editar.
    """
    registrar("=== INÍCIO DA INSERÇÃO ===", log)

    # Mostra no terminal exatamente o que veio do CSV.
    registrar(
        f"  tipo de aula: {aula.get(config.MAPEAMENTO_CSV['titulo'], '')}",
        log,
    )
    registrar(
        f"  conteúdo previsto: {aula.get(config.MAPEAMENTO_CSV['conteudo'], '')[:120]}",
        log,
    )
    registrar(
        f"  lição de casa: {aula.get(config.MAPEAMENTO_CSV['metodologia'], '')[:120]}",
        log,
    )
    registrar(
        f"  observação: {aula.get(config.MAPEAMENTO_CSV['recursos'], '')[:120]}",
        log,
    )

    registrar(
        f"  Aguardando {config.DELAY_MODAL:.1f}s para o modal estar pronto...",
        log,
    )
    time.sleep(config.DELAY_MODAL)

    # 1. TÍTULO
    preencher_campo(
        "titulo",
        aula.get(config.MAPEAMENTO_CSV["titulo"], ""),
        log,
    )

    # 2. CONTEÚDO
    preencher_campo(
        "conteudo",
        aula.get(config.MAPEAMENTO_CSV["conteudo"], ""),
        log,
    )

    # 3. CONTROLE "PREVISTO", se configurado.
    if "previsto" in config.CAMPOS:
        clicar(config.CAMPOS["previsto"], "previsto", log)

    # 4. SCROLL
    if "scroll_start" in config.CAMPOS and "scroll_end" in config.CAMPOS:
        arrastar_scroll(log)

    # 5. CAMPOS INFERIORES
    preencher_campo(
        "metodologia",
        aula.get(config.MAPEAMENTO_CSV["metodologia"], ""),
        log,
    )

    preencher_campo(
        "recursos",
        aula.get(config.MAPEAMENTO_CSV["recursos"], ""),
        log,
    )

    if not config.MODO_TESTE:
        clicar(config.CAMPOS["salvar"], "SALVAR", log)
        registrar("✓ Plano salvo automaticamente.", log)
        time.sleep(config.DELAY_SALVAR)
    else:
        registrar("✓ MODO TESTE: não foi realizado o salvamento.", log)

    registrar("=== FIM DA INSERÇÃO ===", log)
