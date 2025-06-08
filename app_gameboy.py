# c:\Users\Felip\Desktop\pythonscript\app_gameboy.py
from app_core import run_scraper_instance

# URLs for Game Boy, GBA
SEARCH_URLS_GAMEBOY = [
    'https://www.olx.com.br/brasil?q=game%20boy&sf=1',
    'https://www.olx.com.br/brasil?q=gameboy&sf=1',
    'https://www.olx.com.br/brasil?q=nintendo%20game%20boy&sf=1',
    'https://www.olx.com.br/brasil?q=nintendo%20gameboy&sf=1',
    'https://www.olx.com.br/brasil?q=gba&sf=1'
]
SEEN_FILE_GAMEBOY = 'seen_gameboy.json' # Make sure you renamed your original seen.json
TITLE_KEYWORDS_GAMEBOY = ['game boy', 'gameboy', 'gba']

if __name__ == '__main__':
    run_scraper_instance(
        search_urls_list=SEARCH_URLS_GAMEBOY,
        seen_file_name=SEEN_FILE_GAMEBOY,
        title_filter_keywords=TITLE_KEYWORDS_GAMEBOY,
        search_type_name="Game Boy/GBA"
    )
