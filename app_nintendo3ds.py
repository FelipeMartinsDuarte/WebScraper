# c:\Users\Felip\Desktop\pythonscript\app_nintendo3ds.py
from app_core import run_scraper_instance

# URLs for Nintendo 3DS
SEARCH_URLS_NINTENDO3DS = [
    'https://www.olx.com.br/brasil?q=nintendo%203ds'
]
SEEN_FILE_NINTENDO3DS = 'seen_nintendo3ds.json'
TITLE_KEYWORDS_NINTENDO3DS = ['nintendo 3ds', '3ds']

if __name__ == '__main__':
    run_scraper_instance(
        search_urls_list=SEARCH_URLS_NINTENDO3DS,
        seen_file_name=SEEN_FILE_NINTENDO3DS,
        title_filter_keywords=TITLE_KEYWORDS_NINTENDO3DS,
        search_type_name="Nintendo 3DS"
    )
