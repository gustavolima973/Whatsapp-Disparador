📲 Whatsapp Disparador

Um projeto automatizado com interface gráfica para envio de mensagens no WhatsApp Web utilizando Python, Selenium e Tkinter. Permite o envio de mensagens personalizadas, com ou sem imagem, para uma lista de contatos em planilha Excel.
🧰 Tecnologias Utilizadas

    Python 3.10+

    Selenium

    Tkinter

    Pandas

    ChromeDriver

⚙️ Instalação

📦 Requisitos

    Python 3.10 ou superior

    Google Chrome instalado

    ChromeDriver compatível com sua versão do Chrome

💻 Linux

    Clone o repositório:

git clone https://github.com/gustavolima973/Whatsapp-Disparador.git
cd Whatsapp-Disparador

Crie um ambiente virtual (opcional mas recomendado):

python3 -m venv venv
source venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

Garanta que o ChromeDriver esteja instalado:

    Faça download em: https://chromedriver.chromium.org/downloads

    Mova-o para /usr/local/bin/:

    sudo mv chromedriver /usr/local/bin/
    sudo chmod +x /usr/local/bin/chromedriver

Execute o programa:

    python3 src/main.py

🪟 Windows

    Clone ou baixe o repositório e entre na pasta:

    Instale o Python:
    Baixe em: https://www.python.org/downloads/
    Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.

    Instale as dependências: Abra o terminal (cmd ou PowerShell) na pasta do projeto:

pip install -r requirements.txt

Baixe o ChromeDriver:

    Verifique sua versão do Chrome digitando chrome://version no navegador.

    Baixe o ChromeDriver correspondente: https://chromedriver.chromium.org/downloads

    Coloque o chromedriver.exe na pasta do projeto ou em uma pasta no PATH do sistema.

Execute o programa:

    python src/main.py


💾 Funcionalidades

    Envio automatizado de mensagens para contatos via WhatsApp Web.

    Interface gráfica para facilitar a escolha da planilha.

    Suporte a envio de imagens.

    Tenta segundo número caso o primeiro falhe.

    Gera relatório com números que não receberam as mensagens.

🚧 Melhorias Futuras

    Detecção automática de falhas na conexão.

    Interface para editar mensagens antes do envio.

    Dashboard com resultados de envio.

🧑‍💻 Autor

gustavolima973
