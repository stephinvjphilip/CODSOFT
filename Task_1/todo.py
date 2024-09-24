import json
import os

tasks_file = 'tasks.json'

if __name__ == "__main__":
    main() 
def main():
    while True:
    print("\nTo-do List")
    print("1. Add Task")
    print("2. View Pending Task")
    print("3. View Completed task")
    print("4. Delete task")
    Print("5. Exit")

    choice = input("Choose an option from 1 to 5")

    if choice == '1':
        add_task()
    elif choice == '2':
        vp_task()
    elif choice == '3':
        vc_task()
    elif choice == '4':
        del_task()
    elif choice == '5':
        break
    else:
        print("Invalid Option")