import pyautogui
import time

print("=" * 60)
print(" CAPTURADOR DE COORDENADAS")
print("=" * 60)
print()
print("Mova o mouse para o elemento desejado.")
print("Pressione ENTER para registrar a posição atual.")
print("Digite 'q' + ENTER para sair.")
print()

while True:

    entrada = input("> ")

    if entrada.lower() == "q":
        break

    x, y = pyautogui.position()

    print(f"  Coordenada: ({x}, {y})")
    print()
