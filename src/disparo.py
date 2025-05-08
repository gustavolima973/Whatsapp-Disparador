import json
import os
import re
import time
import random
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def carregar_config(caminho_config):
    with open(caminho_config, 'r', encoding='utf-8') as f:
        return json.load(f)


def iniciar_driver(config):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={config['chrome_user_data']}")
    chrome_options.add_argument(f"--profile-directory={config['chrome_profile']}")
    chrome_options.add_argument("--start-maximized")

    service = Service(config['chromedriver_path'])
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def formatar_numero(numero):
    numero = re.sub(r'\D', '', str(numero))
    if numero.startswith('55'):
        return numero
    elif len(numero) in [10, 11]:
        return '55' + numero
    return None


def enviar_midia(driver, caminho_arquivo):
    try:
        print(f"[INFO] Tentando enviar arquivo: {caminho_arquivo}")
      
        botao_mais = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus']"))
        )
        driver.execute_script("arguments[0].click();", botao_mais)
        time.sleep(1)

       
        botoes_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='button']"))
        )

       
        extensao = Path(caminho_arquivo).suffix.lower()
        if extensao in ['.jpg', '.jpeg', '.png', '.gif']:
            botoes_menu[1].click()
            tipo = "imagem"
        else:
            botoes_menu[0].click()
            tipo = "documento"

      
        upload = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )

        caminho_absoluto = os.path.abspath(os.path.expanduser(caminho_arquivo.strip()))
        if not os.path.exists(caminho_absoluto):
            print(f"[ERRO] Arquivo não encontrado: {caminho_absoluto}")
            return

        upload.send_keys(caminho_absoluto)
        print("[INFO] Arquivo enviado para o input.")

      
        botao_enviar = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        driver.execute_script("arguments[0].click();", botao_enviar)
        print(f"[SUCESSO] {tipo.capitalize()} enviado com sucesso!")

        time.sleep(5)

    except Exception as e:
        print(f"[ERRO] Falha ao enviar mídia: {e}")


def salvar_contato_nao_enviado(config, nome, telefone1, telefone2):
    df = pd.DataFrame([{"Nome": nome, "Telefone1": telefone1, "Telefone2": telefone2}])
    caminho_falha = os.path.abspath(os.path.expanduser(config['nao_enviados_path']))

    if os.path.exists(caminho_falha):
        df_existente = pd.read_excel(caminho_falha)
        df_total = pd.concat([df_existente, df], ignore_index=True)
    else:
        df_total = df

    df_total.to_excel(caminho_falha, index=False)


def enviar_mensagens(driver, config, log_func=print):
    campanha = pd.read_excel(config['excel_path'])

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

          
                caixa = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
                caixa.click()
                time.sleep(1)

         
                if mensagem and not pd.isna(mensagem):
                    for linha in mensagem.split('\n'):
                        caixa.send_keys(linha)
                        caixa.send_keys('\n')
                    time.sleep(2)
                elif imagem or pdf:
                    caixa.send_keys('\n')
                    time.sleep(1)

         
                if imagem and not pd.isna(imagem):
                    enviar_midia(driver, imagem)

     
                if pdf and not pd.isna(pdf):
                    enviar_midia(driver, pdf)

                log_func(f"[SUCESSO] Mensagem enviada para {nome} ({telefone})")
                enviado = True
                break

            except Exception as e:
                log_func(f"[ERRO] Falha com {nome} ({telefone}): {e}")
                time.sleep(5)

        if not enviado:
            salvar_contato_nao_enviado(config, nome, telefone1, telefone2)

        time.sleep(random.randint(config['delay_min'], config['delay_max']))


if __name__ == "__main__":
    config_path = os.path.abspath(os.path.expanduser("~/Desktop/meus_projetos/whatsapp_disparador/config.json"))
    config = carregar_config(config_path)

    driver = iniciar_driver(config)
    enviar_mensagens(driver, config)
    driver.quit()
