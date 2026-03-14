@echo off
REM Padronix - Instalador de Dependências
REM Copyright (C) 2026 Melhym Pereira Quemel
REM Email: mpquemel@gmail.com

echo ========================================
echo Padronix - Instalador de Dependencias
echo ========================================
echo.

REM Detectar arquitetura do Python do NVDA
echo Detectando arquitetura do Python...
python -c "import struct; print('Arquitetura:', 8 * struct.calcsize('P'))"

REM Pasta de destino
set NVDA_PYTHON=C:\Program Files (x86)\NVDA\python
if exist "C:\Program Files\NVDA\python" set NVDA_PYTHON=C:\Program Files\NVDA\python

echo.
echo Instalando dependencias em: %NVDA_PYTHON%
echo.

REM Instalar python-docx
echo Instalando python-docx...
"%NVDA_PYTHON%\python.exe" -m pip install python-docx --upgrade

REM Instalar requests
echo Instalando requests...
"%NVDA_PYTHON%\python.exe" -m pip install requests --upgrade

REM Instalar winsound (já incluso no Windows, mas vamos garantir)
echo Verificando winsound...
"%NVDA_PYTHON%\python.exe" -c "import winsound; print('winsound OK')"

echo.
echo ========================================
echo Instalacao concluida!
echo ========================================
echo.
echo Agora voce pode empacotar o add-on com:
echo   python create_addon.py
echo.
pause
