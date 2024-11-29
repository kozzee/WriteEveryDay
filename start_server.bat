@echo off
REM Переходим в директорию проекта
cd /d C:\Python\BOT auto

REM Активируем виртуальное окружение
call .venv\Scripts\activate

REM Запускаем скрипт
python main.py
