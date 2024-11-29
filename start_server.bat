@echo off
REM Переходим в директорию проекта
cd /d C:\твоя директория

REM Активируем виртуальное окружение
call .venv\Scripts\activate

REM Запускаем скрипт
python main.py
