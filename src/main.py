# src/main.py

import json
import os
import sys
import tkinter as tk

# Corrige os imports mesmo com .desktop
sys.path.append(os.path.dirname(__file__))

from interface import iniciar_interface
from disparo import executar_disparo

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

   
    if config.get("modo") == "disparo_direto":
        caminho_planilha = config.get("caminho_planilha")
        if caminho_planilha and os.path.exists(caminho_planilha):
            executar_disparo(caminho_planilha, config)
        else:
            print(f"[ERRO] Caminho da planilha inválido: {caminho_planilha}")
    else:
        iniciar_interface(config)
        