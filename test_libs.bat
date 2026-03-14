@echo off
REM Padronix - Teste de Bibliotecas Vendorizadas
REM Copyright (C) 2026 Melhym Pereira Quemel

echo ========================================
echo Padronix - Teste de Bibliotecas
echo ========================================
echo.

cd /d "%~dp0"

REM Testar imports
echo Testando python-docx...
python -c "from docx import Document; print('  python-docx: OK')"
if %errorlevel% neq 0 (
    echo  ERRO: python-docx nao carregou!
    exit /b 1
)

echo Testando lxml...
python -c "from lxml import etree; print('  lxml: OK')"
if %errorlevel% neq 0 (
    echo  ERRO: lxml nao carregou!
    exit /b 1
)

echo Testando arquitetura...
python -c "import struct; print(f'  Arquitetura: {struct.calcsize(\"P\") * 8}-bit')"

echo.
echo ========================================
echo Todos os testes passaram!
echo ========================================
echo.
echo As bibliotecas estao prontas para uso no NVDA.
echo.
pause
