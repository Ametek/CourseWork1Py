import os
import time
from tqdm import tqdm
import Downloader
import Uploader


if __name__ == '__main__':
    # vk_user_id = input('Введите id пользователя ВК: ')
    vk_user_id = 57629630
    ya_token = input('Введите токен ЯндексДиск: ')
    with open('vktoken.txt', 'r') as file:
        vktoken = file.readline().strip()

    downloader = Downloader.VKDownloader(vktoken)
    downloader.get_all_photo(vk_user_id)

    uploader = Uploader.YaUploader(ya_token)
    path_to_ya = 'vk_photo_backup'
    uploader.create_folder(path_to_ya=path_to_ya)
    folder_contents = os.listdir('vk_photo_backup')
    time.sleep(0.1)
    print('Загрузка фото на ЯндексДиск:')
    for file in tqdm(folder_contents, ncols=100, unit_scale=True):  # Ходим по файлам в папке и сохраняем на ЯДиск
        file_name = file
        file_path = './vk_photo_backup/' + file
        uploader.upload_file(path_to_file=file_path, path_to_ya=path_to_ya, file_name=file_name)
    print('Все операции успешно завершены')
    print(f'На ЯДиск загружено {len(folder_contents)} фото')
