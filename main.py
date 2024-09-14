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
        tk.Label(root, text="Forrás mappa:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.source_folder, width=40).grid(row=0, column=1, padx=10)
        tk.Button(root, text="Tallózás", command=self.select_source_folder).grid(row=0, column=2, padx=10)

        tk.Label(root, text="Cél mappa:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.destination_folder, width=40).grid(row=1, column=1, padx=10)
        tk.Button(root, text="Tallózás", command=self.select_destination_folder).grid(row=1, column=2, padx=10)

        tk.Button(root, text="Manuális mentés", command=self.manual_backup).grid(row=2, column=0, columnspan=3, pady=10)
        tk.Button(root, text="12 óránkénti mentés indítása", command=self.start_scheduled_backup).grid(row=3, column=0, columnspan=3, pady=10)

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
