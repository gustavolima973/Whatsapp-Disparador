# src/interface.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, PhotoImage
from disparo import executar_disparo
import os
import platform

icone_path = os.path.abspath('icons/icone.png')


class App:
    def __init__(self, root, config=None):
        self.root = root
        self.config = config or {}
        self.planilha_path = self.config.get('caminho_planilha')

        self.root.title("Disparador WhatsApp")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

  
        tk.Label(root, text="Selecione a planilha de contatos:").pack(pady=10)
        tk.Button(root, text="Selecionar Planilha", command=self.selecionar_planilha).pack(pady=5)
        tk.Button(root, text="Iniciar Disparo", command=self.iniciar_disparo_interface).pack(pady=5)

        self.log_text = scrolledtext.ScrolledText(root, height=7, width=50)
        self.log_text.pack(pady=10)

    def selecionar_planilha(self):
        filepath = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if filepath:
            self.planilha_path = filepath
            self.log(f"[INFO] Planilha selecionada: {filepath}")
        else:
            self.log("[ERRO] Nenhuma planilha selecionada.")

    def iniciar_disparo_interface(self):
        if not self.planilha_path:
            messagebox.showerror("Erro", "Por favor, selecione uma planilha antes de iniciar.")
            return
        try:
            self.log("[INFO] Iniciando disparo...")
            self.config['caminho_planilha'] = self.planilha_path
            executar_disparo(self.planilha_path, self.config, self.log)
            self.log("[INFO] Disparo concluído.")
        except Exception as e:
            self.log(f"[ERRO] {e}")

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)


def iniciar_interface(config=None):
    root = tk.Tk()
    if platform.system() != "Windows":
        root.iconphoto(True, PhotoImage(file=icone_path))
    else:
        root.iconbitmap("icons/icone.ico")
    app = App(root, config)
    root.mainloop()
    