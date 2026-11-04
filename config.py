# ============================================================
# CONFIGURAÇÃO DO AUTOMATIZADOR DE PLANOS DE AULA — v0.3.1
# ============================================================

CSV_PATH = "dados/aulas.csv"

# ------------------------------------------------------------
# GUI
# ------------------------------------------------------------
GUI_TITULO = "Automatizador — Planos de Aula"
GUI_LARGURA = 360
GUI_ALTURA = 285
GUI_X = 20
GUI_Y = 100
GUI_SEMPRE_NO_TOPO = True

# ------------------------------------------------------------
# PYAutoGUI
# ------------------------------------------------------------
PAUSE = 0.20

# Tempo entre as etapas de preenchimento.
DELAY_CAMPO = 0.60
DELAY_MODAL = 1.20
DELAY_SCROLL = 0.80
DELAY_SALVAR = 1.5

# Primeiro teste: preencher, mas NÃO salvar automaticamente.
MODO_TESTE = True

# Se False, campos vazios também serão limpos.
IGNORAR_CAMPOS_VAZIOS = True

# Coordenadas do modal.
# CONFIRA estas posições na sua tela antes do uso em lote.
CAMPOS = {
    "titulo": (450, 395),
    "conteudo": (372, 591),
    "previsto": (900, 600),

    # Após o scroll:
    "metodologia": (395, 640),
    "recursos": (385, 640),

    # Barra de rolagem vertical do modal:
    "scroll_start": (1625, 295),
    "scroll_end": (1625, 535),

    "salvar": (1560, 925),
}

# campo_do_modal -> coluna_do_CSV
MAPEAMENTO_CSV = {
    "titulo": "tipo de aula",
    "conteudo": "conteúdo previsto",
    "metodologia": "lição de casa",
    "recursos": "observação",
}
