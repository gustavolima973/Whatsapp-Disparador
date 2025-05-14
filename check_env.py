from pathlib import Path
import subprocess

def check_environment():
    base_dir = Path(__file__).parent
    print("🔍 Verificando ambiente...")
    
    # 1. Verifica ChromeDriver
    chromedriver_path = base_dir / "drivers" / "chromedriver-linux64" / "chromedriver"
    if not chromedriver_path.exists():
        print(f"❌ ChromeDriver não encontrado em: {chromedriver_path}")
    else:
        print(f"✅ ChromeDriver encontrado")
        try:
            result = subprocess.run([str(chromedriver_path), "--version"], capture_output=True, text=True)
            print(f"    Versão: {result.stdout.strip()}")
        except Exception as e:
            print(f"    Erro ao verificar versão: {str(e)}")

    # 2. Verifica arquivos essenciais
    essential_files = [
        base_dir / "clientes.xlsx",
        base_dir / "config" / "config.json"
    ]
    
    for file in essential_files:
        if file.exists():
            print(f"✅ {file.name} encontrado")
        else:
            print(f"❌ {file.name} não encontrado")

if __name__ == "__main__":
    check_environment()