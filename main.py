import csv
import time
from pathlib import Path

import pyautogui
import pyperclip

import config


# ============================================================
# CONFIGURAÇÃO DO PYAutoGUI
# ============================================================

pyautogui.FAILSAFE = True
pyautogui.PAUSE = config.PAUSE


# ============================================================
# FUNÇÕES BÁSICAS
# ============================================================

def escrever(texto):
    """
    Escreve texto utilizando clipboard + Ctrl+V.
    Isso evita problemas com acentos e caracteres especiais.
    """
    pyperclip.copy(str(texto or ""))
    pyautogui.hotkey("ctrl", "v")


def clicar(posicao):
    """
    Clica em uma coordenada definida no config.py.
    """
    pyautogui.click(posicao[0], posicao[1])


def preencher_campo(nome, valor):
    """
    Clica no campo, seleciona o conteúdo existente
    e insere o novo valor.
    """
    print(f"    Preenchendo: {nome}")

    clicar(config.CAMPOS[nome])

    pyautogui.hotkey("ctrl", "a")

    escrever(valor)

    time.sleep(config.DELAY_CAMPO)


# ============================================================
# CSV
# ============================================================

def carregar_csv():
    """
    Carrega todas as aulas do arquivo aulas.csv.
    """
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
# STATUS DO CSV
# ============================================================

def atualizar_status(indice, status, erro=""):
    """
    Atualiza o status de uma aula no CSV.

    IMPORTANTE:
    Em MODO_TESTE esta função não será chamada para marcar
    o registro como OK.
    """

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
# LOCALIZAR BOTÃO EDITAR
# ============================================================

def localizar_editar():
    """
    Procura visualmente o botão Editar utilizando
    a imagem definida em config.IMAGEM_EDITAR.
    """

    print("  Procurando botão Editar...")

    inicio = time.time()

    while time.time() - inicio < config.TIMEOUT_EDITAR:

        try:
            box = pyautogui.locateOnScreen(
                config.IMAGEM_EDITAR,
                confidence=config.CONFIANCA_IMAGEM
            )

        except Exception as erro:

            print(
                f"  Erro ao procurar imagem: {erro}"
            )

            return None

        if box:

            centro = pyautogui.center(box)

            print(
                f"  Editar encontrado em: {centro}"
            )

            return centro

        time.sleep(0.5)

    print("  Editar não encontrado.")

    return None


# ============================================================
# ABRIR EDIÇÃO
# ============================================================

def abrir_edicao():
    """
    Localiza e clica no botão Editar.
    """

    posicao = localizar_editar()

    if not posicao:
        return False

    print("  Clicando em Editar...")

    clicar(posicao)

    time.sleep(config.DELAY_MODAL)

    return True


# ============================================================
# PREENCHIMENTO — PARTE SUPERIOR
# ============================================================

def preencher_titulo(aula):
    """
    Preenche o campo Título.
    """

    valor = aula.get(
        config.MAPEAMENTO_CSV["titulo"],
        ""
    )

    if (
        config.IGNORAR_CAMPOS_VAZIOS
        and not valor
    ):
        return

    print(
        f"    título: {valor[:60]}"
    )

    preencher_campo(
        "titulo",
        valor
    )


def preencher_conteudo(aula):
    """
    Preenche o campo Conteúdo.
    """

    valor = aula.get(
        config.MAPEAMENTO_CSV["conteudo"],
        ""
    )

    if (
        config.IGNORAR_CAMPOS_VAZIOS
        and not valor
    ):
        return

    print(
        f"    conteúdo: {valor[:60]}"
    )

    preencher_campo(
        "conteudo",
        valor
    )


# ============================================================
# BOTÃO PREVISTO
# ============================================================

def clicar_previsto():
    """
    Depois de preencher Conteúdo, clica no botão
    'Previsto' para transferir o conteúdo para o
    campo correspondente da plataforma.
    """

    print("  Clicando em 'Previsto'...")

    clicar(
        config.CAMPOS["previsto"]
    )

    time.sleep(config.DELAY_CAMPO)


# ============================================================
# ROLAGEM DO MODAL
# ============================================================

