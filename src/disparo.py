from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import os
import re


def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=" + os.path.expanduser("~/.config/google-chrome"))
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--start-maximized")

    caminho_driver = "/usr/local/bin/chromedriver"
    service = Service(caminho_driver)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def formatar_numero(numero):
    """Remove caracteres não numéricos e adiciona código do país se necessário"""
    numero = re.sub(r'\D', '', numero)
    if numero.startswith('55'):
        return numero
    elif len(numero) == 11 or len(numero) == 10:
        return '55' + numero
    else:
        return None


def tentar_enviar(driver, telefone, mensagem, imagem):
    if not telefone or pd.isna(telefone):
        return False

    try:
        link_whatsapp = f"https://web.whatsapp.com/send?phone={telefone}&text&app_absent=0" 
        driver.get(link_whatsapp)
        


        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )

        caixa_texto = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        caixa_texto.click()


        if mensagem and not pd.isna(mensagem):
            for linha in mensagem.split('\n'):
                caixa_texto.send_keys(linha)
                caixa_texto.send_keys('\n')

        if imagem and not pd.isna(imagem):
            botao_anexo = driver.find_element(By.CSS_SELECTOR, "span[data-icon='clip']")
            botao_anexo.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            upload = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            caminho_imagem = os.path.expanduser(imagem.strip())
            upload.send_keys(caminho_imagem)

            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
            )
            botao_enviar_imagem = driver.find_element(By.CSS_SELECTOR, "span[data-icon='send']")
            botao_enviar_imagem.click()
     
        else:
            caixa_texto.send_keys('\n')

        time.sleep(random.uniform(3, 6))
        return True

    except Exception as e:
        print(f"Erro ao tentar enviar para {telefone}: {e}")
        return False


def enviar_mensagens(driver, caminho_excel, log_func=print):
    campanha = pd.read_excel(caminho_excel)

    for index, row in campanha.iterrows():
        nome = row.get("Nome")
        telefone1 = formatar_numero(str(row.get("Telefone1")))
        telefone2 = formatar_numero(str(row.get("Telefone2"))) if not pd.isna(row.get("Telefone2")) else None
        mensagem = row.get("Mensagem")
        imagem = row.get("Imagem", None)

        numero_para_tentar = [telefone1]
        if telefone2:
            numero_para_tentar.append(telefone2)

        enviado = False
        for telefone in numero_para_tentar:
            if not telefone:
                continue

            if tentar_enviar(driver, telefone, mensagem, imagem):
                log_func(f"Mensagem enviada para {nome} ({telefone})")
                enviado = True
                break
            else:
                log_func(f"Falha ao enviar para {nome} no número {telefone}")

        if not enviado:
            salvar_contato_nao_enviado(nome, telefone1, telefone2)

        time.sleep(random.uniform(2, 4))


def salvar_contato_nao_enviado(nome, telefone1, telefone2):
    df = pd.DataFrame([{"Nome": nome, "Telefone1": telefone1, "Telefone2": telefone2}])
    
    caminho_falha = os.path.expanduser("~/Desktop/meus_projetos/whatsapp_disparador/nao_enviados.xlsx")

    if os.path.exists(caminho_falha):
        df_existente = pd.read_excel(caminho_falha)
        df_total = pd.concat([df_existente, df], ignore_index=True)
    else:
        df_total = df

    df_total.to_excel(caminho_falha, index=False)
