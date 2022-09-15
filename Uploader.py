import requests


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)}

    def _get_upload_link(self, path_to_ya: str, file_name=None):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': f'{path_to_ya}/{file_name}', 'overwrite': 'True'}
        response = requests.get(url=upload_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def create_folder(self, path_to_ya: str):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path_to_ya, 'overwrite': 'False'}
        response = requests.put(url=url, headers=headers, params=params)
        status_code = response.status_code
        if status_code == 201:
            print('Папка на ЯндексДиске успешно создана')
        elif status_code == 409:
            print('Папка на ЯндексДиске уже существует')
        else:
            print(f'Ошибка создания папки № {status_code}')
            response.raise_for_status()

    def upload_file(self, path_to_file, path_to_ya, file_name):
        # path_to_ya = 'vk_photo_backup'  # имя папки на ЯДиске
        href = self._get_upload_link(path_to_ya=path_to_ya, file_name=file_name).get('href', '')
        response = requests.put(href, data=open(path_to_file, 'rb'))
        response.raise_for_status()
