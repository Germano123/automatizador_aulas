import json
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO DO AUTOMATIZADOR DE PLANOS DE AULA — v0.3.1
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# Diretório base dos planos de aula organizados
DADOS_DIR = "dados"
CSV_PATH = "dados/aulas.csv"
CONFIG_JSON_PATH = BASE_DIR / "config_pontos.json"

# ------------------------------------------------------------
# GUI
# ------------------------------------------------------------
GUI_TITULO = "Automatizador — Planos de Aula"
GUI_LARGURA = 420
GUI_ALTURA = 410
GUI_X = 20
GUI_Y = 100
GUI_SEMPRE_NO_TOPO = True

# ------------------------------------------------------------
# VELOCIDADE E TEMPOS (PyAutoGUI)
# ------------------------------------------------------------
# Multiplicador de velocidade (1.0 = base, 1.5 = +50% de velocidade)
VELOCIDADE = 1.5

# Pausa interna padrão do PyAutoGUI
PAUSE = round(0.20 / VELOCIDADE, 3)

# Delays principais entre as etapas de preenchimento
DELAY_CAMPO = round(0.60 / VELOCIDADE, 3)
DELAY_MODAL = round(1.20 / VELOCIDADE, 3)
DELAY_SCROLL = round(0.80 / VELOCIDADE, 3)
DELAY_SALVAR = round(1.50 / VELOCIDADE, 3)

# Nível inteiro de velocidade do mouse (1 a 10, padrão = 3)
VELOCIDADE_MOUSE_PADRAO = 3
VELOCIDADE_MOUSE = VELOCIDADE_MOUSE_PADRAO

def atualizar_velocidade_mouse(nivel=3):
    global VELOCIDADE_MOUSE, DURACAO_MOVIMENTO, DURACAO_SCROLL
    try:
        nivel = max(1, min(10, int(nivel)))
    except (ValueError, TypeError):
        nivel = 3
    VELOCIDADE_MOUSE = nivel
    # Fator: nível 1 = 1.0x, nível 2 = 1.5x, nível 3 = 2.25x (+50% em relacao a 1.5x), etc.
    # Nível 3: 0.25 / 2.25 = 0.111s (50% mais rapido que os 0.167s anteriores)
    fator = (nivel * 0.75)
    DURACAO_MOVIMENTO = round(0.25 / fator, 3)
    DURACAO_SCROLL = round(0.90 / fator, 3)

# Delays finos de interação e animação do mouse/teclado
atualizar_velocidade_mouse(VELOCIDADE_MOUSE_PADRAO)
DELAY_POS_MOVIMENTO = round(0.20 / VELOCIDADE, 3)
DELAY_CLIPBOARD = round(0.15 / VELOCIDADE, 3)
INTERVALO_DIGITACAO = round(0.10 / VELOCIDADE, 3)
INTERVALO_TEXTO_RAPIDO = round(0.05 / VELOCIDADE, 3)

# Arraste do scrollbar
DELAY_SCROLL_POSICIONAR = round(0.30 / VELOCIDADE, 3)
DELAY_SCROLL_ETAPA = round(0.25 / VELOCIDADE, 3)

# Primeiro teste: preencher, mas NÃO salvar automaticamente.
MODO_TESTE = True

# Se False, campos vazios também serão limpos.
IGNORAR_CAMPOS_VAZIOS = True

# ------------------------------------------------------------
# PONTOS DE INTERESSE (POIs) E AÇÕES DA TELA
# ------------------------------------------------------------
PONTOS_PADRAO = {
    "titulo": {
        "label": "Tipo de Aula (Título)",
        "x": 450,
        "y": 395,
        "tipo": "clique",
        "delay": DELAY_CAMPO,
    },
    "conteudo": {
        "label": "Conteúdo Previsto",
        "x": 372,
        "y": 591,
        "tipo": "clique",
        "delay": DELAY_CAMPO,
    },
    "previsto": {
        "label": "Campo Previsto",
        "x": 900,
        "y": 600,
        "tipo": "clique",
        "delay": DELAY_CAMPO,
    },
    "scroll": {
        "label": "Scroll do Modal",
        "x": 1625,
        "y": 295,
        "x2": 1625,
        "y2": 535,
        "tipo": "clique e arraste",
        "delay": DELAY_SCROLL,
    },
    "metodologia": {
        "label": "Metodologia (Lição de Casa)",
        "x": 395,
        "y": 640,
        "tipo": "clique",
        "delay": DELAY_CAMPO,
    },
    "recursos": {
        "label": "Recursos (Observação)",
        "x": 395,
        "y": 760,
        "tipo": "clique",
        "delay": DELAY_CAMPO,
    },
    "salvar": {
        "label": "Botão Salvar",
        "x": 1560,
        "y": 925,
        "tipo": "clique",
        "delay": DELAY_SALVAR,
    },
}

CAMPOS = {}


def atualizar_campos_em_memoria(pontos):
    """Atualiza o dicionário CAMPOS para compatibilidade regressiva."""
    for chave, p in pontos.items():
        if chave == "scroll":
            CAMPOS["scroll_start"] = (int(p.get("x", 1625)), int(p.get("y", 295)))
            CAMPOS["scroll_end"] = (int(p.get("x2", 1625)), int(p.get("y2", 535)))
        else:
            CAMPOS[chave] = (int(p.get("x", 0)), int(p.get("y", 0)))


def obter_config_pontos():
    """Carrega as configurações salvas em JSON ou inicializa com os padrões."""
    if CONFIG_JSON_PATH.exists():
        try:
            with CONFIG_JSON_PATH.open("r", encoding="utf-8") as f:
                dados = json.load(f)
                if isinstance(dados, dict):
                    if "velocidade_mouse" in dados:
                        atualizar_velocidade_mouse(dados["velocidade_mouse"])
                    if "pontos" in dados:
                        atualizar_campos_em_memoria(dados["pontos"])
                        return dados["pontos"]
        except Exception as e:
            print(f"[Aviso] Falha ao carregar {CONFIG_JSON_PATH.name}: {e}")

    # Fallback e criação do JSON padrão
    salvar_config_pontos(PONTOS_PADRAO, VELOCIDADE_MOUSE_PADRAO)
    return PONTOS_PADRAO.copy()


def salvar_config_pontos(pontos, velocidade_mouse=None):
    """Persiste as configurações de pontos, velocidade do mouse e ações em config_pontos.json."""
    if velocidade_mouse is not None:
        atualizar_velocidade_mouse(velocidade_mouse)

    dados = {
        "versao": "0.3.1",
        "velocidade_mouse": VELOCIDADE_MOUSE,
        "pontos": pontos,
    }
    with CONFIG_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    atualizar_campos_em_memoria(pontos)


# Inicializa em memória
atualizar_campos_em_memoria(obter_config_pontos())

# campo_do_modal -> coluna_do_CSV
MAPEAMENTO_CSV = {
    "titulo": "tipo de aula",
    "conteudo": "conteúdo previsto",
    "metodologia": "lição de casa",
    "recursos": "observação",
}
