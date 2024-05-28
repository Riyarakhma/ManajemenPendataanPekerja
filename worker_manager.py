import tkinter as tk
from tkinter import ttk, messagebox

class Worker:
    def __init__(self, id, name, age, position, salary):
        self.id = id
        self.name = name
        self.age = age
        self.position = position
        self.salary = salary

class WorkerManager:
    def __init__(self):
        self.workers = []  # List as stack
        self.queue = []    # List as queue

    def add_worker(self, worker):
        self.workers.append(worker)
        self.queue.append(worker)

    def remove_worker(self):
        if self.workers:
            worker = self.workers.pop()
            self.queue.remove(worker)
            return worker
        return None

    def get_all_workers(self):
        return self.workers

class Application(tk.Tk):
    def __init__(self, worker_manager):
        super().__init__()
        self.worker_manager = worker_manager
        self.title("Manajemen Pendataan Pekerja")
        self.geometry("1200x900")  # Increase window size
        
        self.configure(padx=40, pady=40, bg="#1F1F2E")  # Dark background for contrast

        # Apply theme and styles
        self.style = ttk.Style(self)
        self.configure_theme()

        self.create_widgets()

    def configure_theme(self):
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Arial", 30, "bold"), background="#1F1F2E", foreground="#A9A9A9")
        self.style.configure("TEntry", font=("Arial", 30), padding=10, foreground="#000000")
        self.style.configure("TButton", font=("Arial", 30, "bold"), background="#3B6AA0", foreground="white")
        self.style.map("TButton", background=[('active', '#2A4B73')], foreground=[('active', 'white')])
        self.style.configure("Treeview.Heading", font=("Arial", 30, "bold"), background="#3B6AA0", foreground="white")
        self.style.configure("Treeview", font=("Arial", 30), rowheight=75, background="#E6F0FA", foreground="black")
        self.style.map("Treeview", background=[('selected', '#3B6AA0')], foreground=[('selected', 'white')])

    def create_widgets(self):
        padding = {'padx': 100, 'pady': 30}

        self.label_id = ttk.Label(self, text="ID Pekerja")
        self.label_id.grid(row=0, column=0, **padding)
        self.entry_id = ttk.Entry(self, font=("Arial", 20), width=25)
        self.entry_id.grid(row=0, column=1, **padding)

        self.label_name = ttk.Label(self, text="Nama Pekerja")
        self.label_name.grid(row=1, column=0, **padding)
        self.entry_name = ttk.Entry(self, font=("Arial", 20), width=25)
        self.entry_name.grid(row=1, column=1, **padding)

        self.label_age = ttk.Label(self, text="Umur Pekerja")
        self.label_age.grid(row=2, column=0, **padding)
        self.entry_age = ttk.Entry(self, font=("Arial", 20), width=25)
        self.entry_age.grid(row=2, column=1, **padding)

        self.label_position = ttk.Label(self, text="Posisi Pekerja")
        self.label_position.grid(row=3, column=0, **padding)
        self.entry_position = ttk.Combobox(self, values=[
            "Direktur Utama", "Direktur", "Direktur Keuangan",
            "Direktur Personalia/HRD", "Manajer", "Manajer Personalia/HRD",
            "Manajer Pemasaran", "Manajer Pabrik", "Administrasi dan Gudang",
            "Lainnya"
        ], font=("Arial", 30), width=20)
        self.entry_position.grid(row=3, column=1, **padding)
        self.entry_position.bind("<<ComboboxSelected>>", self.on_position_selected)

        self.entry_position_manual = ttk.Entry(self, font=("Arial", 20), width=25)
        self.entry_position_manual.grid(row=4, column=1, **padding)
        self.entry_position_manual.grid_remove()  # Initially hidden

        self.label_salary = ttk.Label(self, text="Gaji Pekerja")
        self.label_salary.grid(row=5, column=0, **padding)
        self.entry_salary = ttk.Entry(self, font=("Arial", 20), width=25)
        self.entry_salary.grid(row=5, column=1, **padding)

        self.button_add = ttk.Button(self, text="Tambahkan Pekerja", command=self.add_worker)
        self.button_add.grid(row=6, column=0, **padding)

        self.button_show = ttk.Button(self, text="Tampilkan Semua Pekerja", command=self.show_workers)
        self.button_show.grid(row=6, column=1, **padding)

    def on_position_selected(self, event):
        if self.entry_position.get() == "Lainnya":
            self.entry_position_manual.grid()  # Show manual entry
        else:
            self.entry_position_manual.grid_remove()  # Hide manual entry

    def add_worker(self):
        id = self.entry_id.get()
        name = self.entry_name.get()
        age = self.entry_age.get()
        position = self.entry_position.get()
        salary = self.entry_salary.get()

        if position == "Lainnya":
            position = self.entry_position_manual.get()

        if id and name and age.isdigit() and position and salary.isdigit():
            new_worker = Worker(id, name, int(age), position, int(salary))
            self.worker_manager.add_worker(new_worker)
            self.show_add_worker_popup()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Semua field harus diisi dengan benar")

    def show_add_worker_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Pekerja Ditambahkan")
        popup.geometry("300x150")
        popup.configure(bg="#1F1F2E")

        label = ttk.Label(popup, text="Pekerja berhasil ditambahkan!", background="#1F1F2E", foreground="#A9A9A9", font=("Arial", 15))
        label.pack(pady=25)

        small_button_style = ttk.Style()
        small_button_style.configure("Small.TButton", font=("Arial", 10, "bold"), background="#3B6AA0", foreground="white")

        button_ok = ttk.Button(popup, text="OK", command=popup.destroy, style="Small.TButton")
        button_ok.pack(pady=20)

    def show_workers(self):
        workers = self.worker_manager.get_all_workers()
        if workers:
            self.show_workers_window(workers)
        else:
            messagebox.showinfo("Daftar Pekerja", "Tidak ada pekerja yang terdaftar")

    def show_workers_window(self, workers):
        window = tk.Toplevel(self)
        window.title("Daftar Pekerja")
        window.geometry("1000x800")  # Increase window size
        window.configure(bg="#A9A9A9")

        # Define a new style for the Treeview in this window
        tree_style = ttk.Style()
        tree_style.configure("SmallFont.Treeview", font=("Arial", 15), rowheight=40)
        tree_style.configure("SmallFont.Treeview.Heading", font=("Arial", 20, "bold"))

        tree = ttk.Treeview(window, columns=("ID", "Nama", "Umur", "Posisi", "Gaji"), show="headings", style="SmallFont.Treeview")
        tree.heading("ID", text="ID")
        tree.heading("Nama", text="Nama")
        tree.heading("Umur", text="Umur")
        tree.heading("Posisi", text="Posisi")
        tree.heading("Gaji", text="Gaji")

        for worker in workers:
            tree.insert("", "end", values=(worker.id, worker.name, worker.age, worker.position, worker.salary))

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_entries(self):
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_position.set('')  # Clear the combobox
        self.entry_position_manual.delete(0, tk.END)  # Clear manual entry
        self.entry_position_manual.grid_remove()  # Hide manual entry
        self.entry_salary.delete(0, tk.END)

if __name__ == "__main__":
    worker_manager = WorkerManager()
    app = Application(worker_manager)
    app.mainloop()
