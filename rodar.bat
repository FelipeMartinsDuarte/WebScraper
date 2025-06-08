@echo off
REM Define o diretório do script
set SCRIPT_DIR=C:\Users\Felip\Desktop\pythonscript

REM Define o script principal a ser executado
set MAIN_SCRIPT=run_all_scrapers.py

echo [%date% %time%] Iniciando o scraper agendado: %MAIN_SCRIPT%
cd /d %SCRIPT_DIR%
python %MAIN_SCRIPT%
echo [%date% %time%] Execucao do scraper agendado concluida.

REM O script .bat termina aqui. O Agendador de Tarefas cuidara da repeticao.
