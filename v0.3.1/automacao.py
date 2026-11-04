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

    pyautogui.write(texto, interval=config.INTERVALO_TEXTO_RAPIDO)
    time.sleep(config.DELAY_CAMPO)


def colar_texto(texto, descricao="", log=None):
    texto = str(texto or "")

    registrar(
        f"    → Colando {descricao or 'texto'} ({len(texto)} caracteres)",
        log
    )

    pyperclip.copy(texto)
    time.sleep(config.DELAY_CLIPBOARD)
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
        duration=config.DURACAO_MOVIMENTO
    )

    time.sleep(config.DELAY_POS_MOVIMENTO)

    registrar(
        f"    → Clique em {descricao or posicao}",
        log
    )

    pyautogui.click()
    time.sleep(config.DELAY_CAMPO)


def executar_acao_ponto(chave, log=None):
    """
    Executa a ação configurada para o ponto (clique, duplo clique, clique direito ou arraste)
    respeitando as coordenadas e o delay configurados dinamicamente no JSON.
    """
    pontos = config.obter_config_pontos()
    ponto = pontos.get(chave)

    if not ponto:
        # Fallback para config.CAMPOS se a chave não estiver nos pontos
        if chave in config.CAMPOS:
            clicar(config.CAMPOS[chave], chave, log)
        return

    tipo = ponto.get("tipo", "clique")
    x = int(ponto.get("x", 0))
    y = int(ponto.get("y", 0))
    delay = float(ponto.get("delay", config.DELAY_CAMPO))
    label = ponto.get("label", chave)

    if tipo == "clique e arraste":
        x2 = int(ponto.get("x2", x))
        y2 = int(ponto.get("y2", y))
        arrastar_scroll_custom(x, y, x2, y2, delay, log)
        return

    registrar(f"    → Movendo para {label}: ({x}, {y})", log)
    pyautogui.moveTo(x, y, duration=config.DURACAO_MOVIMENTO)
    time.sleep(config.DELAY_POS_MOVIMENTO)

    if tipo == "duplo clique":
        registrar(f"    → Duplo clique em {label}", log)
        pyautogui.doubleClick()
    elif tipo == "clique direito":
        registrar(f"    → Clique direito em {label}", log)
        pyautogui.rightClick()
    else:
        registrar(f"    → Clique em {label}", log)
        pyautogui.click()

    time.sleep(delay)


def arrastar_scroll_custom(x1, y1, x2, y2, delay, log=None):
    registrar(f"    → Posicionando no scroll: ({x1}, {y1})", log)
    pyautogui.moveTo(x1, y1, duration=config.DURACAO_MOVIMENTO)
    time.sleep(config.DELAY_SCROLL_POSICIONAR)

    registrar("    → mouseDown no scroll", log)
    pyautogui.mouseDown(button="left")
    time.sleep(config.DELAY_SCROLL_ETAPA)

    registrar(f"    → Arrastando scroll até: ({x2}, {y2})", log)
    pyautogui.moveTo(x2, y2, duration=config.DURACAO_SCROLL)

    time.sleep(config.DELAY_SCROLL_ETAPA)
    pyautogui.mouseUp(button="left")
    registrar("    ✓ Scroll arrastado.", log)

    time.sleep(delay)


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
    inicio = config.CAMPOS.get("scroll_start", (1625, 295))
    fim = config.CAMPOS.get("scroll_end", (1625, 535))
    arrastar_scroll_custom(inicio[0], inicio[1], fim[0], fim[1], config.DELAY_SCROLL, log)



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
    executar_acao_ponto("titulo", log)

    primeiras_letras = titulo.strip()[:3]

    registrar(
        f"    → Digitando as 3 primeiras letras: '{primeiras_letras}'",
        log
    )

    pyautogui.write(
        primeiras_letras,
        interval=config.INTERVALO_DIGITACAO
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
    executar_acao_ponto("conteudo", log)

    colar_texto(
        conteudo,
        "conteúdo previsto",
        log
    )

    # =========================================================
    # 3. PREVISTO
    # =========================================================

    registrar("  [3/7] Clicando em PREVISTO...", log)
    executar_acao_ponto("previsto", log)

    # =========================================================
    # 4. SCROLL
    # =========================================================

    registrar("  [4/7] Executando SCROLL...", log)
    executar_acao_ponto("scroll", log)

    # =========================================================
    # 5. METODOLOGIA
    # =========================================================

    registrar("  [5/7] Preenchendo METODOLOGIA...", log)
    executar_acao_ponto("metodologia", log)

    colar_texto(
        metodologia,
        "metodologia",
        log
    )

    # =========================================================
    # 6. RECURSOS
    # =========================================================

    registrar("  [6/7] Preenchendo RECURSOS...", log)
    executar_acao_ponto("recursos", log)

    colar_texto(
        recursos,
        "recursos",
        log
    )

    # =========================================================
    # 7. SALVAR
    # =========================================================

    registrar("  [7/7] Clicando em SALVAR...", log)
    executar_acao_ponto("salvar", log)

    time.sleep(config.DELAY_SALVAR)

    registrar("  ✓ Plano salvo.", log)
    registrar("=== FIM DA INSERÇÃO ===", log)