def rolar_modal():
    """
    Arrasta a barra de rolagem do modal.

    Origem:
        scroll_start

    Destino:
        scroll_end
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
    """
    Preenche o campo Metodologia após a rolagem.
    """

    valor = aula.get(
        config.MAPEAMENTO_CSV["metodologia"],
        ""
    )

    if (
        config.IGNORAR_CAMPOS_VAZIOS
        and not valor
    ):
        return

    print(
        f"    metodologia: {valor[:60]}"
    )

    preencher_campo(
        "metodologia",
        valor
    )


def preencher_recursos(aula):
    """
    Preenche o campo Recursos após a rolagem.
    """

    valor = aula.get(
        config.MAPEAMENTO_CSV["recursos"],
        ""
    )

    if (
        config.IGNORAR_CAMPOS_VAZIOS
        and not valor
    ):
        return

    print(
        f"    recursos: {valor[:60]}"
    )

    preencher_campo(
        "recursos",
        valor
    )


# ============================================================
# PREENCHIMENTO COMPLETO DO MODAL
# ============================================================

def preencher_modal(aula):
    """
    Executa a sequência exata definida para a plataforma:

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

    # --------------------------------------------------------
    # ETAPA 1 — TÍTULO
    # --------------------------------------------------------

    preencher_titulo(aula)

    # --------------------------------------------------------
    # ETAPA 2 — CONTEÚDO
    # --------------------------------------------------------

    preencher_conteudo(aula)

    # --------------------------------------------------------
    # ETAPA 3 — PREVISTO
    # --------------------------------------------------------

    clicar_previsto()

    # --------------------------------------------------------
    # ETAPA 4 — ROLAR MODAL
    # --------------------------------------------------------

    rolar_modal()

    # --------------------------------------------------------
    # ETAPA 5 — METODOLOGIA
    # --------------------------------------------------------

    preencher_metodologia(aula)

    # --------------------------------------------------------
    # ETAPA 6 — RECURSOS
    # --------------------------------------------------------

    preencher_recursos(aula)

    print()
    print("  ✓ Campos preenchidos.")


# ============================================================
# SALVAR
# ============================================================

def salvar():
    """
    Salva o registro somente quando MODO_TESTE=False.

    Durante o teste não haverá qualquer clique no botão
    Salvar.
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
    """
    Processa uma única aula.
    """

    print()
    print("=" * 60)
    print(f"AULA / REGISTRO {indice + 1}")
    print("=" * 60)

    print(
        f"Data:     {aula.get('data', '')}"
    )

    print(
        f"Turma:    {aula.get('turma', '')}"
    )

    print(
        f"Aula:     {aula.get('aula', '')}"
    )

    print(
        f"Título:   {aula.get('titulo', '')}"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # ABRIR EDIÇÃO
    # --------------------------------------------------------

    if not abrir_edicao():

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
    print(" AUTOMATIZADOR DE PLANOS DE AULA - v0.1")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. CARREGAR CSV
    # --------------------------------------------------------

    print()
    print("Carregando dados de aulas.csv...")

    aulas = carregar_csv()

    # --------------------------------------------------------
    # 2. IDENTIFICAR REGISTROS PENDENTES
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # VERIFICAR SE EXISTEM REGISTROS
    # --------------------------------------------------------

    if not pendentes:

        print()
        print(
            "Nenhuma aula pendente para processamento."
        )

        return

    # --------------------------------------------------------
    # TESTE — PRIMEIRO REGISTRO PENDENTE
    # --------------------------------------------------------

    indice, aula = pendentes[0]

    print()
    print("=" * 60)
    print(" PRÓXIMO REGISTRO")
    print("=" * 60)

    print(
        f"Índice:   {indice}"
    )

    print(
        f"Data:     {aula.get('data', '')}"
    )

    print(
        f"Turma:    {aula.get('turma', '')}"
    )

    print(
        f"Aula:     {aula.get('aula', '')}"
    )

    print(
        f"Título:   {aula.get('titulo', '')}"
    )

    print("=" * 60)

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

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print(" EXECUÇÃO FINALIZADA")
    print("=" * 60)


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()
