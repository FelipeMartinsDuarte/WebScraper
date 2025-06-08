# c:\Users\Felip\Desktop\pythonscript\app_nintendods.py
from app_core import run_scraper_instance

# URLs for Nintendo DS
SEARCH_URLS_NINTENDODS = [
    'https://www.olx.com.br/brasil?q=nintendo%20ds'
    # You can add price filters here if needed, e.g., &ps=100&pe=500
]
SEEN_FILE_NINTENDODS = 'seen_nintendods.json'
TITLE_KEYWORDS_NINTENDODS = ['nintendo ds', ' ds '] # ' ds ' helps catch "DS Lite", etc.

if __name__ == '__main__':
    run_scraper_instance(
        search_urls_list=SEARCH_URLS_NINTENDODS,
        seen_file_name=SEEN_FILE_NINTENDODS,
        title_filter_keywords=TITLE_KEYWORDS_NINTENDODS,
        search_type_name="Nintendo DS"
    )
