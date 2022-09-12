import requests
import os
import time
import json
from tqdm import tqdm


class VKDownloader:
    def __init__(self, token):
        self.token = token

    def get_photo(self, count=5):
        url = 'https://api.vk.com/method/photos.get'
        params = {'access_token': vktoken, 'v': '5.131', 'owner_id': vk_user_id, 'album_id': 'profile',
                  'extended': '1', 'photo_sizes': '1', 'count': count}
        result = requests.get(url, params=params).json()
        return result

    def get_all_photo(self):
        if not os.path.exists('vk_photo_backup'):
            os.mkdir('vk_photo_backup')  # создаём папку, если нету
        count = 5  # Кол-во получаемых записей
        load = self.get_photo(count)
        photos = []  # Полученные фото
        max_photo = {}  # Фото с максимальным разрешением

        print('Обработка данных:')
        for photo in tqdm(load['response']['items'], ncols=93, unit_scale=True): # Ходим по фоткам
            max_size = 0
            for size in photo['sizes']:  # Ищем максимальный размер
                if size['width'] > max_size:
                    max_size = size['width']
            info = {}
            if photo['likes']['count'] not in max_photo.keys():  # Проверяем лайки на совпадения
                max_photo[photo['likes']['count']] = size['url']
                info['file_name'] = f'{photo["likes"]["count"]}.jpg'  # И задаём имя либо так, если нету
            else:
                date = time.strftime('%d.%m.%Y', time.localtime(photo['date']))
                max_photo[f'{photo["likes"]["count"]}_{date}'] = size['url']
                info['file_name'] = f'{photo["likes"]["count"]}_{date}.jpg'  # либо сяк, если есть
            info['size'] = size['type']
            photos.append(info)  # Добавление в список в требуемом виде

        with open('vk_photo_backup.json', 'w') as file:
            json.dump(photos, file, indent=4, sort_keys=False)

        time.sleep(0.1)
        print('Скачивание фото:')
        for name, url in tqdm(max_photo.items(), ncols=100, unit_scale=True):
            with open(f'vk_photo_backup/{name}.jpg', 'wb') as file:
                image = requests.get(url)
                file.write(image.content)  # Сохраняем фото в папку
        return


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)}

    def _get_upload_link(self, path_to_ya: str):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': f'{path_to_ya}/{file_name}', 'overwrite': 'True'}
        response = requests.get(url=upload_url, headers=headers, params=params)
        return response.json()

    def create_folder(self, path_to_ya: str):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path_to_ya, 'overwrite': 'False'}
        requests.put(url=url, headers=headers, params=params)

    def upload_file(self, path_to_file):
        path_to_ya = 'vk_photo_backup'  # имя папки на ЯДиске
        self.create_folder(path_to_ya=path_to_ya)
        href = self._get_upload_link(path_to_ya=path_to_ya).get('href', '')
        requests.put(href, data=open(path_to_file, 'rb'))


if __name__ == '__main__':
    vk_user_id = input('Введите id пользователя ВК: ')
    ya_token = input('Введите токен ЯндексДиск: ')
    with open('vktoken.txt', 'r') as file:
        vktoken = file.readline().strip()

    downloader = VKDownloader(vktoken)
    downloader.get_all_photo()

    uploader = YaUploader(ya_token)
    folder_contents = os.listdir('vk_photo_backup')
    time.sleep(0.1)
    print('Загрузка фото на ЯндексДиск:')
    for file in tqdm(folder_contents, ncols=100, unit_scale=True):  # Ходим по файлам в папке и сохраняем на ЯДиск
        file_name = file
        file_path = './vk_photo_backup/' + file
        uploader.upload_file(path_to_file=file_path)
    print('Все операции успешно завершены')
    print(f'На ЯДиск загружено {len(folder_contents)} фото')
