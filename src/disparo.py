# src/disparo.py
import os

import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import logging
import numpy as np

# Configura logs
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./User_Data")  # Mantém a sessão
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")
    logging.info("Aguardando login no WhatsApp Web...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "pane-side"))
    )
    return driver


def formatar_numero(numero):
    return ''.join(filter(str.isdigit, str(numero)))

def enviar_mensagem(driver, contato, mensagem, caminho_imagem, caminho_pdf):
    numero_formatado = formatar_numero(contato)
    
    if not numero_formatado.startswith('55') or len(numero_formatado) < 12:
        logging.warning(f"Número inválido ignorado: {contato}")
        return
    
    link = f"https://web.whatsapp.com/send?phone={numero_formatado}&text={mensagem}"
    driver.get(link)

    
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )
        input_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        ActionChains(driver).move_to_element(input_box).send_keys(Keys.ENTER).perform()
        logging.info(f"Mensagem enviada para {contato}")

        if pd.notna(caminho_imagem) and os.path.exists(caminho_imagem):
            enviar_midia(driver, caminho_imagem, tipo='imagem')

        if pd.notna(caminho_pdf) and os.path.exists(caminho_pdf):
            enviar_midia(driver, caminho_pdf, tipo='pdf')

    except TimeoutException:
        logging.error(f"[ERRO] Tempo esgotado para {contato}")


def enviar_midia(driver, caminho, tipo='imagem'):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-icon='clip']"))
        )
        driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']").click()

        if tipo == 'imagem':
            seletor = "input[accept='image/*,video/mp4,video/3gpp,video/quicktime']"
        else:
            seletor = "input[accept='*']"

        upload = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, seletor))
        )
        upload.send_keys(os.path.abspath(caminho))

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        ).click()

        logging.info(f"{tipo.upper()} enviado: {os.path.basename(caminho)}")

    except Exception as e:
        logging.error(f"[ERRO] Falha ao enviar {tipo}: {e}")

def processar_planilha(caminho_planilha):
    df = pd.read_excel(caminho_planilha)
    colunas_necessarias = ['nome', 'telefone1', 'mensagem', 'imagem', 'pdf']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"Coluna ausente na planilha: {coluna}")
    return df[colunas_necessarias]

def executar_disparo(caminho_planilha):
    contatos = processar_planilha(caminho_planilha)
    driver = iniciar_driver()
    for _, contato in contatos.iterrows():
        try:
            logging.info(f"Enviando para {contato['nome']} ({contato['telefone1']})")  # ← AQUI

            enviar_mensagem(driver,
                            contato['telefone1'],
                            contato['mensagem'],
                            contato.get('imagem', None),
                            contato.get('pdf', None))
            time.sleep(5)
        except Exception as e:
            logging.error(f"[ERRO] {e}")
    driver.quit()

