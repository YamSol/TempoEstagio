@echo off
REM Criar ambiente virtual
python -m venv venv

REM Ativar ambiente virtual
call venv\Scripts\activate

REM Instalar dependências
pip install -r requirements.txt

REM Executar o programa principal
python src\unificado.py
