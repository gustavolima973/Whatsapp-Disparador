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
from pathlib import Path


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
   
    numero = re.sub(r'\D', '', numero)
    if numero.startswith('55'):
        return numero
    elif len(numero) in [10, 11]:
        return '55' + numero
    return None


def enviar_midia(driver, caminho_arquivo):
    try:
        print(f"[INFO] Tentando enviar arquivo: {caminho_arquivo}")

        # Clica no botão "+"
        botao_mais = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus']"))
        )
        driver.execute_script("arguments[0].click();", botao_mais)
        time.sleep(1)

        # Encontra todos os botões do menu
        botoes_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='button']"))
        )

        # Determina o tipo pelo sufixo
        extensao = Path(caminho_arquivo).suffix.lower()
        if extensao in ['.jpg', '.jpeg', '.png', '.gif']:
            botoes_menu[1].click()  # Fotos e vídeos
            tipo = "imagem"
        else:
            botoes_menu[0].click()  # Documento
            tipo = "documento"

        # Input do arquivo
        upload = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )

        caminho_absoluto = os.path.abspath(os.path.expanduser(caminho_arquivo.strip()))
        if not os.path.exists(caminho_absoluto):
            print(f"[ERRO] Arquivo não encontrado: {caminho_absoluto}")
            return

        upload.send_keys(caminho_absoluto)
        print("[INFO] Arquivo enviado para o input.")

        # Clica no botão de enviar
        botao_enviar = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        driver.execute_script("arguments[0].click();", botao_enviar)
        print(f"[SUCESSO] {tipo.capitalize()} enviado com sucesso!")

        time.sleep(5)

    except Exception as e:
        print(f"[ERRO] Falha ao enviar mídia: {e}")


def salvar_contato_nao_enviado(nome, telefone1, telefone2):
    df = pd.DataFrame([{"Nome": nome, "Telefone1": telefone1, "Telefone2": telefone2}])
    caminho_falha = os.path.expanduser("~/Desktop/meus_projetos/whatsapp_disparador/nao_enviados.xlsx")

    if os.path.exists(caminho_falha):
        df_existente = pd.read_excel(caminho_falha)
        df_total = pd.concat([df_existente, df], ignore_index=True)
    else:
        df_total = df

    df_total.to_excel(caminho_falha, index=False)


def enviar_mensagens(driver, caminho_excel, log_func=print):
    campanha = pd.read_excel(caminho_excel)

    for _, row in campanha.iterrows():
        nome = row.get("Nome")
        telefone1 = str(row.get("Telefone1"))
        telefone2 = str(row.get("Telefone2")) if not pd.isna(row.get("Telefone2")) else None
        mensagem = row.get("Mensagem")
        imagem = row.get("Imagem", None)
        pdf = row.get("PDF", None)

        numeros = [telefone for telefone in [telefone1, telefone2] if telefone and not pd.isna(telefone)]
        enviado = False
        for telefone in numeros:
            try:
                numero_formatado = formatar_numero(telefone)
                if not numero_formatado:
                    continue

                link = f"https://web.whatsapp.com/send?phone={numero_formatado}&text&app_absent=0"
                driver.get(link)

                # Espera pela caixa de mensagem
                caixa = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                caixa.click()
                time.sleep(1)

                # Envia mensagem (se houver)
                if mensagem and not pd.isna(mensagem):
                    for linha in mensagem.split('\n'):
                        caixa.send_keys(linha)
                        caixa.send_keys('\n')
                    time.sleep(2)
                elif imagem or pdf:
                    caixa.send_keys('\n')
                    time.sleep(1)

                # Envia imagem (se houver)
                if imagem and not pd.isna(imagem):
                    enviar_midia(driver, imagem)

                # Envia PDF (se houver)
                if pdf and not pd.isna(pdf):
                    enviar_midia(driver, pdf)

                log_func(f"[SUCESSO] Mensagem enviada para {nome} ({telefone})")
                enviado = True
                break

            except Exception as e:
                log_func(f"[ERRO] Falha com {nome} ({telefone}): {e}")
                time.sleep(5)

        if not enviado:
            salvar_contato_nao_enviado(nome, telefone1, telefone2)

        time.sleep(random.randint(4, 7))
