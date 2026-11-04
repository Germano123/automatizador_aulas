# Automatizador de Planos de Aula — v0.3.1

## Objetivo

Nesta versão, o usuário localiza manualmente a aula no Portal do Professor,
clica em **Editar** e depois usa a GUI para inserir os dados da linha atual do CSV.

O programa não procura mais o botão Editar.

## Correções desta versão

1. A linha atual do CSV é explicitamente lida e enviada para `preencher_aula()`.
2. O terminal mostra os valores que serão inseridos.
3. Cada campo faz:
   - clique;
   - espera;
   - `Ctrl+A`;
   - colagem via clipboard;
   - espera.
4. O arraste do scrollbar agora é explícito:
   - `moveTo`;
   - `mouseDown`;
   - `moveTo` com duração;
   - `mouseUp`.
5. A GUI não é atualizada diretamente pela thread do PyAutoGUI; o resultado retorna à thread principal do Tkinter.
6. O salvamento continua desativado enquanto `MODO_TESTE = True`.

## Instalação

```powershell
pip install -r requirements.txt
```

## Execução

Abra o Portal, localize a aula desejada e clique manualmente em **Editar**.

Depois:

```powershell
python main.py
```

Na GUI, escolha a aula correspondente e clique em:

**INSERIR ESTA AULA**

## Importante

As coordenadas em `config.py` são coordenadas absolutas da tela:

```python
CAMPOS = {
    "titulo": ...,
    "conteudo": ...,
    "previsto": ...,
    "metodologia": ...,
    "recursos": ...,
    "scroll_start": ...,
    "scroll_end": ...,
}
```

Se o mouse chegar ao campo mas o conteúdo não for inserido, verifique
primeiramente se a coordenada realmente está dentro da área editável.

## Modo teste

O padrão é:

```python
MODO_TESTE = True
```

Portanto o programa preenche, mas não clica em Salvar.

Não altere para `False` até o preenchimento estar validado.
