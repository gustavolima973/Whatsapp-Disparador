import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from disparo import iniciar_driver, enviar_mensagens
import threading
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Disparador")

        # Botão para selecionar planilha
        self.botao_selecionar = tk.Button(root, text="Selecionar Planilha", command=self.selecionar_arquivo)
        self.botao_selecionar.pack(pady=10)

        # Botão para iniciar disparo
        self.botao_iniciar = tk.Button(root, text="Iniciar Disparo", command=self.iniciar_disparo, state=tk.DISABLED)
        self.botao_iniciar.pack(pady=10)

        # Área de log
        self.log = scrolledtext.ScrolledText(root, width=60, height=20)
        self.log.pack(padx=10, pady=10)

        self.caminho_planilha = None

    def selecionar_arquivo(self):
        self.caminho_planilha = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.caminho_planilha:
            self.botao_iniciar.config(state=tk.NORMAL)
            self.log.insert(tk.END, f"Planilha selecionada: {self.caminho_planilha}\n")
            self.log.see(tk.END)

    def iniciar_disparo(self):
        self.log.insert(tk.END, "Iniciando disparo...\n")
        self.log.see(tk.END)
        threading.Thread(target=self.disparar_mensagens).start()  # Para não travar a interface

    def disparar_mensagens(self):
        try:
            driver = iniciar_driver()
            enviar_mensagens(driver, self.caminho_planilha, log_func=self.atualizar_log)
            driver.quit()
            self.atualizar_log("Disparo concluído!\n")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.atualizar_log(f"Erro: {e}\n")

    def atualizar_log(self, mensagem):
        self.log.insert(tk.END, mensagem + "\n")
        self.log.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
