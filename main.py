from tqdm import tqdm
import os

from modules.application import Application

def get_medicines_list():
    target_file = os.path.join(os.path.abspath(os.getcwd()), 'список наименований для поиска.txt')
    with open(target_file, 'r', encoding='utf-8') as file:
        medicines_list = file.readlines()
    return [medicine.replace('\n', '') for medicine in medicines_list]

if __name__ == "__main__":
    medicines_list = get_medicines_list()
    print(f'Загружен список лекарств - {medicines_list}')
    downloaded_files_amount = 0
    for medicine in tqdm(medicines_list):
        print(f'\nВыполняем поиск лекарства: {medicine}...')
        row_in_process = 0
        app = Application()
        app.start()
        medicine_rows = app.navigation.find_rows_for_given_label(medicine)
        if not medicine_rows:
            continue
        medicine_ids = [app.navigation.extract_guid(row) for row in medicine_rows]
        print(f'Успешно извлечено {len(medicine_ids)} позиций для лекарства {medicine}.')
        attempts_number, was_app_restarted = 0, False
        while row_in_process < len(medicine_ids):
            current_id = medicine_ids[row_in_process]
            print(f'Начинаем загрузку PDF файла c ID - {current_id}...')
            try:
                app.navigation.download_instruction(current_id)
                downloaded_files_amount += 1
                row_in_process += 1
                attempts_number, was_app_restarted = 0, False
            except Exception as ex:
                print(f'Ошибка при обработке очередной строки: {ex}')
                if attempts_number < 3:
                    attempts_number += 1
                    continue
                else:
                    if not was_app_restarted:
                        print('Выполняем рестарт браузера...')
                        was_app_restarted = True
                        app = Application.restart_app(app)
                    else:
                        print("Рестарт браузера не устранил ошибку. Переходим к следующему файлу...")
                        row_in_process += 1
        print(f'PDF файлы по лекарственному средству {medicine} успешно загружены.\n')
        app.destroy()
    print(f'Процесс загрузки PDF файлов завершен. Загружено файлов: {downloaded_files_amount}')
