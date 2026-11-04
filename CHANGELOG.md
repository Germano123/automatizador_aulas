# CHANGELOG — Automatizador de Planos de Aula

Todas as alterações relevantes deste projeto estão documentadas neste arquivo.

---

## [v0.3.1 - Atualização 2] - 2026-11-04

### Adicionado
- **Controlador Geral de Velocidade do Mouse**: Seletor numérico de 1 a 10 no cabeçalho do Painel de Configurações, com recálculo automático da duração dos deslocamentos e do arraste do scrollbar.
- **Navegação Direta por Número de Aula**: Campo de entrada numérica editável `AULA [ XX ] / YY [Ir]` com acionamento por botão ou tecla `Enter`.
- **Avanço Automático de Aula**: Transição automática para a próxima aula subsequente assim que o preenchimento da aula atual é concluído com sucesso.
- **Auto-Ocultação do Painel**: Minimização temporária da janela durante o preenchimento para desobstruir a tela durante as ações do PyAutoGUI, reaparecendo com o status atualizado.
- **Arquivo `.gitignore`**: Padronização para ignorar `__pycache__`, arquivos compilados `.pyc`, pastas de ambiente virtual `venv/` e configurações de IDEs.

### Modificado
- **Aceleração da Automação**: Velocidade de movimentação do cursor aumentada em 50% (duração reduzida de 0.167s para 0.111s no nível padrão).
- **Tratamento de Tipos de Aula**: Suporte aos tipos `Demonstração` e `Apresentação` com mapeamento e envio das 3 primeiras letras no modal.

---

## [v0.3.1 - Atualização 1] - 2026-10-26

### Adicionado
- **Painel Visual de Configurações (`painel_config.py`)**:
  - Janela rolável dedicada para inspeção e edição de todos os pontos de interesse (POIs).
  - Seleção do tipo de ação por ponto (`clique`, `duplo clique`, `clique direito` e `clique e arraste`).
  - Ajuste fino dos tempos de espera pós-comando em segundos.
  - Botão interativo de captura de coordenadas com mouse (🎯) com contagem regressiva de 2 segundos.
  - Persistência em `config_pontos.json` com botão de restauração de padrões.
- **Gerenciador Dinâmico de Dados (`gerenciador_dados.py`)**:
  - Varredura e carregamento hierárquico por Curso e Unidade Curricular.
  - Retentativas com tratamento de `PermissionError` para arquivos abertos no Excel.
- **Catálogo Estruturado de Unidades Curriculares**:
  - Organização dos arquivos CSV nas pastas `Almoxarife`, `Comprador` e `Operador de Computador`.
  - Geração de templates padronizados em `UTF-8-SIG` com delimitador `;`.

---

## [v0.3.1] - 2026-09-25

### Adicionado
- Leitura e gravação do status de execução diretamente no arquivo CSV.
- Exibição no terminal dos valores a serem preenchidos.
- Fluxo de preenchimento via clipboard (`pyperclip` + `Ctrl+V`) para preservação de acentuação e velocidade.
- Arraste explícito da barra de rolagem vertical do modal.
- Execução em thread separada com retorno assíncrono para a thread principal do Tkinter.
- Flag de segurança `MODO_TESTE`.
