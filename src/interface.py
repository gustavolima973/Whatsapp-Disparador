# interface.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from disparo import iniciar_driver, enviar_mensagens
class WhatsAppApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disparador WhatsApp")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="Selecione a planilha com os contatos e mensagens:")
        self.label.pack(pady=10)

        self.btn_selecionar = tk.Button(root, text="Selecionar Planilha", command=self.selecionar_planilha)
        self.btn_selecionar.pack(pady=10)

        self.label_arquivo = tk.Label(root, text="Nenhum arquivo selecionado.")
        self.label_arquivo.pack(pady=5)

        self.btn_enviar = tk.Button(root, text="Iniciar Envio", command=self.iniciar_envio, state=tk.DISABLED)
        self.btn_enviar.pack(pady=20)

        self.log_text = tk.Text(root, height=8, width=60, state=tk.DISABLED)
        self.log_text.pack(pady=5)

    def selecionar_planilha(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if caminho:
            self.caminho_planilha = caminho
            self.label_arquivo.config(text=os.path.basename(caminho))
            self.btn_enviar.config(state=tk.NORMAL)

    def iniciar_envio(self):
        self.log("[INFO] Iniciando envio... Aguarde o carregamento do WhatsApp Web.")
        threading.Thread(target=self.enviar).start()

    def enviar(self):
        try:
            driver = iniciar_driver()
            enviar_mensagens(driver, self.caminho_planilha, log_func=self.log)
            self.log("[FINALIZADO] Envio concluído.")
        except Exception as e:
            self.log(f"[ERRO] Erro ao iniciar envio: {e}")

    def log(self, mensagem):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    app = WhatsAppApp(root)
    root.mainloop()
