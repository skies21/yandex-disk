from typing import List
import aiohttp
import urllib.parse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET

YANDEX_API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={}'
YANDEX_API_FULL_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources?public_key=https://disk.yandex.ru/d/{}'
YANDEX_DOWNLOAD_API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}&path={}'
YANDEX_DOWNLOAD_API_FULL_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key=https://disk.yandex.ru/d/{}&path={}'


async def fetch_file_list(public_key: str):
    urls = [YANDEX_API_URL, YANDEX_API_FULL_URL]

    for base_url in urls:
        url = base_url.format(public_key)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
    return None


@require_GET
async def index(request):
    public_key = request.GET.get('public_key')
    files = []
    error = None

    if public_key:
        files_response = await fetch_file_list(public_key)
        if files_response:
            files = files_response.get('_embedded', {}).get('items', [])
        else:
            error = 'Не удалось получить файлы'

    return render(request, 'index.html', {'files': files, 'public_key': public_key, 'error': error})


async def download_file(request, file_path: str) -> HttpResponse:
    public_key = request.GET.get('public_key')

    encoded_file_path = urllib.parse.quote(file_path)

    urls: List[str] = [YANDEX_DOWNLOAD_API_URL, YANDEX_DOWNLOAD_API_FULL_URL]

    for url_template in urls:
        download_url = url_template.format(public_key, encoded_file_path)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(download_url) as response:
                    if response.status == 200:
                        download_info = await response.json()
                        file_url = download_info.get('href')

                        if file_url:
                            async with session.get(file_url) as file_response:
                                if file_response.status == 200:
                                    file_data = await file_response.read()
                                    file_name = urllib.parse.unquote(file_path)
                                    response = HttpResponse(file_data, content_type='application/octet-stream')
                                    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                                    return response
                                else:
                                    return HttpResponse(
                                        f'Ошибка при загрузке файла с URL: {file_url}. Код ответа: {file_response.status}',
                                        status=500)

            except aiohttp.ClientError as e:
                print(f'Ошибка клиента: {e}. Попробуем другой URL.')

    return HttpResponse('Не удалось скачать файл', status=500)
