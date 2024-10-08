import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

tasks_file = 'tasks.json'

def load_tasks():
    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(tasks_file, 'w') as file:
        json.dump(tasks, file)

def update_task_list(filtered_tasks=None):
    task_listbox.delete(0, tk.END)
    tasks = filtered_tasks if filtered_tasks is not None else load_tasks()
    
    for task in tasks:
        status = "✓" if task['completed'] else "✗"
        task_listbox.insert(tk.END, f"{status} {task['description']}")

def add_task():
    description = simpledialog.askstring("Input", "Enter the task:")
    if description:
        tasks = load_tasks()
        task = {"description": description, "completed": False}
        tasks.append(task)
        save_tasks(tasks)
        update_task_list()
        messagebox.showinfo("Success", "Task added")
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def view_pending_tasks():
    tasks = load_tasks()
    pending_tasks = [task for task in tasks if not task['completed']]
    update_task_list(pending_tasks)

def view_completed_tasks():
    tasks = load_tasks()
    completed_tasks = [task for task in tasks if task['completed']]
    update_task_list(completed_tasks)

def view_all_tasks():
    update_task_list()

def complete_task():
    tasks = load_tasks()
    selected_indices = task_listbox.curselection()
    
    for index in selected_indices:
        tasks[index]['completed'] = True
    
    save_tasks(tasks)
    update_task_list()
    messagebox.showinfo("Success", "Selected tasks marked as completed")

def delete_task():
    tasks = load_tasks()
    selected_indices = task_listbox.curselection()
    
    if not selected_indices:
        messagebox.showwarning("Warning", "Please select at least one task to delete.")
        return
    
   
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected tasks?")
    
    if confirm:
        for index in sorted(selected_indices, reverse=True):
            removed_task = tasks.pop(index)
        
        save_tasks(tasks)
        update_task_list()
        messagebox.showinfo("Success", f"Deleted {len(selected_indices)} task(s)")

root = tk.Tk()
root.title("To-Do List")
root.geometry("500x600")
root.configure(bg="#FAFA33")

titlebar_frame = tk.Frame(root, bg="#4CAF50", height=60)
titlebar_frame.pack(fill=tk.X)

heading = tk.Label(titlebar_frame, text="To-Do List", font="Arial 20 bold", fg="white", bg="#4CAF50")
heading.pack(pady=10)

frame = tk.Frame(root, bg="#90EE90")
frame.pack(pady=(10, 0))

task_listbox = tk.Listbox(frame, width=50, height=10, bg="#ffffff", fg="#000000", font=("Arial", 12), selectmode=tk.MULTIPLE)
task_listbox.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)

button_frame = tk.Frame(root, bg="#FAFA33")
button_frame.pack(pady=20)

button_bg_color = "#4CAF50"
button_fg_color = "white"

add_button = tk.Button(button_frame, text="Add Task", command=add_task, bg="#0000FF", fg=button_fg_color, font=("Arial", 10))
add_button.pack(pady=5)

view_all_button = tk.Button(button_frame, text="View All Tasks", command=view_all_tasks, bg="#ADD8E6", fg="white", font=("Arial", 10))
view_all_button.pack(pady=5)

complete_button = tk.Button(button_frame, text="Complete Task(s)", command=complete_task, bg=button_bg_color, fg=button_fg_color, font=("Arial", 10))
complete_button.pack(pady=5)

view_pending_button = tk.Button(button_frame, text="View Pending Tasks", command=view_pending_tasks, bg="#FFA500", fg=button_fg_color, font=("Arial", 10))
view_pending_button.pack(pady=5)

view_completed_button = tk.Button(button_frame, text="View Completed Tasks", command=view_completed_tasks, bg=button_bg_color, fg=button_fg_color, font=("Arial", 10))
view_completed_button.pack(pady=5)

delete_button = tk.Button(button_frame, text="Delete Task(s)", command=delete_task, bg="#FF0000", fg=button_fg_color, font=("Arial", 10))
delete_button.pack(pady=5)

update_task_list()

if __name__ == "__main__":
    root.mainloop()