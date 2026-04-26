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
        namelist = ' '.join(row[0:3]).strip().split()
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
    delete_list = []
    for i, row_1 in enumerate(contacts_list[1:], 1):
        for j, row_2 in enumerate(contacts_list[(i+1):], i+1):
            lastname, firstname, surname = row_1[0:3]
            if j not in delete_list:
                if re.match(rf'{lastname} {firstname} ?({surname})?', ' '.join(row_2[0:3])):
                    delete_list.append(j)
                    for k, el in enumerate(row_1[4:], 4):
                        contacts_list[i][k] = row_2[k] if row_2[k].strip() != '' else row_1[k]      

    for index in delete_list[::-1]:
        del contacts_list[index]

# Сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)
