import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

# Создаем класс приложения для управления данными о сотрудниках
class EmployeeManagementApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Employee Management App")  # Устанавливаем заголовок окна приложения

        # Устанавливаем соединение с базой данных SQLite
        self.conn = sqlite3.connect('employees.db')
        
        # Создаем таблицу 'employees' в базе данных (если она еще не существует)
        self.create_table()

        # Создаем виджет Treeview для отображения данных о сотрудниках
        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="Salary")
        self.tree.pack(padx=20, pady=20)  # Размещаем Treeview в окне приложения

        # Создаем виджеты и обновляем Treeview с данными о сотрудниках
        self.create_widgets()
        self.update_treeview()

    # Метод для создания таблицы 'employees' в базе данных
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary INTEGER
            )
        ''')
        self.conn.commit()  # Сохраняем изменения в базе данных

    def create_widgets(self):
        # Создаем виджеты (кнопки) для взаимодействия с данными о сотрудниках
        self.add_button = tk.Button(self.master,
                                    text="Add Employee",
                                    command=self.add_employee)
        self.add_button.pack(pady=10)
        self.update_button = tk.Button(self.master,
                                       text="Update Employee",
                                       command=self.update_employee)
        self.update_button.pack(pady=10)
        self.delete_button = tk.Button(self.master,
                                       text="Delete Employee",
                                       command=self.delete_employee)
        self.delete_button.pack(pady=10)
        self.search_button = tk.Button(self.master,
                                       text="Search Employee",
                                       command=self.search_employee)
        self.search_button.pack(pady=10)
        self.undo_button = tk.Button(self.master,
                                     text="Undo",
                                     command=self.undo_action)
        self.undo_button.pack(pady=10)

        # Привязываем событие "двойной щелчок" на виджете Treeview к методу on_double_click
        self.tree.bind("<Double-1>", self.on_double_click)

        self.update_treeview()

    def add_employee(self):
        name = simpledialog.askstring("Input", "Enter employee name:")
        phone = simpledialog.askstring("Input", "Enter employee phone:")
        email = simpledialog.askstring("Input", "Enter employee email:")
        salary = simpledialog.askinteger("Input", "Enter employee salary:")

    # Создаем курсор для работы с базой данных и выполняем SQL-запрос для вставки нового сотрудника
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
            (name, phone, email, salary))
        self.conn.commit()
        self.update_treeview()
        
    # Метод для обновления информации о сотруднике
    def update_employee(self):
        emp_id = simpledialog.askinteger("Input", "Enter employee ID:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id, ))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring("Input",
                                         "Enter updated employee name:",
                                         initialvalue=employee[1])
            phone = simpledialog.askstring("Input",
                                          "Enter updated employee phone:",
                                          initialvalue=employee[2])
            email = simpledialog.askstring("Input",
                                          "Enter updated employee email:",
                                          initialvalue=employee[3])
            salary = simpledialog.askinteger("Input",
                                             "Enter updated employee salary:",
                                             initialvalue=employee[4])

            cursor.execute(
                "UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?",
                (name, phone, email, salary, emp_id))
            self.conn.commit()
            self.update_treeview()
        else:
            messagebox.showerror("Error", "Employee not found.")

    # Метод для удаления информации о сотруднике

    def delete_employee(self):
        # Запрашиваем у пользователя идентификатор сотрудника, который должен быть удален
        emp_id = simpledialog.askinteger("Input", "Enter employee ID:")

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=?", (emp_id, ))
        self.conn.commit()
        self.update_treeview()

# Метод для поиска информации о сотруднике по имени
    def search_employee(self):
        # Запрашиваем у пользователя имя сотрудника, по которому нужно выполнить поиск
        name = simpledialog.askstring("Input", "Enter employee name:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE name=?", (name, ))
        employees = cursor.fetchall()

        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("Info", "No employee found with the given name.")

# Метод для обновления Treeview с данными о сотрудниках
    def update_treeview(self):
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        for employee in employees:
            self.tree.insert("", "end", values=employee)

# Метод, вызываемый при двойном щелчке на элементе Treeview
    def on_double_click(self, event):
        item = self.tree.selection()[0]
        employee_id = self.tree.item(item, "values")[0]  # Get the employee ID
        messagebox.showinfo("Employee ID", f"Employee ID: {employee_id}")

# Метод для действия "Отмена" (пока не реализовано)
    def undo_action(self):
        messagebox.showinfo("Undo", "Feature not implemented yet.")

# Метод, вызываемый при закрытии окна приложения
    def on_closing(self):
        self.conn.close()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()  # Создаем главное окно приложения
    app = EmployeeManagementApp(root)  # Создаем экземпляр класса EmployeeManagementApp, передавая главное окно
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Назначаем метод on_closing для обработки закрытия окна
    root.mainloop()  # Запускаем цикл обработки событий графического интерфейса (GUI)