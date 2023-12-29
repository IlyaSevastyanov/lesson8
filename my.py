
from csv import DictReader, DictWriter
from os.path import exists

class LenNumberError:
    def __init__(self,txt):
        self.txt = txt
def get_info():
    is_valid_name = False
    while not is_valid_name:
        try:
            first_name = str(input("Введите имя: "))
            if len(first_name) < 2:
                raise LenNumberError("Невалидная длина")
            else:
                is_valid_name = True
        except ValueError:
            print("Невалидное имя")
            continue
        except LenNumberError as err:
            print(err)
            continue
    is_valid_last_name = False
    while not is_valid_last_name:
        try:
            last_name = str(input("Введите фамилию: "))
            if len(last_name) < 2:
                raise LenNumberError("Невалидная длина")
            else:
                is_valid_last_name = True
        except ValueError:
            print("Невалидная фамилия")
            continue
        except LenNumberError as err:
            print(err)
            continue

    is_valid_number = False
    while not is_valid_number:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Невалидная длина")
            else:
                is_valid_number = True
        except ValueError:
            print("Невалидный номер")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]

def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)

def write_file(file_name):
    res = read_file(file_name)
    user_data = get_info()
    for el in res:
        if el['Телефон'] == str(user_data[2]):
            print('Такой пользователь уже существует')
            return
    obj = {'Имя': user_data[0], 'Фамилия': user_data[1], 'Телефон': user_data[2]}
    res.append(obj)
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)
def update_file(file_name, field_to_update, old_value, new_value):
    res = read_file(file_name)

    for el in res:
        if el[field_to_update] == old_value:
            el[field_to_update] = new_value

    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

def delete_file_entry(file_name, field_to_delete, value_to_delete):
    res = read_file(file_name)
    for el in res:
        if el[field_to_delete] == value_to_delete:
            el[field_to_delete] = "Удалено"

    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def copy_entry(source_file, destination_file, entry_number):
    source_data = read_file(source_file)

    if 1 <= entry_number <= len(source_data):
        entry_to_copy = source_data[entry_number - 1]

        if not exists(destination_file):
            create_file(destination_file)

        destination_data = read_file(destination_file)
        destination_data.append(entry_to_copy)

        with open(destination_file, 'w', encoding='utf-8', newline='') as dest_data:
            f_writer = DictWriter(dest_data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
            f_writer.writerows(destination_data)

        print(f"Запись из строки {entry_number} успешно скопирована в файл '{destination_file}'.")
        print(f"Содержимое файла '{destination_file}':")
        print(*read_file(destination_file))
    else:
        print("Некорректный номер строки для копирования.")


file_name = 'phone.csv'

def main():
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)

        elif command == 'r':
            read_file(file_name)
            if not exists(file_name):
                print("Файл не создан! Создайте файл)")
                continue
            print(*read_file(file_name))
        elif command == "c":
            field_to_update = input("Введите поле для изменения (Имя/Фамилия/Телефон): ")
            old_value = input("Введите текущее значение: ")
            new_value = input("Введите новое значение: ")
            update_file(file_name, field_to_update, old_value, new_value)

        elif command == "d":
            field_to_delete = input("Введите поле для удаления (Имя/Фамилия/Телефон): ")
            value_to_delete = input("Введите значение для удаления: ")
            delete_file_entry(file_name, field_to_delete, value_to_delete)
        elif command == "cp":
            entry_number = int(input("Введите номер строки для копирования: "))
            copy_entry(file_name, 'copied_phone.csv', entry_number)
        else:
            print("Некорректная команда")


main()
