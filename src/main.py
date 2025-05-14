# src/main.py

import json
import os

import tkinter as tk
from interface import App, iniciar_interface
from disparo import executar_disparo

def iniciar_interface(config=None):
    root = tk.Tk()
    app = App(root)
    root.mainloop()

def carregar_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRO] Falha ao carregar config.json: {e}")
        return {}

if __name__ == "__main__":
    config = carregar_config()

    # Modo de disparo direto, útil para testes ou .desktop
    if config.get("modo") == "disparo_direto":
        caminho_planilha = config.get("caminho_planilha")
        if caminho_planilha and os.path.exists(caminho_planilha):
            executar_disparo(caminho_planilha)
        else:
            print(f"[ERRO] Caminho da planilha inválido: {caminho_planilha}")
    else:
        iniciar_interface(config)
e