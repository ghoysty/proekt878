import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

DATA_FILE = 'training_data.json'

# Загрузка данных из файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Сохранение данных
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(training_list, f, ensure_ascii=False, indent=4)

# Валидация даты
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Валидация длительности
def validate_duration(duration_text):
    try:
        duration = float(duration_text)
        return duration > 0
    except ValueError:
        return False

# Добавление записи
def add_training():
    date = entry_date.get().strip()
    type_training = entry_type.get().strip()
    duration = entry_duration.get().strip()

    if not validate_date(date):
        messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ГГГГ-ММ-ДД")
        return
    if not validate_duration(duration):
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
        return

    training = {
        'date': date,
        'type': type_training,
        'duration': float(duration)
    }
    training_list.append(training)
    refresh_table()
    clear_entries()

# Очистка полей
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_duration.delete(0, tk.END)

# Обновление таблицы
def refresh_table(filtered_list=None):
    for row in tree.get_children():
        tree.delete(row)
    data = filtered_list if filtered_list is not None else training_list
    for item in data:
        tree.insert('', tk.END, values=(item['date'], item['type'], item['duration']))

# Загрузка данных при запуске
training_list = load_data()

# Создаем окно
root = tk.Tk()
root.title("Training Planner")

# Поля ввода
tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Тип тренировки").grid(row=1, column=0, padx=5, pady=5)
entry_type = tk.Entry(root)
entry_type.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Длительность (мин)").grid(row=2, column=0, padx=5, pady=5)
entry_duration = tk.Entry(root)
entry_duration.grid(row=2, column=1, padx=5, pady=5)

# Кнопка добавить
btn_add = tk.Button(root, text="Добавить тренировку", command=add_training)
btn_add.grid(row=3, column=0, columnspan=2, pady=10)

# Таблица с тренировками
columns = ('date', 'type', 'duration')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Фильтр
filter_frame = tk.Frame(root)
filter_frame.grid(row=5, column=0, columnspan=2, pady=10)

tk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, padx=5)
entry_filter_type = tk.Entry(filter_frame)
entry_filter_type.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=2, padx=5)
entry_filter_date = tk.Entry(filter_frame)
entry_filter_date.grid(row=0, column=3, padx=5)

def apply_filter():
    type_filter = entry_filter_type.get().strip().lower()
    date_filter = entry_filter_date.get().strip()
    filtered = training_list

    if type_filter:
        filtered = [t for t in filtered if t['type'].lower() == type_filter]
    if date_filter:
        if validate_date(date_filter):
            filtered = [t for t in filtered if t['date'] == date_filter]
        else:
            messagebox.showerror("Ошибка", "Некорректный формат даты фильтра")
            return
    refresh_table(filtered)

btn_filter = tk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=5)

# После закрытия, сохранить данные
def on_closing():
    save_data()
    root.destroy()

# Инициализация таблицы данными
refresh_table()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
