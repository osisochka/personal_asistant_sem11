import os
import json
import csv
import datetime
from typing import List, Optional

NOTES_FILE = 'notes.json'


def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data(file_path, default_data):
    if not os.path.exists(file_path):
        save_data(file_path, default_data)
        return default_data
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class Note:
    def __init__(self, note_id, title, content, timestamp):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp


class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        data = load_data(NOTES_FILE, [])
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.__dict__ for note in self.notes]
        save_data(NOTES_FILE, data)

    def add_note(self, title, content):
        note_id = max([note.note_id for note in self.notes], default=0) + 1
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        new_note = Note(note_id, title, content, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно добавлена")

    def list_notes(self):
        if not self.notes:
            print("Список заметок пуст")
            return
        for note in self.notes:
            print(f"{note.note_id}. {note.title} (дата: {note.timestamp})")

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None

    def view_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            print(f"Заголовок: {note.title}")
            print(f"Содержимое: {note.content}")
            print(f"Дата создания / изменения: {note.timestamp}")
        else:
            print("Заметка не найдена")

    def edit_note(self, note_id, new_title, new_content):
        note = self.get_note_by_id(note_id)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print('Заметка успешно изменена')
        else:
            print('Заметка не найдена')

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print('Заметка успешно удалена')
        else:
            print('Заметка не найдена')

    def export_notes_to_csv(self):
        if not self.notes:
            print("Список заметок пуст")
            return
        file_name = "notes_export.csv"
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['id', 'Заголовок', 'Содержимое', 'Дата']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow({
                    "id": note.note_id,
                    'Заголовок': note.title,
                    'Содержимое': note.content,
                    'Дата': note.timestamp
                })
            print(f"Заметки успешно экспортированы в файл {file_name}")

    def import_notes_to_csv(self):
        file_name = input('Введите имя CSV-файла: ')
        if not os.path.exists(file_name):
            print("Файл не найден")
            return
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                note_id = max([note.note_id for note in self.notes], default=0) + 1
                title = row.get('Заголовок', '')
                content = row.get('Содержимое', '')
                timestamp = row.get('Дата', datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                new_note = Note(note_id, title, content, timestamp)
                self.notes.append(new_note)
                self.save_notes()




def notes_menu():
    manager = NoteManager()
    while True:
        print("Управление заметками:")
        print("1. Добавить новую заметку")
        print("2. Посмотреть список заметок")
        print("3. Посмотреть заметку")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Экспорт заметок в CSV")
        print("7. Импорт заметок из CSV")
        print("8. Назад")
        choice = int(input("Введите номер действия: "))
        if choice == 1:
            title = input("Введите заголовок заметки: ")
            content = input("Введите содержимое заметки: ")
            manager.add_note(title, content)
        elif choice == 2:
            manager.list_notes()
        elif choice == 3:
            try:
                note_id = int(input("Введите ID заметки: "))
                manager.view_note(note_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == 4:
            try:
                note_id = int(input("Введите ID заметки: "))
                new_title = input("Введите заголовок заметки: ")
                new_content = input("Введите содержимое заметки: ")
                manager.edit_note(note_id, new_title, new_content)
            except ValueError:
                print("Некорректный ID")
        elif choice == 5:
            try:
                note_id = int(input("Введите ID заметки: "))
                manager.delete_note(note_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == 6:
            manager.export_notes_to_csv()
        elif choice == 7:
            manager.import_notes_to_csv()
        elif choice == 8:
            break
        else:
            print("Некорректный выбор")



class Task:
    def __init__(self, task_id, description, deadline, status):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.status = status


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        data = load_data('tasks.json', [])
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.__dict__ for task in self.tasks]
        save_data('tasks.json', data)

    def add_task(self, description, deadline):
        task_id = max([task.task_id for task in self.tasks], default=0) + 1
        new_task = Task(task_id, description, deadline, "Не выполнено")
        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача успешно добавлена")

    def list_tasks(self):
        if not self.tasks:
            print("Список задач пуст")
            return
        for task in self.tasks:
            print(f"{task.task_id}. {task.description} (Дедлайн: {task.deadline}, Статус: {task.status})")

    def mark_task_done(self, task_id):
        task = next((task for task in self.tasks if task.task_id == task_id), None)
        if task:
            task.status = "Выполнено"
            self.save_tasks()
            print("Задача отмечена как выполненная")
        else:
            print("Задача не найдена")

    def delete_task(self, task_id):
        task = next((task for task in self.tasks if task.task_id == task_id), None)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Задача удалена")
        else:
            print("Задача не найдена")


def tasks_menu():
    manager = TaskManager()
    while True:
        print("Управление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу выполненной")
        print("4. Удалить задачу")
        print("5. Назад")
        choice = int(input("Введите номер действия: "))
        if choice == 1:
            description = input("Введите описание задачи: ")
            deadline = input("Введите дедлайн (дд-мм-гггг): ")
            manager.add_task(description, deadline)
        elif choice == 2:
            manager.list_tasks()
        elif choice == 3:
            try:
                task_id = int(input("Введите ID задачи: "))
                manager.mark_task_done(task_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == 4:
            try:
                task_id = int(input("Введите ID задачи: "))
                manager.delete_task(task_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == 5:
            break
        else:
            print("Некорректный выбор")



class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email


class ContactManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        data = load_data('contacts.json', [])
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.__dict__ for contact in self.contacts]
        save_data('contacts.json', data)

    def add_contact(self, name, phone, email):
        contact_id = max([contact.contact_id for contact in self.contacts], default=0) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Контакт успешно добавлен")

    def list_contacts(self):
        if not self.contacts:
            print("Список контактов пуст")
            return
        for contact in self.contacts:
            print(f"{contact.contact_id}. {contact.name} (Телефон: {contact.phone}, Email: {contact.email})")

    def delete_contact(self, contact_id):
        contact = next((contact for contact in self.contacts if contact.contact_id == contact_id), None)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print("Контакт удален")
        else:
            print("Контакт не найден")


def contacts_menu():
    manager = ContactManager()
    while True:
        print("Управление контактами:")
        print("1. Добавить контакт")
        print("2. Просмотреть контакты")
        print("3. Удалить контакт")
        print("4. Назад")
        choice = int(input("Введите номер действия: "))
        if choice == 1:
            name = input("Введите имя контакта: ")
            phone = input("Введите телефон контакта: ")
            email = input("Введите email контакта: ")
            manager.add_contact(name, phone, email)
        elif choice == 2:
            manager.list_contacts()
        elif choice == 3:
            try:
                contact_id = int(input("Введите ID контакта: "))
                manager.delete_contact(contact_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == 4:
            break
        else:
            print("Некорректный выбор")



def calculator_menu():
    while True:
        print("Калькулятор:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("5. Назад")
        choice = int(input("Введите номер действия: "))
        if choice in (1, 2, 3, 4):
            try:
                a = float(input("Введите первое число: "))
                b = float(input("Введите второе число: "))
                if choice == 1:
                    print(f"Результат: {a + b}")
                elif choice == 2:
                    print(f"Результат: {a - b}")
                elif choice == 3:
                    print(f"Результат: {a * b}")
                elif choice == 4:
                    if b == 0:
                        print("Ошибка: деление на ноль")
                    else:
                        print(f"Результат: {a / b}")
            except ValueError:
                print("Некорректный ввод")
        elif choice == 5:
            break
        else:
            print("Некорректный выбор")


class FinanceRecord:
    def __init__(self, id: int, amount: float, category: str, date: str, description: str):
        self.id = id  # уникальный идентификатор записи
        self.amount = amount  # сумма операции (положительное число для доходов, отрицательное для расходов)
        self.category = category  # категория операции (например, «Еда», «Транспорт», «Зарплата»)
        self.date = date  # дата операции в формате ДД-ММ-ГГГГ
        self.description = description  # описание операции


class FinanceManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.records = self.load_from_json()

    def add_finance_record(self, amount: float, category: str, date: str, description: str):
        new_id = len(self.records) + 1  # Генерация нового уникального идентификатора
        record = FinanceRecord(new_id, amount, category, date, description)
        self.records.append(record)
        self.save_to_json()

    def view_finance_records(self, filter_by: Optional[str] = None) -> List[FinanceRecord]:
        if filter_by:
            return [record for record in self.records if record.category == filter_by or record.date == filter_by]
        return self.records

    def generate_report(self, start_date: str, end_date: str) -> List[FinanceRecord]:
        return [record for record in self.records if start_date <= record.date <= end_date]

    def export_to_csv(self, filename: str):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Description'])
            for record in self.records:
                writer.writerow([record.id, record.amount, record.category, record.date, record.description])

    def import_from_csv(self, filename: str):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Пропустить заголовок
            for row in reader:
                id = int(row[0])
                amount = float(row[1])
                category = row[2]
                date = row[3]
                description = row[4]
                self.records.append(FinanceRecord(id, amount, category, date, description))
            self.save_to_json()

    def calculate_balance(self) -> float:
        return sum(record.amount for record in self.records)

    def group_by_category(self) -> dict:
        categories = {}
        for record in self.records:
            if record.category not in categories:
                categories[record.category] = 0
            categories[record.category] += record.amount
        return categories

    def save_to_json(self):
        with open(self.filename, 'w') as file:
            json.dump([record.__dict__ for record in self.records], file)

    def load_from_json(self) -> List[FinanceRecord]:
        try:
            with open(self.filename, 'r') as file:
                records_data = json.load(file)
                return [FinanceRecord(**data) for data in records_data]
        except FileNotFoundError:
            return []


def finance_menu():
    manager = FinanceManager('finance.json')
    while True:
        print("\nУправление финансовыми записями:")
        print("1. Добавить запись")
        print("2. Просмотреть записи")
        print("3. Сгенерировать отчёт")
        print("4. Экспорт в CSV")
        print("5. Импорт из CSV")
        print("6. Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == '1':
            amount = float(input("Введите сумму (положительное число для доходов и отрицательное для расходов): "))
            category = input("Введите категорию операции: ")
            date = input("Введите дату (ДД-ММ-ГГГГ): ")
            description = input("Введите описание операции: ")
            manager.add_finance_record(amount, category, date, description)
            print("Запись добавлена.")

        elif choice == '2':
            filter_choice = input(
                "Фильтровать по дате или категории? (введите дату или категорию или оставьте пустым для просмотра всех): ")
            records = manager.view_finance_records(filter_choice)
            for record in records:
                print(
                    f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")

        elif choice == '3':
            start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
            end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
            report = manager.generate_report(start_date, end_date)
            for record in report:
                print(
                    f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")

        elif choice == '4':
            filename = input("Введите имя файла для экспорта (например finance.csv): ")
            manager.export_to_csv(filename)
            print(f"Записи экспортированы в {filename}.")

        elif choice == '5':
            filename = input("Введите имя файла для импорта (например finance.csv): ")
            manager.import_from_csv(filename)
            print(f"Записи импортированы из {filename}.")

        elif choice == '6':
            break




def main_menu():
    while True:
        print("Добро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")
        choice = int(input("Введите номер действия: "))
        if choice == 1:
            notes_menu()
        elif choice == 2:
            tasks_menu()
        elif choice == 3:
            contacts_menu()
        elif choice == 4:
            finance_menu()
        elif choice == 5:
            calculator_menu()
        elif choice == 6:
            print("До свидания")
            break
        else:
            print('Некорректный ввод\n')



if __name__ == '__main__':
    main_menu()






