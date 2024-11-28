@echo off
REM Переходим в директорию проекта
cd d CUsersUsernameDocumentsMyProject

REM Активируем виртуальное окружение
call venvScriptsactivate

REM Запускаем скрипт
python script.py