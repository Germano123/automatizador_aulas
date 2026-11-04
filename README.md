# Automatizador de Planos de Aula — v0.1

## Objetivo
Primeiro protótipo para testar a automação do Portal do Professor.

## Instalação
```bash
python -m pip install -r requirements.txt
```

## Preparação
1. Abra o Portal do Professor.
2. Deixe a tabela de aulas visível.
3. Faça um pequeno recorte do botão `Editar`.
4. Salve o recorte em `elementos/editar.png`.
5. Ajuste as coordenadas de `config.py`.

## Teste inicial
Mantenha:
```python
MODO_TESTE = True
```

O programa procura `Editar`, abre o modal e preenche os campos, mas não salva.

Quando estiver validado, altere para:
```python
MODO_TESTE = False
```

## Segurança
O `pyautogui.FAILSAFE` está ativo. Mova o mouse para o canto superior esquerdo para interromper.
