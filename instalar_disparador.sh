#!/bin/bash

# Caminho absoluto do projeto
PROJETO_DIR="$(cd "$(dirname "$0")" && pwd)"

# Nome do pacote
PACOTE="whatsapp_disparador"

# Caminho do ícone (ajuste se necessário)
ICONE_PATH="$PROJETO_DIR/assets/icone.png"

# Caminho do executável após instalação (local)
BIN_PATH="$HOME/.local/bin/disparador-whatsapp"

# Mensagem inicial
echo "[INFO] Instalando o pacote local..."

# Instalação via pip
pip install .

# Verifica se instalou corretamente
if [ ! -f "$BIN_PATH" ]; then
    echo "[ERRO] Não foi possível encontrar $BIN_PATH"
    exit 1
fi

# Criação do .desktop
DESKTOP_FILE="$HOME/.local/share/applications/whatsapp-disparador.desktop"

echo "[INFO] Criando atalho em $DESKTOP_FILE"

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Name=WhatsApp Disparador
Exec=$BIN_PATH
Icon=$ICONE_PATH
Type=Application
Categories=Utility;
Terminal=false
EOF

chmod +x "$DESKTOP_FILE"

echo "[SUCESSO] Atalho criado com sucesso!"
echo "Você pode procurar por 'WhatsApp Disparador' no menu de aplicativos."
