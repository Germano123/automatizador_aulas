import csv
import time
from pathlib import Path

import pyautogui
import pyperclip
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

import config


# ============================================================
# CONFIGURAÇÃO DO PYAUTOGUI
# ============================================================

pyautogui.FAILSAFE = True
pyautogui.PAUSE = config.PAUSE


# ============================================================
# ESTADO DO NAVEGADOR
# ============================================================

PLAYWRIGHT = None
BROWSER = None
PAGE = None


# ============================================================
# FUNÇÕES BÁSICAS
# ============================================================

def escrever(texto):
    """Escreve texto usando clipboard + Ctrl+V."""
    pyperclip.copy(str(texto or ""))
    pyautogui.hotkey("ctrl", "v")


def clicar(posicao):
    """Clica em uma coordenada definida no config.py."""
    pyautogui.click(posicao[0], posicao[1])


def preencher_campo(nome, valor):
    """Preenche um campo usando as coordenadas do config.py."""
    print(f"    Preenchendo: {nome}")

    clicar(config.CAMPOS[nome])
    pyautogui.hotkey("ctrl", "a")
    escrever(valor)

    time.sleep(config.DELAY_CAMPO)


# ============================================================
# CSV
# ============================================================

def carregar_csv():
    """Carrega todas as aulas do arquivo configurado."""
    caminho = Path(config.CSV_PATH)

    if not caminho.exists():
        raise FileNotFoundError(
            f"CSV não encontrado: {caminho.resolve()}"
        )

    with caminho.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        return list(csv.DictReader(arquivo))


# ============================================================
# STATUS
# ============================================================

