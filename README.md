# Disparador de Mensagens via WhatsApp Web

Este projeto automatiza o envio de mensagens personalizadas via WhatsApp Web utilizando **Selenium** e **Python**, com suporte a **mensagens de texto, imagens e documentos (PDFs)**. Ele também inclui uma interface gráfica simples feita com `tkinter` para facilitar o uso sem depender do terminal.

## ✅ Funcionalidades

- Envio automático de mensagens personalizadas para contatos listados em um arquivo Excel.
- Suporte ao envio de:
  - Texto
  - Imagens (enviadas corretamente como mídia)
  - Documentos (PDFs)
- Suporte a dois números por contato (`Telefone1` e `Telefone2`)
- Registro automático dos contatos que não receberam a mensagem (`nao_enviados.xlsx`)
- Interface gráfica amigável para facilitar o uso

## 🧰 Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatível com a versão do seu Chrome
- Sessão do WhatsApp Web previamente autenticada

## 💻 Instalação

### Linux

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install -r requirements.txt

Windows

    Instale o Python 3: https://www.python.org/downloads/

    Instale as dependências:

    pip install -r requirements.txt

    Faça download do ChromeDriver compatível com sua versão do Chrome e adicione ao PATH do sistema.

📄 Estrutura esperada da planilha (Excel)

A planilha deve conter as colunas abaixo:
Nome	Telefone1	Telefone2	Mensagem	Imagem	PDF
João	55999999999		Olá João!	/caminho/imagem.jpg	/caminho/arquivo.pdf

    Mensagem: Pode conter múltiplas linhas (use Alt + Enter no Excel).

    Imagem: Caminho completo ou relativo até o arquivo.

    PDF: Caminho completo ou relativo até o arquivo.

🚀 Como usar

    Verifique se o Chrome está fechado e sua conta do WhatsApp Web já está logada.

    Execute a interface:

    python3 main.py

    Selecione o arquivo Excel e clique em "Iniciar disparo".

    O script abrirá o WhatsApp Web automaticamente e começará os envios.

📁 Estrutura do Projeto

whatsapp_disparador/
├── main.py                  # Interface gráfica (Tkinter)
├── disparo.py               # Lógica de envio com Selenium
├── requirements.txt         # Dependências
├── README.md                # Documentação
└── nao_enviados.xlsx        # Contatos que não receberam a mensagem

🧠 Possíveis melhorias futuras

    Logs detalhados por envio (em arquivo .txt ou .csv)

    Integração com banco de dados para controle de campanhas

    Suporte a envio em lote com divisão automática de planilhas grandes

    Integração com email para notificação do status de envio

    Suporte a áudios e vídeos

    Controle de tempo mais avançado entre envios (modo stealth)

🤝 Contribuição

Sugestões e melhorias são muito bem-vindas. Abra uma issue ou envie um pull request!

🧑‍💻 Autor

gustavolima973
