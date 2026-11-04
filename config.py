CSV_PATH = "dados/aulas.csv"

# Substitua por um recorte real do botão Editar.
IMAGEM_EDITAR = "elementos/editar.png"
CONFIANCA_IMAGEM = 0.85

# ------------------------------------------------------------
# PLAYWRIGHT / NAVEGADOR
# ------------------------------------------------------------
# O navegador precisa estar iniciado com depuração remota.
# Exemplo no Chrome: --remote-debugging-port=9222
PLAYWRIGHT_CDP_URL = "http://127.0.0.1:9222"
PORTAL_DOMINIO = "portalsge.fiepi.com.br"
TIMEOUT_DOM = 15

# Estratégia para localizar a linha da aula.
# O CSV atual não possui data/turma/aula, portanto, no teste,
# usamos a posição do registro na lista de Editar.
COLUNAS_IDENTIFICACAO = {
    "data": "data",
    "turma": "turma",
    "aula": "aula",
}

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

# Índice do botão Editar quando o CSV não possui colunas
# de identificação da linha. 0 = primeiro Editar.
EDITAR_INDICE_FALLBACK = 0

# campo_do_modal -> coluna_do_CSV
MAPEAMENTO_CSV = {
    "titulo": "tipo de aula",
    "conteudo": "conteúdo previsto",
    "metodologia": "lição de casa",
    "recursos": "observação",
}
