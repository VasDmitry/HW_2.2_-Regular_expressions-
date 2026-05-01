from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)    
    
    # 1) Поместить Фамилию, Имя и Отчество человека 
    # в поля lastname, firstname и surname
    for row in contacts_list[1:]:
        namelist = ' '.join(row[0:3]).title().strip().split()
        namelist += [''] * (3 - len(namelist))
        row[0:3] = namelist

    # 2) Привести все телефоны в формат +7(999)999-99-99. 
    # Если есть добавочный номер, формат будет такой: 
    # +7(999)999-99-99 доб.9999.
        match = re.search(
        r'(?:\+7|8)?\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})(?:\D*(?:доб\.?)\D*(\d{1,4}))?',
            row[5],
            flags=re.I
        )
        if match:
            ext = f' доб.{match.group(5)}' if match.group(5) else ''
            row[5] = f'+7({match.group(1)}){match.group(2)}-{match.group(3)}-{match.group(4)}{ext}'   

    # 3) Объединить все дублирующиеся записи о человеке в одну.
    merged_contacts = {}  # словарь с ключами
    final_order = []  # список с правильным порядком записи в финальный список контактов
    for row in contacts_list[1:]:
        key = tuple(row[0:3])
        if key not in merged_contacts:
            merged_contacts[key] = row[:]
            final_order.append(key)
        else:
            for k in range(3, len(row)):
                if merged_contacts[key][k].strip() == "" and row[k].strip() != "":
                    merged_contacts[key][k] = row[k]
    contacts_list = [contacts_list[0]] + [merged_contacts[key] for key in final_order]
    
# Сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)
