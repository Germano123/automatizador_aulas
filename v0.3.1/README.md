# Automatizador de Planos de Aula

Robô assistido de RPA desenvolvido em Python ([PyAutoGUI](https://pyautogui.readthedocs.io/), [Tkinter](https://docs.python.org/3/library/tkinter.html) e [pyperclip](https://pypi.org/project/pyperclip/)) para acelerar o preenchimento de planos pedagógicos no Portal do Professor com simulação visual de periféricos.

---

## Recursos da Versão Atual

1. **Catálogo Hierárquico de Dados**:
   - Organização automática por **Curso** e **Unidade Curricular** sob a pasta `dados/`.
   - Detecção dinâmica de novas turmas e UCs sem necessidade de alterar código-fonte.
   - Menus suspensos (`ttk.Combobox`) para alternância instantânea de turmas.

2. **Navegação Direta e Avanço Automático**:
   - Salto direto por número de aula digitável: `AULA [ XX ] / YY [Ir]`.
   - Avanço automático para a próxima aula após a confirmação da inserção.
   - Navegação tradicional com botões `◀ ANTERIOR` e `PRÓXIMA ▶`.

3. **Painel Visual de Configurações (`⚙ Configurações`)**:
   - Listagem vertical de todos os pontos de tela (POIs).
   - Configuração do **tipo de ação** por ponto (`clique`, `duplo clique`, `clique direito`, `clique e arraste`).
   - Ajuste independente de **espera pós-comando** (delays) por etapa.
   - **Controle geral de velocidade do mouse (1 a 10)** com seletor numérico.
   - **Capturador interativo de coordenadas (🎯)**: conta 2 segundos para você posicionar o mouse sobre o elemento do portal e captura as coordenadas automaticamente.
   - Persistência das configurações em `config_pontos.json` com botão de restauração de padrões.

4. **Auto-Ocultação do Painel**:
   - O overlay minimiza automaticamente ao clicar em **INSERIR ESTA AULA**, evitando sobrepor botões e campos do portal.
   - Reaparece automaticamente no topo da tela logo após a conclusão da inserção.

5. **Segurança e Integridade**:
   - `FAILSAFE = True` ativo (mover o cursor para qualquer canto da tela aborta o robô imediatamente).
   - Flag `MODO_TESTE` para preenchimento sem clique acidental no botão Salvar.
   - Tratamento de concorrência com Excel e salvamento do status de cada aula diretamente no CSV.

---

## Estrutura de Pastas de Dados

Os planos de aula estão organizados na seguinte estrutura:

```text
v0.3.1/dados/
├── Almoxarife/
│   ├── Fundamentos da Indústria 4.0 (12h)/
│   │   └── aulas.csv
│   └── Fundamentos de Tecnologia da Informação (20h)/
│       └── aulas.csv
├── Comprador/
│   ├── Fundamentos da Indústria 4.0 (12h)/
│   │   └── aulas.csv
│   └── Fundamentos de Tecnologia da Informação (20h)/
│       └── aulas.csv
└── Operador de Computador/
    ├── Ferramentas de produtividade e recursos web (80h)/
    │   └── aulas.csv
    ├── Fundamentos de Sistema Operacional (20h)/
    │   └── aulas.csv
    ├── Fundamentos de Tecnologia da Informação (40h)/
    │   └── aulas.csv
    └── Instalação de Aplicativos e Periféricos (20h)/
        └── aulas.csv
```

### Formato Obrigatório dos Arquivos CSV
* **Codificação**: `UTF-8-SIG` (BOM preservado para compatibilidade nativa com Excel).
* **Delimitador**: Ponto e vírgula (`;`).
* **Cabeçalho**: `tipo de aula;conteúdo previsto;lição de casa;observação`
* **Tipos de Aula Suportados**: `Teórica`, `Prática`, `Produção`, `Apresentação` ou `Demonstração`.

---

## Instalação

```powershell
pip install -r requirements.txt
```

---

## Como Executar

1. Abra o navegador, faça login no Portal do Professor e acesse a turma desejada.
2. Localize a aula na lista e clique manualmente em **Editar**.
3. Inicie o automatizador:

```powershell
python main.py
```

4. Na interface:
   - Selecione o **Curso** e a **Unidade Curricular**.
   - Se necessário, digite o número da aula no campo numérico e pressione **Enter** (ou use as setas `◀` / `▶`).
   - Se estiver configurando pela primeira vez na tela, clique em **⚙ Configurações** para calibrar as posições com o botão 🎯.
   - Clique em **INSERIR ESTA AULA** (ou pressione a tecla **Enter**).
   - O painel ocultará, o robô preencherá o formulário, e a janela reaparecerá pronta na aula seguinte.

---

## Modo Teste

Por padrão em `config.py`:

```python
MODO_TESTE = True
```

No modo de teste, o programa preenche os campos do modal, mas não clica em Salvar, permitindo validação visual dos dados antes do envio final.
