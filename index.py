import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

class TodoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")
        
        # Create the task list
        self.tasks = []
        
        # Create GUI elements
        self.task_entry = tk.Entry(master, width=50)
        self.task_entry.pack(pady=10)
        
        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.pack()
        
        self.task_listbox = tk.Listbox(master, width=50)
        self.task_listbox.pack(pady=10)
        
        self.remove_button = tk.Button(master, text="Remove Task", command=self.remove_task)
        self.remove_button.pack()
        
        self.edit_button = tk.Button(master, text="Edit Task", command=self.edit_task)
        self.edit_button.pack()
        
        self.save_button = tk.Button(master, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack()
        
        self.load_button = tk.Button(master, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack()
    
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
    
    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            self.task_listbox.delete(task_index)
    
    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            new_task = simpledialog.askstring("Edit Task", "Enter the new task:")
            if new_task:
                self.tasks[task_index] = new_task
                self.task_listbox.delete(task_index)
                self.task_listbox.insert(task_index, new_task)
    
    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for task in self.tasks:
                f.write(task + "\n")
    
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                self.tasks = [line.strip() for line in f.readlines()]
                self.task_listbox.delete(0, tk.END)
                for task in self.tasks:
                    self.task_listbox.insert(tk.END, task)
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "No tasks file found.")

root = tk.Tk()
app = TodoListApp(root)
root.mainloop()
