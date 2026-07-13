@echo off
REM ============================================================
REM  PAN-TOGETHER - Serveur Pelican avec live-reload
REM  Double-cliquez sur ce fichier pour demarrer le site en local.
REM  Le navigateur se rafraichit automatiquement a chaque modif.
REM ============================================================

REM Se placer dans le dossier de ce fichier (racine du projet)
cd /d "%~dp0"

REM --- Chemin vers python.exe ---------------------------------
REM Par defaut : l'environnement virtuel du projet (cree par "uv sync").
REM Pour utiliser un autre Python, decommentez / adaptez la ligne suivante :

set "PYTHON=C:\pantogether\Python312\python.exe"
if not defined PYTHON set "PYTHON=.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
  echo [!] Python introuvable : %PYTHON%
  echo.
  echo     Lancez d'abord "uv sync" pour creer l'environnement,
  echo     ou definissez la variable PYTHON en haut de ce fichier.
  echo.
  pause
  exit /b 1
)

echo Demarrage du serveur : http://localhost:8000
echo (Ctrl+C pour arreter)
echo.

"%PYTHON%" -m invoke livereload

REM Garder la fenetre ouverte apres arret / en cas d'erreur
echo.
pause
