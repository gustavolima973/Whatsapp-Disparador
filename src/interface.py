# src/interface.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from disparo import executar_disparo
import os

icone_path = os.path.abspath('icons/icone.ico')


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Disparador WhatsApp")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        self.planilha_path = None

        # Elementos da interface
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
            executar_disparo(self.planilha_path, self.log)
            self.log("[INFO] Disparo concluído.")
        except Exception as e:
            self.log(f"[ERRO] {e}")

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)


def iniciar_interface(config=None):
    root = tk.Tk()
    root.iconbitmap(icone_path)
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_interface()