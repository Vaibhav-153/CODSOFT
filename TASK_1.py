import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Task:
    def __init__(self, description, priority="Normal", due_date=None):
        self.description = description
        self.completed = False
        self.priority = priority
        self.due_date = due_date

    def __str__(self):
        status = "✓" if self.completed else "✗"
        due_date_str = f"[Due: {self.due_date}]" if self.due_date else "[Due: -]"
        return f"{status} {self.description} (Priority: {self.priority}, {due_date_str})"

    def to_dict(self):
        return {
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['description'], data['priority'], data['due_date'])
        task.completed = data['completed']
        return task

class ToDoList:
    def __init__(self, filename='todo_list.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, description, priority="Normal", due_date=None):
        task = Task(description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def update_task(self, index, description, priority="Normal", due_date=None):
        if 0 <= index < len(self.tasks):
            self.tasks[index].description = description
            self.tasks[index].priority = priority
            self.tasks[index].due_date = due_date
            self.save_tasks()
            return self.tasks[index]
        else:
            return None

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()
            return self.tasks[index]
        else:
            return None

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            deleted_task = self.tasks.pop(index)
            self.save_tasks()
            return deleted_task
        else:
            return None

    def list_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks_data]
        except FileNotFoundError:
            self.tasks = []

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.todo_list = ToDoList()

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # Frame for displaying tasks
        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack(padx=10, pady=10)

        # Text widget to display tasks
        self.task_text = tk.Text(self.tasks_frame, height=20, width=80)
        self.task_text.pack(side=tk.LEFT, padx=10)

        # Scrollbar for the text widget
        self.scrollbar = tk.Scrollbar(self.tasks_frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.task_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_text.config(yscrollcommand=self.scrollbar.set)

        # Entry widget for task description
        self.task_entry = tk.Entry(self.root, width=80)
        self.task_entry.pack(pady=5)

        # Combobox for task priority
        self.priority_combobox = ttk.Combobox(self.root, values=["Low", "Normal", "High"], state="readonly")
        self.priority_combobox.set("Normal")
        self.priority_combobox.pack(pady=5)

        # Entry widget for task due date
        self.due_date_entry = tk.Entry(self.root, width=80)
        self.due_date_entry.pack(pady=5)
        self.due_date_entry.insert(0, "Due Date [dd-mm-yyyy]")

        # Buttons for various actions
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(self.root, text="Update Task", command=self.update_task)
        self.update_button.pack(pady=5)

        self.complete_button = tk.Button(self.root, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def add_task(self):
        description = self.task_entry.get().strip()  # Get task description
        priority = self.priority_combobox.get()  # Get task priority
        due_date = self.due_date_entry.get().strip()  # Get due date

        if description:
            self.todo_list.add_task(description, priority, due_date)
            self.refresh_list()
            self.clear_task_entry()
        else:
            messagebox.showwarning("Warning", "Please enter a task description")

    def update_task(self):
        try:
            selected_task_text = self.task_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if selected_task_text:
                index = int(selected_task_text.split('.')[0]) - 1
                description = self.task_entry.get().strip()
                priority = self.priority_combobox.get()
                due_date = self.due_date_entry.get().strip()

                updated_task = self.todo_list.update_task(index, description, priority, due_date)
                if updated_task:
                    messagebox.showinfo("Success", f"Task updated: {updated_task}")
                    self.clear_task_entry()
                else:
                    messagebox.showerror("Error", "Invalid task number")
            else:
                messagebox.showwarning("Warning", "Please select a task to update")
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select a task to update")

    def complete_task(self):
        try:
            selected_task_text = self.task_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if selected_task_text:
                index = int(selected_task_text.split('.')[0]) - 1
                completed_task = self.todo_list.complete_task(index)
                if completed_task:
                    messagebox.showinfo("Success", f"Task completed: {completed_task}")
                else:
                    messagebox.showerror("Error", "Invalid task number")
                self.refresh_list()
            else:
                messagebox.showwarning("Warning", "Please select a task to complete")
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select a task to complete")

    def delete_task(self):
        try:
            selected_task_text = self.task_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if selected_task_text:
                index = int(selected_task_text.split('.')[0]) - 1
                deleted_task = self.todo_list.delete_task(index)
                if deleted_task:
                    messagebox.showinfo("Success", f"Task deleted: {deleted_task}")
                else:
                    messagebox.showerror("Error", "Invalid task number")
                self.refresh_list()
            else:
                messagebox.showwarning("Warning", "Please select a task to delete")
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select a task to delete")

    def refresh_list(self):
        self.task_text.delete(1.0, tk.END)
        task_list = self.todo_list.list_tasks()
        for i, task in enumerate(task_list, start=1):
            self.task_text.insert(tk.END, f"{i}. {task}\n")

    def clear_task_entry(self):
        self.task_entry.delete(0, tk.END)
        self.priority_combobox.set("Normal")
        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, "Due Date [dd-mm-yyyy]")

def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
