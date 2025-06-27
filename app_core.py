# c:\Users\Felip\Desktop\pythonscript\app_core.py
import json
import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import undetected_chromedriver as uc # Importa a biblioteca undetected-chromedriver

# Load environment variables from .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Constants for managing seen items
SEEN_LIMIT = 400
SEEN_KEEP = 200

def load_seen_data(seen_file_path):
    """Loads seen items from a JSON file."""
    if os.path.exists(seen_file_path):
        try:
            with open(seen_file_path, 'r', encoding='utf-8') as f:
                return list(json.load(f))
        except json.JSONDecodeError:
            print(f"Erro ao decodificar {seen_file_path}. Retornando lista vazia.")
            return []
    return []

def save_seen_data(seen_list, seen_file_path):
    """Saves seen items to a JSON file, trimming if necessary."""
    if len(seen_list) > SEEN_LIMIT:
        seen_list = seen_list[-SEEN_KEEP:]
    with open(seen_file_path, 'w', encoding='utf-8') as f:
        json.dump(seen_list, f, ensure_ascii=False, indent=2)
    return seen_list

def send_telegram_message(msg):
    """Sends a message via Telegram."""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("ERRO: TELEGRAM_TOKEN ou CHAT_ID não configurados. Verifique seu arquivo .env.")
        return

    api_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': msg,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    try:
        r = requests.post(api_url, data=payload, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

def scrape_olx_ads(search_url, title_keywords_list):
    """Scrapes OLX ads from a given URL, filtering by title keywords."""
    chrome_options = Options()
    # Configure o modo headless aqui: True para rodar em segundo plano, False para ver o navegador
    run_headless = True # Defina como False para depuração visual

    args = [
        '--lang=pt-BR', 
        '--window-size=1920,1080', 
        '--incognito',
        '--disable-gpu',  # Often necessary for headless, prevents GPU crashes
        '--disable-software-rasterizer', # Can also help with stability
        '--no-sandbox', # Use with caution, can be necessary in some environments
        '--disable-dev-shm-usage', # Overcomes limited resource problems
        '--ignore-certificate-errors', # For SSL handshake issues (use as a workaround)
        '--allow-running-insecure-content' # For SSL handshake issues (use as a workaround)
    ]
    if run_headless:
        args.append('--headless')

    # Adicionar um User-Agent comum
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    # Tentar mascarar automação
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    for a in args:
        chrome_options.add_argument(a)
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = None
    itens = []
    coletados = set()

    # Definir seletores como constantes
    AD_LINK_SELECTOR = 'a.olx-adcard__link'
    AD_TITLE_SELECTOR = 'h2' # Relativo ao AD_LINK_SELECTOR
    AD_PRICE_SELECTOR = 'h3.olx-adcard__price' # Relativo ao container do anúncio

    try:
        # undetected_chromedriver gerencia o download e o caminho do driver automaticamente.
        print("  Iniciando undetected_chromedriver...")
        driver = uc.Chrome(
            options=chrome_options
        )

        # Define um tempo máximo de 45 segundos para o carregamento de uma página.
        # Se a página não carregar neste tempo, uma TimeoutException será lançada.
        driver.set_page_load_timeout(45)
        print(f"  WebDriver iniciado com sucesso.")
        print(f"  Acessando URL: {search_url}")
        driver.get(search_url)
        # time.sleep(5)  # Opcional: A WebDriverWait abaixo já lida com a espera pelos elementos (comentado)

        # Esperar explicitamente por pelo menos um elemento de anúncio
        wait_timeout = 30 # Tempo máximo de espera em segundos
        try:
            WebDriverWait(driver, wait_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, AD_LINK_SELECTOR))
            )
            # Se a espera for bem-sucedida, agora podemos encontrar todos os elementos
            ad_elements = driver.find_elements(By.CSS_SELECTOR, AD_LINK_SELECTOR)
        except TimeoutException:
            print(f"    Timeout ({wait_timeout}s) esperando pelos elementos de anúncio com o seletor '{AD_LINK_SELECTOR}' em {search_url}. Nenhum anúncio encontrado.")
            return [] # Retorna lista vazia se não encontrar elementos dentro do tempo limite

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for lazy-loaded content

        for ad_element in ad_elements:
            try:
                titulo_element = ad_element.find_element(By.CSS_SELECTOR, AD_TITLE_SELECTOR)
                titulo = titulo_element.text.strip()
                titulo_lower = titulo.lower()

                if not any(keyword in titulo_lower for keyword in title_keywords_list):
                    continue

                link = ad_element.get_attribute('href') # type: ignore # Ignorar aviso de tipo se necessário
                if not link:
                    continue

                container = ad_element.find_element(By.XPATH, './../..')

                preco = "Preço não disponível" 
                preco_float = 0.0 

                preco_elements = container.find_elements(By.CSS_SELECTOR, AD_PRICE_SELECTOR) 

                if preco_elements:
                    preco_element = preco_elements[0] 
                    preco = preco_element.text.strip()
                    preco_limpo = preco.replace('R$', '').replace('.', '').replace(',', '.').strip()
                    try:
                        preco_float = float(preco_limpo)
                    except ValueError:
                        preco_float = 0.0

                chave = (titulo, preco_float)
                if chave not in coletados:
                    coletados.add(chave)
                    itens.append((titulo, preco, link))
            except Exception as e_inner: 
                print(f"    Erro inesperado processando um anúncio individual: {e_inner}. Título: {titulo if 'titulo' in locals() else 'N/A'}") 
                continue
    except Exception as e_outer: 
        print(f"  Erro geral no scraping de {search_url}: {e_outer}")
    finally:
        if driver:
            driver.quit()
    print(f"  Scraping de {search_url} concluído. Itens coletados: {len(itens)}") # DEBUG
    return itens

