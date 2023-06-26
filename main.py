from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):
    PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?\d{3}\)?[\d\-\s]{7,10}$")

    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    @staticmethod
    def validate(phone):
        if not Phone.PHONE_REGEX.match(phone):
            raise ValueError(f"Phone number {phone} is invalid.")


class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add(self, phone):
        self.phones.append(phone)

    def remove(self, phone):
        self.phones.remove(phone)

    def clear_phones(self):
        self.phones.clear()


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        self.data.pop(name, None)


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (IndexError, ValueError):
            return "Помилка введення. Спробуйте ще раз."
        except KeyError:
            return "Контакту з таким ім'ям не знайдено."
    return inner


class Assistant:
    def __init__(self):
        self.address_book = AddressBook()

    @input_error
    def hello(self, command_args):
        return "Привіт! Я можу допомогти Вам з наступними командами: \n" + self.list_commands()

    @input_error
    def add(self, command_args):
        name = input("Введіть ім'я для записної книги: ")
        phone = input(f"Введіть мобільний номер телефону для контакта {name}: ")
        record = Record(Name(name))
        record.add(Phone(phone))
        self.address_book.add_record(record)
        return f"Запис з ім'ям {name} та номером телефону {phone} додано."

    @input_error
    def change(self, command_args):
        name = input("Введіть ім'я контакту, номер якого хочете змінити: ")
        phone = input(f"Введіть новий номер телефону для контакта {name}: ")
        record = self.address_book[name]
        record.clear_phones()
        record.add(Phone(phone))
        return f"Для контакту {name} номер телефону оновлено."

    @input_error
    def remove_phone(self, command_args):
        name = input("Введіть ім'я контакту, з якого хочете видалити номер телефону: ")
        phone = input(f"Введіть номер телефону, який хочете видалити з контакту {name}: ")
        record = self.address_book[name]
        record.remove(Phone(phone))
        return f"Номер телефону {phone} видалено з контакту {name}."

    @input_error
    def remove_record(self, command_args):
        name = input("Введіть ім'я контакту, який хочете видалити: ")
        self.address_book.remove_record(name)
        return f"Контакт {name} видалено."

    @input_error
    def phone(self, command_args):
        name = input("Введіть ім'я контакту, номери телефону якого хочете побачити: ")
        record = self.address_book[name]
        return ", ".join([phone.value for phone in record.phones])

    @input_error
    def show_all(self, command_args):
        return "\n".join([f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in self.address_book.data.items()])

    @input_error
    def exit(self, command_args):
        return "До побачення!"

    COMMANDS = {
        'hello': {'handler': hello, 'description': "Список доступних команд"},
        'add': {'handler': add, 'description': "Додати новий контакт. Формат вводу: 'add' -> потім введіть ім'я -> введіть номер"},
        'change': {'handler': change, 'description': "Змінити номер телефону вже існуючого контакту. Формат вводу: 'change' -> потім введіть ім'я -> введіть новий номер"},
        'remove_phone': {'handler': remove_phone, 'description': "Видалити номер телефону існуючого контакту. Формат вводу: 'remove_phone' -> потім введіть ім'я -> введіть номер, який хочете видалити"},
        'remove_record': {'handler': remove_record, 'description': "Видалити контакт. Формат вводу: 'remove_record' -> потім введіть ім'я контакту"},
        'phone': {'handler': phone, 'description': "Показати номери телефону контакту. Формат вводу: 'phone' -> потім введіть ім'я контакту"},
        'show_all': {'handler': show_all, 'description': "Показати всі контакти і їх номери телефону"},
        'exit': {'handler': exit, 'description': "Вийти з програми"}
    }

    def list_commands(self):
        return '\n'.join([f"{name}: {params['description']}" for name, params in self.COMMANDS.items()])

    def get_command_handler(self, command):
        command = command.lower().strip()
        command_handler = self.COMMANDS.get(command, {'handler': None})['handler']
        return command_handler

    def run(self):
        while True:
            command = input("Введіть команду: ")
            handler = self.get_command_handler(command)
            if handler is None:
                print("Неправильна команда")
            else:
                response = handler(self, '')
                print(response)
                if response == "До побачення!":
                    break


if __name__ == "__main__":
    assistant = Assistant()
    assistant.run()
