import csv
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def resolver_diretorio_dados(diretorio_base="dados"):
    caminho = Path(diretorio_base)
    if caminho.exists():
        return caminho
    if not caminho.is_absolute():
        caminho_base = BASE_DIR / caminho
        if caminho_base.exists():
            return caminho_base
    return caminho


def listar_estrutura(diretorio_base="dados"):
    """
    Escaneia a pasta base de dados e retorna a hierarquia:
    {
        "Nome do Curso": ["Unidade 1", "Unidade 2", ...]
    }
    """
    base = resolver_diretorio_dados(diretorio_base)
    if not base.exists():
        return {}

    estrutura = {}
    for curso_dir in sorted(base.iterdir()):
        if curso_dir.is_dir() and not curso_dir.name.startswith((".", "_")):
            unidades = []
            for uc_dir in sorted(curso_dir.iterdir()):
                if uc_dir.is_dir() and not uc_dir.name.startswith((".", "_")):
                    tem_csv = any(uc_dir.glob("*.csv"))
                    if tem_csv:
                        unidades.append(uc_dir.name)
            if unidades:
                estrutura[curso_dir.name] = unidades

    return estrutura


def obter_caminho_csv(curso, unidade, diretorio_base="dados"):
    """
    Localiza o arquivo CSV dentro de dados/<curso>/<unidade>/.
    Prioriza 'aulas.csv', caso contrário pega o primeiro .csv encontrado.
    """
    base = resolver_diretorio_dados(diretorio_base)
    pasta_uc = base / curso / unidade

    if not pasta_uc.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {pasta_uc}")

    padrao = pasta_uc / "aulas.csv"
    if padrao.exists():
        return padrao

    arquivos_csv = list(pasta_uc.glob("*.csv"))
    if arquivos_csv:
        return arquivos_csv[0]

    raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em {pasta_uc}")


def carregar_csv(caminho_csv):
    """Lê o arquivo CSV informado com encoding utf-8-sig."""
    caminho = Path(caminho_csv)
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho.resolve()}")

    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo, delimiter=";"))


def atualizar_status(caminho_csv, indice, status, erro=""):
    """
    Persiste o status de preenchimento da aula diretamente no CSV correspondente.
    Trata possíveis bloqueios caso o arquivo esteja em uso.
    """
    caminho = Path(caminho_csv)

    for tentativa in range(3):
        try:
            with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
                registros = list(csv.DictReader(arquivo, delimiter=";"))

            if not registros or indice >= len(registros):
                return

            fieldnames = list(registros[0].keys())
            if "status" not in fieldnames:
                fieldnames.append("status")
            if "erro" not in fieldnames:
                fieldnames.append("erro")

            registros[indice]["status"] = status
            registros[indice]["erro"] = erro

            with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
                writer = csv.DictWriter(
                    arquivo,
                    fieldnames=fieldnames,
                    delimiter=";"
                )
                writer.writeheader()
                writer.writerows(registros)
            return

        except PermissionError:
            time.sleep(0.5)

    print(f"Aviso: Não foi possível atualizar o CSV {caminho.name} (arquivo pode estar aberto no Excel).")
