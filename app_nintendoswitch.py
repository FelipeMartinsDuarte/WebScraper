from app_core import run_scraper_instance

# URLs for Nintendo Switch, OLED, Lite
SEARCH_URLS_NINTENDOSWITCH = [
    'https://www.olx.com.br/brasil?q=nintendo%20switch',
    'https://www.olx.com.br/brasil?q=nintendo%20switch%20oled',
    'https://www.olx.com.br/games/consoles-de-video-game?q=nintendo%20switch%20lite'
    # Você pode adicionar filtros de preço aqui se necessário, ex: &ps=500&pe=2000
]
SEEN_FILE_NINTENDOSWITCH = 'seen_nintendoswitch.json'
# Palavras-chave para filtrar títulos. Incluí 'switch', 'oled' e 'lite'.
# O 'nintendo switch' já está nas URLs, mas manter aqui reforça o filtro.
TITLE_KEYWORDS_NINTENDOSWITCH = ['nintendo switch', 'switch', 'oled', 'lite']

if __name__ == '__main__':
    run_scraper_instance(
        search_urls_list=SEARCH_URLS_NINTENDOSWITCH,
        seen_file_name=SEEN_FILE_NINTENDOSWITCH,
        title_filter_keywords=TITLE_KEYWORDS_NINTENDOSWITCH,
        search_type_name="Nintendo Switch",
        max_notifications=10
    )