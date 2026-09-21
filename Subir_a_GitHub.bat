@echo off
title Subir Proyecto a GitHub - Untaldomi
color 0a
echo ============================================================
echo   SUBIENDO PROYECTO A TU GITHUB (Untaldomi)
echo ============================================================
echo.
cd /d "%~dp0"
git remote set-url origin https://github.com/Untaldomi/-llm-evaluation-toolkit.git
git branch -M main
echo Conectando con GitHub... Si te pide autorizar en el navegador, haz clic en "Authorize" o "Sign in".
echo.
git push -u origin main
echo.
echo ============================================================
echo   PROCESO TERMINADO. REVISA TU GITHUB:
echo   https://github.com/Untaldomi/-llm-evaluation-toolkit
echo ============================================================
echo.
pause
