CSV_PATH = "dados/aulas.csv"

# Substitua por um recorte real do botão Editar.
IMAGEM_EDITAR = "elementos/editar.png"
CONFIANCA_IMAGEM = 0.85

PAUSE = 0.20
DELAY_CAMPO = 0.20
DELAY_MODAL = 1.0
DELAY_SALVAR = 1.5
TIMEOUT_EDITAR = 10

# Primeiro teste: preencher, mas NÃO salvar.
MODO_TESTE = True

IGNORAR_CAMPOS_VAZIOS = True

# Coordenadas do modal. SUBSTITUA pelas coordenadas reais.
CAMPOS = {
    "titulo": (450, 395),
    "conteudo": (372, 591),
    "previsto": (900, 600),
    "metodologia": (395, 640),
    "recursos": (385, 640),
    "scroll_start": (1625, 295),
    "scroll_end": (1625, 535),
    "salvar": (1560, 925),
}

BOTAO_SALVAR = (1100, 750)

# campo_do_modal -> coluna_do_CSV
MAPEAMENTO_CSV = {
    "titulo": "tipo de aula",
    "conteudo": "conteúdo previsto",
    "metodologia": "lição de casa",
    "recursos": "observação",
}
