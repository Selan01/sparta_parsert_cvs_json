import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import json
import csv

url = 'https://whatmyuseragent.com/'

options = webdriver.ChromeOptions()

# web_driver ---> False

options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--headless')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version='116').install()), options=options)


#Вводишь назавания групп вк
name_group = [
        'Качалка',
        'Фитнесс центр',
        'Фитнесс клуб',
        'Тренажерный зал',
        'Спорт клуб',
        'Спортивный клуб']

repeat = 60
def search(name_group, repeat):
try:
    for name in name_group:
        count = 0
        link_dict = dict()
        start_heigh = 0
        last_heigh = 1080
        url = f'https://vk.com/groups?act=catalog&c%5Blike_hints%5D=1&c%5Bper_page%5D=40&c%5Bq%5D={name}&c%5Bsection%5D=communities&c%5Bsort%5D=6'
        driver.get(url=url)
        time.sleep(5)
        for _ in range(repeat):
            scroll = f"window.scrollTo({start_heigh}, {last_heigh} );"
            driver.execute_script(scroll)
            start_heigh += 1080
            last_heigh += 1080
            time.sleep(1)

        infos = driver.find_elements(By.CLASS_NAME, 'groups_row')

        for info in infos:
            link_element = info.find_element(By.CLASS_NAME, 'AvatarRich')
            link = link_element.get_attribute('href')
            link_dict[f'{name}_{count}'] = link
            count += 1
        with open(f'sparta/{name}.json', 'w', encoding='utf8') as f:
            json.dump(link_dict, f, indent=4, ensure_ascii=False)
        print(f'{name} --------> сделан')


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


# id_common = 1
#
# with open(f'sparta/info/sparta_all.csv', 'w', encoding='utf-8-sig', newline='') as file:
#     writer = csv.writer(file, delimiter=',')
#     writer.writerow(
#         (
#             'id',
#             'Название_группы',
#             'Ссылка_группы',
#             'Имя_контакта',
#             'Ссылка_контакта',
#             'Количество_участников',
#         )
#     )
#
# for name in name_group.keys():
#     id = 1
#     name_rep = name.replace(' ', '_')
#     with open(f'sparta/info/{name_rep}.csv', 'w', encoding='utf-8-sig', newline='') as f:
#         writer = csv.writer(f, delimiter=',')
#         writer.writerow(
#             (
#                 'id',
#                 'Название_группы',
#                 'Ссылка_группы',
#                 'Имя_контакта',
#                 'Ссылка_контакта',
#                 'Количество_участников',
#             )
#         )
#
#     with open(f'sparta/{name}.json', encoding='utf8') as f:
#         sparta = json.load(f)
#
#     iteration_count = len(sparta)
#     print(f'Всего итераций: {iteration_count}')
#
#     for vk_name, vk_link in sparta.items():
#         driver = webdriver.Chrome(service=ChromeService(executable_path='c:/sp/chromedriver/chromedriver'),
#                                   options=options)
#         driver.get(url=vk_link)
#         try:
#             # time.sleep(3)
#             people = driver.find_element(By.CLASS_NAME, 'redesigned-group-subscribers').text.strip()
#             people = people.split()
#             if 'K' in people[0]:
#                 people = people[0].replace('K', '000')
#             elif len(people) > 2:
#                 people = people[0] + people[1]
#             else:
#                 people = people[0]
#
#             name_info = driver.find_element(By.CLASS_NAME, 'people_name').text
#             link_info = driver.find_element(By.PARTIAL_LINK_TEXT, name_info).get_attribute('href')
#
#             group_name = driver.find_element(By.CLASS_NAME, 'page_name').text.strip()
#             iteration_count -= 1
#             print(f'Осталось {iteration_count} итераций')
#
#
#             with open(f'sparta/info/{name_rep}.csv', 'a', encoding='utf-8-sig', newline='') as f:
#                 writer = csv.writer(f, delimiter=',')
#                 writer.writerow(
#                     (
#                         id,
#                         group_name,
#                         vk_link,
#                         name_info,
#                         link_info,
#                         int(people),
#                     )
#                 )
#             id += 1
#             with open(f'sparta/info/sparta_all.csv', 'a', encoding='utf-8-sig', newline='') as file:
#                 writer = csv.writer(file, delimiter=',')
#                 writer.writerow(
#                     (
#                         id_common,
#                         group_name,
#                         vk_link,
#                         name_info,
#                         link_info,
#                         int(people),
#                     )
#                 )
#             id_common += 1
#
#         except NoSuchElementException:
#             iteration_count -= 1
#             print(f'Нет контактов. Итераций осталось {iteration_count}')
#
#         finally:
#             driver.close()
#             driver.quit()
#     print(f'{name} --------> сделан')


