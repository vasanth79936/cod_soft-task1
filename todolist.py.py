import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = "tasks.json"

#common for both
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

#console interface
def view_tasks(tasks):
    if not tasks:
        print("\n No tasks found!\n")
        return
    print("\n Your To-Do List:")
    for idx, task in enumerate(tasks, 1):
        status = " Done" if task["completed"] else " Pending"
        print(f"{idx}. {task['title']} - {status}")

def add_task_commandline(tasks):
    title = input("Enter task title: ")
    tasks.append({"title": title, "completed": False})
    save_tasks(tasks)
    print(" Task added successfully!")

def mark_complete_commandline(tasks):
    view_tasks(tasks)
    try:
        choice = int(input("Enter task number to mark complete: ")) - 1
        tasks[choice]["completed"] = True
        save_tasks(tasks)
        print(" Task marked complete!")
    except (ValueError, IndexError):
        print(" Invalid selection!")

def delete_task_commandline(tasks):
    view_tasks(tasks)
    try:
        choice = int(input("Enter task number to delete: ")) - 1
        tasks.pop(choice)
        save_tasks(tasks)
        print(" Task deleted!")
    except (ValueError, IndexError):
        print(" Invalid selection!")

def commandline_main():
    tasks = load_tasks()
    while True:
        print("\n==== TO-DO LIST MENU ====")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Mark Task Complete")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")
        match choice:
         case "1":
            view_tasks(tasks)
         case "2":
            add_task_commandline(tasks)
            tasks = load_tasks()
         case "3":
            mark_complete_commandline(tasks)
            tasks = load_tasks()
         case "4":
            delete_task_commandline(tasks)
            tasks = load_tasks()
         case "5":
            print("exiting!")
            break
         case _ :
            print("Invalid choice!please choice a appropriate choice")

# ------------------- GUI Functions -------------------
def refresh_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "Finished" if task["completed"] else "Pending"
        listbox.insert(tk.END, f"{status}-{task['title']}")

def add_task_interface():
    title = entry.get()
    if title.strip():
        tasks.append({"title": title, "completed": False})
        save_tasks(tasks)
        entry.delete(0, tk.END)
        refresh_listbox()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def mark_complete_interface():
    try:
        index = listbox.curselection()[0]
        tasks[index]["completed"] = True
        save_tasks(tasks)
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark complete!")

def delete_task_interface():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        save_tasks(tasks)
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete!")

def interface_main():
    global root, entry, listbox, tasks

    root = tk.Tk()
    root.title("To-Do List App")
    root.geometry("400x400")
    root.configure(bg="lightblue") 

    tasks = load_tasks()

    # Entry + Add button
    frame = tk.Frame(root,bg="lightgreen")
    frame.pack(pady=10)

    entry = tk.Entry(frame, width=25)
    entry.grid(row=0, column=0, padx=5)

    add_button = tk.Button(frame, text="Add Task", command=add_task_interface)
    add_button.grid(row=0, column=1)

    # Task Listbox
    listbox = tk.Listbox(root, width=50, height=15)
    listbox.pack(pady=10)

    refresh_listbox()

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    complete_button = tk.Button(button_frame, text="Mark Complete", command=mark_complete_interface)
    complete_button.grid(row=0, column=0, padx=5)

    delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task_interface)
    delete_button.grid(row=0, column=1, padx=5)

    root.mainloop()
#start
if __name__ == "__main__":
    print("==== TO-DO LIST APPLICATION ====")
    print("1. Run in Command Line (CLI)")
    print("2. Run in Graphical Interface (GUI)")
    mode = input("Choose mode (1/2): ")
    match mode:
     case "1":
        commandline_main()
     case "2":
        interface_main()
     case _:
        print(" Invalid choice! Exiting...")