def run_scraper_instance(search_urls_list, seen_file_name, title_filter_keywords, search_type_name, max_notifications=None):
    """Main function to run a scraper instance for a specific search type."""
    try:
        print(f"\n--- Iniciando scraper para: {search_type_name} ---")
        print(f"  Usando SEEN_FILE: {seen_file_name}")
        print(f"  Palavras-chave para filtro de título: {title_filter_keywords}")

        seen_links = load_seen_data(seen_file_name)
        seen_links_set = set(seen_links)
        new_ads_found = []

        for s_url in search_urls_list:
            scraped_items = scrape_olx_ads(s_url, title_filter_keywords)
            for titulo, preco, link in scraped_items:
                if link not in seen_links_set:
                    seen_links.append(link)
                    seen_links_set.add(link)
                    new_ads_found.append((titulo, preco, link))

        if new_ads_found:

            print(f"  Encontrados {len(new_ads_found)} novos anúncios para {search_type_name}.")

            sorted_new_ads = sorted(new_ads_found, key=lambda item: float(str(item[1]).replace('R$', '').replace('.', '').replace(',', '.').strip() if str(item[1]).replace('R$', '').replace('.', '').replace(',', '.').strip().replace('.','',1).isdigit() else '0'))

            # Aplicar o limite máximo de notificações, se especificado
            if max_notifications is not None and max_notifications > 0:
                sorted_new_ads = sorted_new_ads[:max_notifications]

                
            print(f"  Enviando {len(sorted_new_ads)} novas notificações para {search_type_name} (ordenado por preço)...")
            for titulo, preco, link in sorted_new_ads:
                
                now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                msg = (
                    f"🚨 *Nova Oferta ({search_type_name}) Detectada!*\n"
                    f"📅 *Data:* {now.split()[0]}   🕑 *Hora:* {now.split()[1]}\n\n"
                    f"*{titulo}*\n"
                    f"{preco}\n"
                    f"{link}"
                )
                send_telegram_message(msg)
                time.sleep(0.5)  
            save_seen_data(seen_links, seen_file_name)
            print(f"  Notificações enviadas e {seen_file_name} atualizado.")
        else:
            print(f"  Nenhum anúncio novo encontrado para {search_type_name}.")

        print(f"  Total de anúncios novos para {search_type_name}: {len(new_ads_found)}")
    except Exception as e:
        print(f"  ERRO INESPERADO durante o scraping para '{search_type_name}': {e}")
        # Você pode adicionar mais logging aqui se necessário, como traceback.format_exc()
    finally:
        print(f"--- Scraper para {search_type_name} concluído (ou falhou) ---")
