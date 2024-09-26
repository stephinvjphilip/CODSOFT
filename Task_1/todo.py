import json
import os

tasks_file = 'tasks.json'
 
def main():
    while True:
     print("\nTo-do List")
     print("1. Add Task")
     print("2. View Pending Task")
     print("3. View Completed Task")
     print("4. Delete Task")
     print("5. Exit")

     choice = input("Choose an option from 1 to 5: ")

     if choice == '1':
        description = input("Enter the task: ")
        add_task(description)
     elif choice == '2':
        vp_task()
     elif choice == '3':
        vc_task()
     elif choice == '4':
        index = int(input("Enter the task number to delete: ")) - 1
        del_task(index)
     elif choice == '5':
        break
     else:
        print("Invalid Option")

def load_tasks():
    if os.path.exists(tasks_file):
        with open(tasks_file, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(tasks_file, 'w') as file:
        json.dumb(tasks, file)

def add_task(description):
    tasks = load_tasks()
    task = {"description": description, "completed": False}
    tasks.append(task)
    save_tasks(task)
    print("Task added")

def vp_task():
    tasks = load_tasks()
    print("\nPending Tasks:")
    for index,  task in enumerate(tasks):
        if not task['completed']:
            print(f"{index + 1}.{task['description']}")

def vc_task():
    tasks = load_tasks()
    print("\nCompleted Tasks:")
    for index, task in enumerate(tasks):
        if task['Completed']:
            print(f"{index + 1}.{task['description']}")

def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index] ['completed'] = True
        save_tasks(tasks)
        print("Task Marked as completed")
    else:
        print("Invalid task number")

def del_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed_task = tasks.pop(index)
        save_tasks(tasks)
        print(f"Task'{removed_task['description']}' deleted")
    else:
        print("Invaild task number")

if __name__ == "__main__":
    main()