# Automatizador de Planos de Aula — v0.3

## Nova abordagem

A versão 0.3 abandona a tentativa de localizar automaticamente o botão **Editar** no Portal.

O processo agora é deliberadamente híbrido:

1. O usuário abre o Portal do Professor.
2. Localiza visualmente a aula correta.
3. Clica manualmente em **Editar**.
4. Usa o painel flutuante do automatizador para selecionar a aula correspondente.
5. Clica em **INSERIR ESTA AULA**.
6. O PyAutoGUI preenche o formulário aberto.
7. O usuário confere o resultado e salva manualmente no Portal.
8. O usuário clica em **PRÓXIMA** e repete o processo.

## GUI flutuante

A GUI foi construída com Tkinter e possui:

- número da aula atual e total de aulas;
- descrição/tipo da aula;
- botão **Anterior**;
- botão **Próxima**;
- botão **Inserir esta aula**;
- status da operação;
- botão para ocultar o painel.

A janela utiliza `-topmost`, permanecendo acima do Portal e de outras aplicações. Ela não força o foco continuamente. Assim, é possível clicar e trabalhar no Portal enquanto o painel continua visível.

## Atalhos

Quando o painel estiver com foco:

- `←` = aula anterior
- `→` = próxima aula
- `Enter` = inserir aula

## Dependências

```powershell
pip install -r requirements.txt
```

Não é necessário Playwright nesta versão.

## Execução

```powershell
python main.py
```

Depois de iniciar:

1. posicione o painel em um canto conveniente da tela;
2. abra a aula desejada no Portal;
3. clique manualmente em **Editar**;
4. confirme o número correspondente no painel;
5. clique **INSERIR ESTA AULA**;
6. confira o preenchimento;
7. salve manualmente no Portal;
8. clique **PRÓXIMA**.

## Modo de teste

Em `config.py`:

```python
MODO_TESTE = True
```

Nesse modo o programa preenche os campos, mas não clica no botão Salvar.

Para automatizar o salvamento futuramente:

```python
MODO_TESTE = False
```

Recomenda-se manter `True` durante os primeiros testes.

## Coordenadas

As coordenadas do formulário continuam em `config.py`:

```python
CAMPOS = {
    "titulo": (...),
    "conteudo": (...),
    "previsto": (...),
    "metodologia": (...),
    "recursos": (...),
    "scroll_start": (...),
    "scroll_end": (...),
    "salvar": (...),
}
```

Elas devem corresponder à resolução/escala da tela usada no Portal.

## Observação importante

A v0.3 assume que o usuário abriu manualmente o formulário correto antes de clicar em **INSERIR ESTA AULA**. O programa não verifica qual aula está aberta no Portal.

Isso é intencional: reduz a complexidade e torna o fluxo mais previsível para o MVP.
