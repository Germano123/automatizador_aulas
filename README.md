# Automatizador de Planos de Aula — v0.2

## Objetivo

Automatizar o preenchimento dos planos de aula no Portal do Professor.

A versão 0.2 substitui a procura visual do botão `Editar` por localização no DOM através do Playwright.

O preenchimento do modal continua usando as coordenadas configuradas no `config.py`, pois já foram medidas na interface real.

## Arquitetura

```text
aulas.csv
   ↓
Python
   ↓
Playwright/CDP
   ↓
DOM do Portal → localizar "Editar"
   ↓
PyAutoGUI
   ↓
coordenadas do modal
   ↓
Título → Conteúdo → Previsto → Scroll → Metodologia → Recursos
```

Não é utilizado crawler. O Playwright apenas controla a página que já está aberta no navegador.

## Instalação

```powershell
python -m pip install -r requirements.txt
```

Como estamos conectando ao Chrome existente via CDP, não é necessário instalar outro navegador pelo Playwright.

## Iniciar o Chrome com depuração remota

O Playwright precisa conseguir se conectar ao navegador existente.

Feche as janelas do Chrome usadas no teste e abra uma instância dedicada com:

```powershell
chrome.exe --remote-debugging-port=9222 --user-data-dir="%TEMP%\PortalProfessorAutomation"
```

Se `chrome.exe` não estiver no PATH, use o caminho completo do executável do Chrome.

Depois:

1. Abra o Portal do Professor nessa janela.
2. Faça login normalmente.
3. Navegue até a página do plano de aula.
4. Deixe a página aberta.

A sessão desse perfil fica separada do Chrome normal.

## Execução

Com o ambiente virtual ativado:

```powershell
python main.py
```

O programa:

1. carrega `dados/aulas.csv`;
2. identifica os registros pendentes;
3. mostra no terminal o primeiro registro;
4. conecta ao Chrome via CDP;
5. espera 1,5 segundo para você deixar o Portal em primeiro plano;
6. procura `Editar` diretamente no DOM;
7. clica em `Editar`;
8. preenche o modal usando as coordenadas;
9. clica em `Previsto`;
10. arrasta o scroll;
11. preenche Metodologia e Recursos;
12. não clica em Salvar enquanto `MODO_TESTE = True`.

## Teste inicial

Mantenha:

```python
MODO_TESTE = True
```

Assim o botão Salvar nunca será clicado e o registro não será marcado como OK.

## Identificação da linha

A versão atual aceita duas estratégias.

### CSV com data/turma/aula

Se o CSV possuir:

```text
data
turma
aula
```

o programa tenta localizar a `<tr>` correspondente e clicar no `Editar` daquela linha.

### CSV atual

O CSV enviado nesta versão contém:

```text
tipo de aula
conteúdo previsto
lição de casa
observação
```

Como não existem data/turma/aula, o programa utiliza o índice configurado em:

```python
EDITAR_INDICE_FALLBACK = 0
```

Para o primeiro teste, `0` significa o primeiro botão `Editar` encontrado no DOM.

## Segurança

`pyautogui.FAILSAFE` está ativo.

Para interromper uma ação de PyAutoGUI, mova o mouse para o canto superior esquerdo.

Não altere `MODO_TESTE` para `False` até confirmar visualmente todo o fluxo.
