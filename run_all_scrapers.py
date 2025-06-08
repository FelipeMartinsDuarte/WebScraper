# run_all_scrapers.py
import time
# Import the functions or main variables from your specific scraper files
from app_gameboy import SEARCH_URLS_GAMEBOY, SEEN_FILE_GAMEBOY, TITLE_KEYWORDS_GAMEBOY
from app_nintendods import SEARCH_URLS_NINTENDODS, SEEN_FILE_NINTENDODS, TITLE_KEYWORDS_NINTENDODS
from app_nintendo3ds import SEARCH_URLS_NINTENDO3DS, SEEN_FILE_NINTENDO3DS, TITLE_KEYWORDS_NINTENDO3DS
from app_pokemon import SEARCH_URLS_POKEMON, SEEN_FILE_POKEMON, TITLE_KEYWORDS_POKEMON
from app_nintendoswitch import SEARCH_URLS_NINTENDOSWITCH, SEEN_FILE_NINTENDOSWITCH, TITLE_KEYWORDS_NINTENDOSWITCH

# Import the core function that does the work
from app_core import run_scraper_instance

if __name__ == '__main__':
    # Tempo de espera entre cada ciclo completo de scraping (15 minutos)
    delay_between_cycles_seconds = 15 * 60
    # Define um pequeno delay entre cada scraper individual dentro de um ciclo, se desejado
    delay_between_individual_scrapers = 5  # segundos

    while True:
        print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} --- Iniciando novo ciclo de scraping ---")

        # --- Game Boy / GBA ---
        run_scraper_instance(
            search_urls_list=SEARCH_URLS_GAMEBOY,
            seen_file_name=SEEN_FILE_GAMEBOY,
            title_filter_keywords=TITLE_KEYWORDS_GAMEBOY,
            search_type_name="Game Boy/GBA"
        )
        time.sleep(delay_between_individual_scrapers)

        # --- Nintendo DS ---
        run_scraper_instance(
            search_urls_list=SEARCH_URLS_NINTENDODS,
            seen_file_name=SEEN_FILE_NINTENDODS,
            title_filter_keywords=TITLE_KEYWORDS_NINTENDODS,
            search_type_name="Nintendo DS"
        )
        time.sleep(delay_between_individual_scrapers)

        # --- Nintendo 3DS ---
        run_scraper_instance(
            search_urls_list=SEARCH_URLS_NINTENDO3DS,
            seen_file_name=SEEN_FILE_NINTENDO3DS,
            title_filter_keywords=TITLE_KEYWORDS_NINTENDO3DS,
            search_type_name="Nintendo 3DS"
        )
        time.sleep(delay_between_individual_scrapers)

        # --- Pokemon ---
        run_scraper_instance(
            search_urls_list=SEARCH_URLS_POKEMON,
            seen_file_name=SEEN_FILE_POKEMON,
            title_filter_keywords=TITLE_KEYWORDS_POKEMON,
            search_type_name="Pokemon Cartuchos/Fitas"
        )
        time.sleep(delay_between_individual_scrapers)

        # --- Nintendo Switch ---
        run_scraper_instance(
            search_urls_list=SEARCH_URLS_NINTENDOSWITCH,
            seen_file_name=SEEN_FILE_NINTENDOSWITCH,
            title_filter_keywords=TITLE_KEYWORDS_NINTENDOSWITCH,
            search_type_name="Nintendo Switch",
            max_notifications=10
        )

        print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} --- Ciclo de scraping concluído. Aguardando {delay_between_cycles_seconds / 60:.0f} minutos... ---")
        time.sleep(delay_between_cycles_seconds)