def atualizar_status(indice, status, erro=""):
    """Atualiza status e erro no CSV."""
    caminho = Path(config.CSV_PATH)

    with caminho.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
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

    with caminho.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        writer = csv.DictWriter(
            arquivo,
            fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(registros)


# ============================================================
# PLAYWRIGHT — CONEXÃO COM O CHROME
# ============================================================

def conectar_navegador():
    """
    Conecta ao Chrome já aberto através do protocolo CDP.

    Isso não é crawler: o Playwright apenas controla o DOM
    da página que já está aberta no navegador.
    """
    global PLAYWRIGHT, BROWSER, PAGE

    print("  Conectando ao navegador via Playwright/CDP...")

    PLAYWRIGHT = sync_playwright().start()

    try:
        BROWSER = PLAYWRIGHT.chromium.connect_over_cdp(
            config.PLAYWRIGHT_CDP_URL
        )
    except Exception as erro:
        PLAYWRIGHT.stop()
        PLAYWRIGHT = None

        raise RuntimeError(
            "Não foi possível conectar ao Chrome via CDP.\n"
            f"Endereço configurado: {config.PLAYWRIGHT_CDP_URL}\n\n"
            "Inicie o Chrome com depuração remota, por exemplo:\n"
            'chrome.exe --remote-debugging-port=9222 '
            '--user-data-dir="%TEMP%\\PortalProfessorAutomation"\n\n'
            f"Erro original: {erro}"
        )

    paginas = []

    for contexto in BROWSER.contexts:
        paginas.extend(contexto.pages)

    # Primeiro procura especificamente uma página do Portal.
    portal_pages = [
        pagina
        for pagina in paginas
        if config.PORTAL_DOMINIO.lower()
        in pagina.url.lower()
    ]

    if portal_pages:
        PAGE = portal_pages[0]
    elif paginas:
        PAGE = paginas[0]
        print(
            "  Aviso: nenhuma aba do Portal foi identificada ainda."
        )
    else:
        raise RuntimeError(
            "O navegador está conectado, mas nenhuma página foi encontrada."
        )

    print(f"  Página conectada: {PAGE.url}")

    return PAGE


def fechar_navegador():
    """
    Desconecta o Playwright sem fechar o Chrome do usuário.
    """
    global PLAYWRIGHT, BROWSER, PAGE

    try:
        if BROWSER:
            BROWSER.close()
    except Exception:
        pass

    try:
        if PLAYWRIGHT:
            PLAYWRIGHT.stop()
    except Exception:
        pass

    PLAYWRIGHT = None
    BROWSER = None
    PAGE = None


def selecionar_pagina_portal():
    """
    Procura novamente uma aba do Portal entre as páginas abertas.
    """
    global PAGE

    paginas = []

    for contexto in BROWSER.contexts:
        paginas.extend(contexto.pages)

    portal_pages = [
        pagina
        for pagina in paginas
        if config.PORTAL_DOMINIO.lower()
        in pagina.url.lower()
    ]

    if portal_pages:
        PAGE = portal_pages[0]

    return PAGE


# ============================================================
# PLAYWRIGHT — LOCALIZAR EDITAR
# ============================================================

def obter_botoes_editar():
    """
    Retorna os elementos Editar do DOM.

    A estrutura observada no HTML do Portal é:

        td.po-table-column-single-action
          div.po-table-single-action
            span
              Editar

    Portanto não usamos reconhecimento de imagem.
    """
    selecionar_pagina_portal()

    if PAGE is None:
        raise RuntimeError("Nenhuma página do Portal disponível.")

    seletor = (
        "td.po-table-column-single-action "
        "div.po-table-single-action "
        "span"
    )

    try:
        PAGE.wait_for_selector(
            seletor,
            state="visible",
            timeout=config.TIMEOUT_DOM * 1000
        )
    except PlaywrightTimeoutError:
        return []

    elementos = PAGE.locator(seletor)

    resultado = []

    for i in range(elementos.count()):
        elemento = elementos.nth(i)

        try:
            texto = elemento.inner_text().strip()

            if texto == "Editar":
                resultado.append(elemento)

        except Exception:
            continue

    return resultado


def linha_corresponde_a_aula(linha, aula):
    """
    Tenta identificar uma linha do Portal através de
    data/turma/aula quando essas colunas existirem no CSV.

    O CSV atual do projeto não possui essas colunas.
    Nesse caso retorna False e o sistema utiliza o fallback
    por posição.
    """
    colunas = config.COLUNAS_IDENTIFICACAO

    valores = []

    for chave, coluna_csv in colunas.items():
        valor = str(aula.get(coluna_csv, "")).strip()

        if not valor:
            return False

        valores.append(valor.lower())

    try:
        texto_linha = linha.inner_text().strip().lower()
    except Exception:
        return False

    return all(valor in texto_linha for valor in valores)


def localizar_editar(indice_registro, aula):
    """
    Localiza o botão Editar no DOM.

    Estratégia 1:
        se o CSV possuir data/turma/aula, tenta localizar
        a linha correspondente.

    Estratégia 2:
        caso o CSV não tenha identificadores, usa o índice
        do registro como fallback.

    Para o CSV atual, o primeiro registro usa o primeiro
    botão Editar encontrado no DOM.
    """
    print("  Procurando botão Editar no DOM...")

    selecionar_pagina_portal()

    if PAGE is None:
        print("  ERRO: página do Portal não disponível.")
        return None

    # --------------------------------------------------------
    # Estratégia 1 — identificação por linha
    # --------------------------------------------------------

    possui_identificadores = all(
        str(aula.get(coluna, "")).strip()
        for coluna in config.COLUNAS_IDENTIFICACAO.values()
    )

    if possui_identificadores:

        print(
            "  Tentando localizar a linha por data/turma/aula..."
        )

        linhas = PAGE.locator("tr")

        for i in range(linhas.count()):

            linha = linhas.nth(i)

            try:
                if not linha.is_visible():
                    continue

                if linha_corresponde_a_aula(
                    linha,
                    aula
                ):
                    editar = linha.locator(
                        "td.po-table-column-single-action "
                        "div.po-table-single-action "
                        "span",
                    ).filter(
                        has_text="Editar"
                    )

                    if editar.count() > 0:
                        print(
                            f"  Linha correspondente encontrada: {i}"
                        )
                        return editar.first

            except Exception:
                continue

    # --------------------------------------------------------
    # Estratégia 2 — fallback por posição
    # --------------------------------------------------------

    print(
        "  Identificadores de linha não disponíveis."
    )

    botoes = obter_botoes_editar()

    if not botoes:
        print(
            "  Nenhum botão Editar encontrado no DOM."
        )
        return None

    posicao = (
        config.EDITAR_INDICE_FALLBACK
        if len(botoes) > config.EDITAR_INDICE_FALLBACK
        else 0
    )

    print(
        f"  Usando Editar de índice {posicao}."
    )

    return botoes[posicao]


def abrir_edicao(indice_registro, aula):
    """
    Localiza o Editar no DOM e dispara o clique.
    """
    elemento = localizar_editar(
        indice_registro,
        aula
    )

    if elemento is None:
        return False

    print("  Clicando em Editar pelo DOM...")

    try:
        elemento.click()
    except Exception as erro:
        print(
            f"  Erro no clique DOM: {erro}"
        )
        return False

    time.sleep(config.DELAY_MODAL)

    return True


# ============================================================
# PREENCHIMENTO — PARTE SUPERIOR
# ============================================================

def preencher_titulo(aula):
    """Preenche o campo Título."""
    coluna = config.MAPEAMENTO_CSV["titulo"]
    valor = aula.get(coluna, "")

    if config.IGNORAR_CAMPOS_VAZIOS and not valor:
        return

    print(f"    título: {valor[:60]}")

    preencher_campo(
        "titulo",
        valor
    )


def preencher_conteudo(aula):
    """Preenche o campo Conteúdo."""
    coluna = config.MAPEAMENTO_CSV["conteudo"]
    valor = aula.get(coluna, "")

    if config.IGNORAR_CAMPOS_VAZIOS and not valor:
        return

    print(f"    conteúdo: {valor[:60]}")

    preencher_campo(
        "conteudo",
        valor
    )


# ============================================================
# PREVISTO
# ============================================================

def clicar_previsto():
    """
    Depois de preencher Conteúdo, clica em Previsto.
    """
    print("  Clicando em 'Previsto'...")

    clicar(
        config.CAMPOS["previsto"]
    )

    time.sleep(config.DELAY_CAMPO)


# ============================================================
# ROLAGEM
# ============================================================

def rolar_modal():
    """
    Arrasta a barra de rolagem do modal de scroll_start
    até scroll_end.
    """
    print("  Rolando o modal...")

    inicio = config.CAMPOS["scroll_start"]
    fim = config.CAMPOS["scroll_end"]

    pyautogui.moveTo(
        inicio[0],
        inicio[1]
    )

    pyautogui.dragTo(
        fim[0],
        fim[1],
        duration=config.SCROLL_DURACAO,
        button="left"
    )

    time.sleep(config.DELAY_SCROLL)


# ============================================================
# PREENCHIMENTO — PARTE INFERIOR
# ============================================================

def preencher_metodologia(aula):
    """Preenche o campo Metodologia após a rolagem."""
    coluna = config.MAPEAMENTO_CSV["metodologia"]
    valor = aula.get(coluna, "")

    if config.IGNORAR_CAMPOS_VAZIOS and not valor:
        return

    print(f"    metodologia: {valor[:60]}")

    preencher_campo(
        "metodologia",
        valor
    )


def preencher_recursos(aula):
    """Preenche o campo Recursos após a rolagem."""
    coluna = config.MAPEAMENTO_CSV["recursos"]
    valor = aula.get(coluna, "")

    if config.IGNORAR_CAMPOS_VAZIOS and not valor:
        return

    print(f"    recursos: {valor[:60]}")

    preencher_campo(
        "recursos",
        valor
    )


# ============================================================
# PREENCHIMENTO COMPLETO
# ============================================================

def preencher_modal(aula):
    """
    Sequência definida para o Portal:

    1. Título
    2. Conteúdo
    3. Previsto
    4. Arrastar scroll
    5. Metodologia
    6. Recursos
    """
    print()
    print("  Preenchendo modal...")
    print()

    preencher_titulo(aula)
    preencher_conteudo(aula)
    clicar_previsto()
    rolar_modal()
    preencher_metodologia(aula)
    preencher_recursos(aula)

    print()
    print("  ✓ Campos preenchidos.")


# ============================================================
# SALVAR
# ============================================================

def salvar():
    """
    Salva somente quando MODO_TESTE=False.
    """
    if config.MODO_TESTE:
        print()
        print(
            "  [MODO TESTE] SALVAR NÃO SERÁ CLICADO."
        )
        return True

    print()
    print("  Clicando em SALVAR...")

    clicar(
        config.CAMPOS["salvar"]
    )

    time.sleep(
        config.DELAY_SALVAR
    )

    return True


# ============================================================
# PROCESSAR UMA AULA
# ============================================================

def processar_aula(indice, aula):
    """Processa uma única aula."""

    print()
    print("=" * 60)
    print(f"AULA / REGISTRO {indice + 1}")
    print("=" * 60)

    print(
        f"Tipo de aula: {aula.get('tipo de aula', '')}"
    )

    print(
        f"Conteúdo: {aula.get('conteúdo previsto', '')[:80]}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # ABRIR EDIÇÃO
    # --------------------------------------------------------

    if not abrir_edicao(indice, aula):

        print(
            "  ERRO: botão Editar não encontrado."
        )

        if not config.MODO_TESTE:
            atualizar_status(
                indice,
                "ERRO",
                "Editar não encontrado"
            )

        return False

    # --------------------------------------------------------
    # PREENCHER MODAL
    # --------------------------------------------------------

    preencher_modal(aula)

    # --------------------------------------------------------
    # SALVAR
    # --------------------------------------------------------

    salvar()

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if config.MODO_TESTE:

        print()
        print(
            "  [MODO TESTE] Registro não será marcado como OK."
        )

    else:

        atualizar_status(
            indice,
            "OK",
            ""
        )

        print(
            "  ✓ Aula processada e salva."
        )

    return True


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print(" AUTOMATIZADOR DE PLANOS DE AULA - v0.2")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. CARREGAR CSV
    # --------------------------------------------------------

    print()
    print("Carregando dados de aulas.csv...")

    aulas = carregar_csv()

    pendentes = [
        (indice, aula)
        for indice, aula in enumerate(aulas)
        if aula.get(
            "status",
            ""
        ).strip().upper() != "OK"
    ]

    print()
    print(
        f"Total de registros: {len(aulas)}"
    )

    print(
        f"Registros pendentes: {len(pendentes)}"
    )

    if not pendentes:
        print()
        print(
            "Nenhuma aula pendente para processamento."
        )
        return

    # --------------------------------------------------------
    # PRIMEIRO REGISTRO — TESTE
    # --------------------------------------------------------

    indice, aula = pendentes[0]

    print()
    print("=" * 60)
    print(" PRÓXIMO REGISTRO")
    print("=" * 60)

    print(
        f"Índice:          {indice}"
    )

    print(
        f"Tipo de aula:    {aula.get('tipo de aula', '')}"
    )

    print(
        f"Conteúdo:        {aula.get('conteúdo previsto', '')[:100]}"
    )

    print(
        f"Lição de casa:   {aula.get('lição de casa', '')[:100]}"
    )

    print(
        f"Observação:      {aula.get('observação', '')[:100]}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # 2. CONECTAR AO NAVEGADOR
    # --------------------------------------------------------

    try:
        conectar_navegador()
    except Exception as erro:
        print()
        print("ERRO AO CONECTAR AO NAVEGADOR:")
        print(erro)
        return

    # --------------------------------------------------------
    # 3. DAR TEMPO PARA TROCAR PARA O PORTAL
    # --------------------------------------------------------

    print()
    print(
        "Troque agora para a página do Portal do Professor."
    )

    print(
        "A automação começará em 1,5 segundo."
    )

    print()
    print(
        "IMPORTANTE: não mova o mouse durante esse intervalo."
    )

    print()

    time.sleep(1.5)

    # --------------------------------------------------------
    # 4. INICIAR AUTOMAÇÃO
    # --------------------------------------------------------

    try:

        processar_aula(
            indice,
            aula
        )

    except KeyboardInterrupt:

        print()
        print(
            "Execução interrompida pelo usuário."
        )

    except Exception as erro:

        print()
        print(
            f"ERRO inesperado: {erro}"
        )

        if not config.MODO_TESTE:
            atualizar_status(
                indice,
                "ERRO",
                str(erro)
            )

    finally:
        fechar_navegador()

    print()
    print("=" * 60)
    print(" EXECUÇÃO FINALIZADA")
    print("=" * 60)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()
