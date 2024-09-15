# Yandex Disk File Viewer

Этот проект представляет собой веб-приложение на Django, которое позволяет просматривать и загружать файлы из публичных ссылок на Яндекс.Диск. Приложение использует API Яндекс.Диск для получения списка файлов и их скачивания.

## Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/skies21/yandex-disk.git
   cd yandex_disk
   
2. Создайте виртуальное окружение и активируйте его:
    ```
    python -m venv venv
    Linux: source venv/bin/activate 
    Windows: venv\Scripts\activate
    ```
3. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
4. Запуск:
    ```
    python manage.py runserver
    ```
5. Откройте браузер и перейдите по адресу:
    ```
   http://127.0.0.1:8000/
   ```
## Функциональность

Форма ввода публичной ссылки: Введите публичную ссылку на Яндекс.Диск для просмотра списка файлов.
Список файлов: Отображает файлы из предоставленной ссылки с возможностью их загрузки.
Загрузка файлов: Нажмите кнопку "Скачать" для загрузки файла.

## Структура проекта

- index.html: Главная страница с формой ввода и списком файлов.
- views.py: Содержит представления для обработки запросов и взаимодействия с API Яндекс.Диск.
- urls.py: Настройки маршрутизации URL.
- requirements.txt: Список зависимостей проекта.

## Требования

- Python 3.x
- Django
- aiohttp
- bootstrap (для стилизации)