# c:\Users\Felip\Desktop\pythonscript\app_pokemon.py
from app_core import run_scraper_instance

# URLs for Pokemon Cartridges/Tapes
SEARCH_URLS_POKEMON = [
    'https://www.olx.com.br/brasil?q=cartucho%20pokemon',
    'https://www.olx.com.br/brasil?q=fita%20pokemon',
    'https://www.olx.com.br/brasil?q=jogos%20pokemon'
    # 'fitas pokemon' is likely covered by 'fita pokemon' and the title filter
]
SEEN_FILE_POKEMON = 'seen_pokemon.json'
TITLE_KEYWORDS_POKEMON = ['pokemon'] # Keep it simple, search URL is specific

if __name__ == '__main__':
    run_scraper_instance(
        search_urls_list=SEARCH_URLS_POKEMON,
        seen_file_name=SEEN_FILE_POKEMON,
        title_filter_keywords=TITLE_KEYWORDS_POKEMON,
        search_type_name="Pokemon Cartuchos/Fitas"
    )
