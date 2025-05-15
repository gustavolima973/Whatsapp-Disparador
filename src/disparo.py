

import os

import time

import pandas as pd
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def iniciar_driver(config=None):
    options = webdriver.ChromeOptions()
    user_data = config.get("user_data_dir", "./User_Data") if config else "./User_Data"
    options.add_argument(f"--user-data-dir={user_data}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")
    logging.info("Aguardando login no WhatsApp Web...")
    WebDriverWait(driver, config.get("wait_login", 60)).until(
        EC.presence_of_element_located((By.ID, "pane-side"))
    )
    return driver


def formatar_numero(numero):
    numero = ''.join(filter(str.isdigit, str(numero)))
    if numero.startswith('55'):
        return numero
    elif len(numero) in [10, 11]:
        return f"55{numero}"
    return None

def enviar_midia(driver, caminho_arquivo, tipo=None, log_func=print):
    """
    Versão otimizada para envio rápido de mídias no WhatsApp
    """
    try:
        # Verificação rápida do arquivo
        caminho_absoluto = os.path.abspath(caminho_arquivo.strip())
        if not os.path.exists(caminho_absoluto):
            log_func(f"[ERRO] Arquivo não encontrado: {caminho_absoluto}")
            return False

        # Mapeamento rápido de tipos
        tipo = tipo.lower() if tipo else None
        if tipo == 'pdf':
            tipo = 'documento'

        # Autodetecção relâmpago
        if not tipo:
            ext = os.path.splitext(caminho_arquivo)[1].lower()
            tipo = 'imagem' if ext in ('.jpg', '.jpeg', '.png', '.gif', '.webp') else 'documento'

        # Clicagem ultra-rápida no anexo
        botao_anexo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@title='Anexar' or @data-icon='clip' or @data-icon='plus']"))
        )
        driver.execute_script("arguments[0].click();", botao_anexo)

        # Seleção inteligente do tipo
        if tipo == 'imagem':
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(translate(., 'FOTOSVÍDEO', 'fotosvídeo'), 'foto')]"))
            ).click()
        else:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(translate(., 'DOCUMENTO', 'documento'), 'doc')]"))
            ).click()

        # Upload direto
        input_file = driver.find_element(By.XPATH, "//input[@type='file']")
        input_file.send_keys(caminho_absoluto)

        # Envio instantâneo (se possível)
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@data-icon='send' or contains(@aria-label, 'Enviar')]"))
            ).click()
            log_func(f"[SUCESSO] {tipo.upper()} enviado em tempo recorde!")
            return True
        except:
            log_func("[AVISO] Envio rápido falhou, tentando método tradicional...")
            time.sleep(1)
            driver.find_element(By.XPATH, "//*[@data-icon='send']").click()
            return True

    except Exception as e:
        log_func(f"[ERRO] Falha no envio turbo: {str(e)}")
        return False
    
def enviar_mensagem(driver, contato, mensagem, imagem, pdf, config, log_func):
    numero_formatado = formatar_numero(contato)
    if not numero_formatado:
        log_func(f"[AVISO] Número ignorado (inválido): {contato}")
        return


    driver.get(f"https://web.whatsapp.com/send?phone={numero_formatado}&app_absent=0")

    try:
        caixa = WebDriverWait(driver, config.get("wait_load_chat", 15)).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )
        if pd.notna(mensagem):
            for linha in str(mensagem).split("\n"):
                ActionChains(driver).move_to_element(caixa).send_keys(linha).perform()
                ActionChains(driver).send_keys(Keys.SHIFT, Keys.ENTER).perform()
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            log_func(f"[INFO] Mensagem enviada para {contato}")
            time.sleep(1)

        if pd.notna(imagem) and os.path.exists(imagem):
            enviar_midia(driver, imagem, 'imagem', log_func)

        if pd.notna(pdf) and os.path.exists(pdf):
            enviar_midia(driver, pdf, 'pdf', log_func)

    except TimeoutException:
        log_func(f"[ERRO] Tempo esgotado para abrir chat com {contato}")

def processar_planilha(caminho_planilha):
    df = pd.read_excel(caminho_planilha)
    colunas_necessarias = ['nome', 'telefone1', 'mensagem', 'imagem', 'pdf']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"Coluna ausente: {coluna}")
    return df[colunas_necessarias]

def executar_disparo(caminho_planilha, config=None, log_func=print):
    contatos = processar_planilha(caminho_planilha)
    driver = iniciar_driver(config)
    for _, contato in contatos.iterrows():
        try:
            log_func(f"[INFO] Enviando para {contato['nome']} ({contato['telefone1']})")
            enviar_mensagem(driver,
                            contato['telefone1'],
                            contato.get('mensagem', ''),
                            contato.get('imagem', ''),
                            contato.get('pdf', ''),
                            config,
                            log_func)
            time.sleep(config.get("wait_between_msgs", 5))
        except Exception as e:
            log_func(f"[ERRO] Falha geral com {contato['nome']}: {e}")
    driver.quit()
    log_func("[INFO] Disparo concluído.")
