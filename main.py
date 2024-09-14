import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import schedule
import time
from threading import Thread
from datetime import datetime

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MSC Backup")

        # Forrás és cél mappa változók
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()

        # GUI elemek
        self.language_selector = tk.OptionMenu(root, self.language, *LANGUAGES.keys(), command=self.update_language)
        self.language_selector.grid(row=0, column=1, padx=10, pady=10)

        self.source_label = tk.Label(root, text=self.translations['source_label'])
        self.source_label.grid(row=1, column=0, padx=10, pady=10)
        self.source_entry = tk.Entry(root, textvariable=self.source_folder, width=40)
        self.source_entry.grid(row=1, column=1, padx=10)
        self.source_button = tk.Button(root, text=self.translations['browse'], command=self.select_source_folder)
        self.source_button.grid(row=1, column=2, padx=10)

        self.destination_label = tk.Label(root, text=self.translations['destination_label'])
        self.destination_label.grid(row=2, column=0, padx=10, pady=10)
        self.destination_entry = tk.Entry(root, textvariable=self.destination_folder, width=40)
        self.destination_entry.grid(row=2, column=1, padx=10)
        self.destination_button = tk.Button(root, text=self.translations['browse'],command=self.select_destination_folder)
        self.destination_button.grid(row=2, column=2, padx=10)

        self.manual_backup_button = tk.Button(root, text=self.translations['manual_backup'], command=self.manual_backup)
        self.manual_backup_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.schedule_button = tk.Button(root, text=self.translations['start_schedule'], command=self.start_scheduled_backup)
        self.schedule_button.grid(row=4, column=0, columnspan=3, pady=10)

        def update_language(self, event=None):
        """Frissíti a felület szövegeit a kiválasztott nyelv szerint."""
        self.translations = LANGUAGES[self.language.get()]

        # Szövegek frissítése
        self.source_label.config(text=self.translations['source_label'])
        self.destination_label.config(text=self.translations['destination_label'])
        self.source_button.config(text=self.translations['browse'])
        self.destination_button.config(text=self.translations['browse'])
        self.manual_backup_button.config(text=self.translations['manual_backup'])
        self.schedule_button.config(text=self.translations['start_schedule'])

    def select_source_folder(self):
        folder_selected = filedialog.askdirectory()
        self.source_folder.set(folder_selected)

    def select_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        self.destination_folder.set(folder_selected)

    def manual_backup(self):
        source = self.source_folder.get()
        destination = self.destination_folder.get()

        if not os.path.exists(source):
            messagebox.showerror("Hiba", "A forrás mappa nem létezik!")
            return

        if not os.path.exists(destination):
            messagebox.showerror("Hiba", "A cél mappa nem létezik!")
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            destination_path = os.path.join(destination, f"backup_{timestamp}")
            shutil.copytree(source, destination_path)
            messagebox.showinfo("Siker", f"Sikeresen elmentve ide: {destination_path}")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt a mentés során: {e}")

    def start_scheduled_backup(self):
        source = self.source_folder.get()
        destination = self.destination_folder.get()

        if not os.path.exists(source) or not os.path.exists(destination):
            messagebox.showerror("Hiba", "Állítsd be a forrás- és célmappát!")
            return

        # Ütemezett mentés 12 óránként
        schedule.every(12).hours.do(self.scheduled_backup)

        # Háttérszál indítása az ütemezett feladatokhoz
        t = Thread(target=self.run_scheduler)
        t.daemon = True
        t.start()

        messagebox.showinfo("Ütemezés", "12 óránkénti mentés elindítva!")

    def scheduled_backup(self):
        source = self.source_folder.get()
        destination = self.destination_folder.get()

        if os.path.exists(source) and os.path.exists(destination):
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                destination_path = os.path.join(destination, f"backup_{timestamp}")
                shutil.copytree(source, destination_path)
                print(f"Sikeres mentés: {destination_path}")
            except Exception as e:
                print(f"Hiba történt a mentés során: {e}")
        else:
            print("A forrás vagy cél mappa nem elérhető.")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(60)  # Ellenőriz minden percben

# Fő program
if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
