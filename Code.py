import tkinter as tk
from tkinter import ttk, messagebox, font


class Task:
    def __init__(self, description, priority, status=False):
        self.description = description
        self.priority = priority
        self.status = status

    def __str__(self):
        status_icon = "✅" if self.status else "◻️"
        return f"{status_icon} [{self.priority}] {self.description}"


class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do List")
        self.root.geometry("600x500")
        self.tasks = []

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._setup_styles()

        # Create GUI
        self._create_widgets()

    def _setup_styles(self):
        self.style.configure("Green.TButton", foreground="white", background="#4CAF50", font=("Segoe UI", 10))
        self.style.configure("Blue.TButton", foreground="white", background="#2196F3", font=("Segoe UI", 10))
        self.style.configure("Red.TButton", foreground="white", background="#FF5252", font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="white", bordercolor="#cccccc")

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Title
        title_font = font.Font(family="Segoe UI", size=18, weight="bold")
        ttk.Label(main_frame, text="To Do List", font=title_font, foreground="#2c3e50").pack(pady=10)

        # Input Area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        self.task_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        self.priority_var = tk.StringVar(value="Medium")
        priorities = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                  values=["High", "Medium", "Low"], width=8)
        priorities.pack(side=tk.LEFT, padx=5)

        ttk.Button(input_frame, text="Add", style="Green.TButton",
                   command=self.add_task).pack(side=tk.LEFT)

        # Search Area
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        self.search_entry = ttk.Entry(search_frame, font=("Segoe UI", 12))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Search", style="Blue.TButton",
                   command=self.search_tasks).pack(side=tk.LEFT)

        # Task List
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.task_list = tk.Listbox(list_frame, bg="white", font=("Segoe UI", 12),
                                    selectbackground="#e0e0e0", activestyle="none")
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_list.yview)

        # Control Buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Delete", style="Red.TButton",
                   command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Sort by Priority", style="Blue.TButton",
                   command=self.sort_by_priority).pack(side=tk.LEFT, padx=5)

    def add_task(self):
        description = self.task_entry.get().strip()
        priority = self.priority_var.get()

        if description:
            task = Task(description, priority)
            self.tasks.append(task)
            self._update_display()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Task", "Please enter a task!")

    def delete_task(self):
        try:
            index = self.task_list.curselection()[0]
            del self.tasks[index]
            self._update_display()
        except IndexError:
            messagebox.showwarning("Error", "Please select a task to delete!")

    def search_tasks(self):
        query = self.search_entry.get().lower()
        filtered = [t for t in self.tasks if query in t.description.lower() or query in t.priority.lower()]
        self._update_display(filtered)

    def sort_by_priority(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda x: priority_order[x.priority])
        self._update_display()

    def _update_display(self, tasks=None):
        self.task_list.delete(0, tk.END)
        display_tasks = tasks if tasks else self.tasks
        for task in display_tasks:
            self.task_list.insert(tk.END, str(task))


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()