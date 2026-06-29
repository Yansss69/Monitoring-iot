import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd
from PIL import Image, ImageTk
import os

# --- FUNGSI-FUNGSI LOGIKA ---
def tambah_log():
    try:
        t_start = datetime.strptime(entry_start.get().strip(), "%H:%M")
        durasi = int(pilihan_durasi.get())
        t1 = t_start + timedelta(minutes=3)
        t2 = t1 + timedelta(minutes=12)
        t3 = t2 + timedelta(minutes=3)
        t_selesai = t_start + timedelta(minutes=durasi)

        lb1.insert(tk.END, f"{t_start.strftime('%H:%M')} | {t1.strftime('%H:%M')} | {t2.strftime('%H:%M')} | {t3.strftime('%H:%M')}")
        lb2.insert(tk.END, f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}")
        lb3.insert(tk.END, f"{t_start.strftime('%H:%M')} - {t_selesai.strftime('%H:%M')}")
        status_var.set("Status: Log ditambahkan.")
    except ValueError:
        status_var.set("Status: Format jam salah!")

def edit_terpilih():
    current_tab = notebook.index(notebook.select())
    target_lb = [lb1, lb2, lb3][current_tab]
    idx = target_lb.curselection()
    if idx:
        text = target_lb.get(idx[0])
        mulai = text.split(" ")[0]
        entry_start.delete(0, tk.END)
        entry_start.insert(0, mulai)
        status_var.set(f"Status: Mode Edit Tab {current_tab+1}")

def update_baris():
    current_tab = notebook.index(notebook.select())
    target_lb = [lb1, lb2, lb3][current_tab]
    idx = target_lb.curselection()
    if not idx: return
    i = idx[0]
    try:
        t_start = datetime.strptime(entry_start.get().strip(), "%H:%M")
        durasi = int(pilihan_durasi.get())
        t1 = t_start + timedelta(minutes=3)
        t2 = t1 + timedelta(minutes=12)
        t3 = t2 + timedelta(minutes=3)
        t_selesai = t_start + timedelta(minutes=durasi)
        target_lb.delete(i)
        if current_tab == 0: target_lb.insert(i, f"{t_start.strftime('%H:%M')} | {t1.strftime('%H:%M')} | {t2.strftime('%H:%M')} | {t3.strftime('%H:%M')}")
        elif current_tab == 1: target_lb.insert(i, f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}")
        else: target_lb.insert(i, f"{t_start.strftime('%H:%M')} - {t_selesai.strftime('%H:%M')}")
    except ValueError: status_var.set("Status: Format jam salah!")

def simpan_ke_excel():
    try:
        data1 = list(lb1.get(0, tk.END))
        data2 = list(lb2.get(0, tk.END))
        data3 = list(lb3.get(0, tk.END))
        max_len = max(len(data1), len(data2), len(data3))
        data1 += [None] * (max_len - len(data1))
        data2 += [None] * (max_len - len(data2))
        data3 += [None] * (max_len - len(data3))
        df = pd.DataFrame({"3m + 12m": data1, "Proses": data2, "Hasil Mixing": data3})
        df.to_excel("Log_Produksi.xlsx", index=False)
        status_var.set("Status: Berhasil disimpan ke Excel")
    except Exception as e: status_var.set(f"Status: Gagal! {e}")

def hapus_terpilih():
    current_tab = notebook.index(notebook.select())
    target_lb = [lb1, lb2, lb3][current_tab]
    idx = target_lb.curselection()
    if idx: target_lb.delete(idx[0])

# --- GUI SETUP ---
root = tk.Tk()
root.geometry("400x900")
root.title("Line Sachet Production")
root.configure(bg="#e3f2fd")

# Menampilkan Logo
try:
    if os.path.exists("logo.png"):
        img = Image.open("logo.png")
        img = img.resize((150, 75), Image.Resampling.LANCZOS)
        logo_tk = ImageTk.PhotoImage(img)
        lbl_logo = tk.Label(root, image=logo_tk, bg="#e3f2fd")
        lbl_logo.image = logo_tk  # Menjaga referensi agar tidak hilang
        lbl_logo.pack(pady=10)
except Exception as e:
    print(f"Gagal memuat logo: {e}")

# Judul
tk.Label(root, text="LINE SACHET MONITORING", font=("Arial", 16, "bold"), bg="#1565c0", fg="white").pack(fill="x", pady=(0, 10))

# Input Area
frame_input = tk.LabelFrame(root, text="Input Data", bg="#e3f2fd", fg="#1565c0", font=("Arial", 10, "bold"))
frame_input.pack(fill="x", padx=10, pady=5)
entry_start = tk.Entry(frame_input, font=("Arial", 16), justify="center", bg="#ffffff")
entry_start.insert(0, "09:41")
entry_start.pack(fill="x", padx=5, pady=5)

pilihan_durasi = tk.StringVar(value="50")
frame_rad = tk.Frame(frame_input, bg="#e3f2fd")
frame_rad.pack(pady=5)
for text, val in [("50 Min", "50"), ("40 Min", "40")]:
    tk.Radiobutton(frame_rad, text=text, variable=pilihan_durasi, value=val, bg="#e3f2fd").pack(side="left", padx=10)

# Listbox Area
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10)

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook.Tab", background="#bbdefb")

lb1 = tk.Listbox(notebook, font=("Arial", 12), bg="#ffffff", fg="#1565c0"); notebook.add(lb1, text="3m + 12m")
lb2 = tk.Listbox(notebook, font=("Arial", 12), bg="#ffffff", fg="#1565c0"); notebook.add(lb2, text="Proses")
lb3 = tk.Listbox(notebook, font=("Arial", 12), bg="#ffffff", fg="#1565c0"); notebook.add(lb3, text="Hasil Mixing")

# Buttons Area
btn_frame = tk.Frame(root, bg="#e3f2fd")
btn_frame.pack(fill="x", padx=10, pady=10)
btn_config = {"fill": "x", "pady": 2}
tk.Button(btn_frame, text="TAMBAH LOG", command=tambah_log, bg="#1976d2", fg="white").pack(**btn_config)
tk.Button(btn_frame, text="EDIT DATA", command=edit_terpilih, bg="#1976d2", fg="white").pack(**btn_config)
tk.Button(btn_frame, text="UPDATE", command=update_baris, bg="#1976d2", fg="white").pack(**btn_config)
tk.Button(btn_frame, text="HAPUS", command=hapus_terpilih, bg="#d32f2f", fg="white").pack(**btn_config)
tk.Button(btn_frame, text="SIMPAN EXCEL", command=simpan_ke_excel, bg="#0d47a1", fg="white").pack(fill="x", pady=5)

# Status Bar
status_var = tk.StringVar(value="Status: Ready")
tk.Label(root, textvariable=status_var, bg="#1565c0", fg="white", anchor="w").pack(side="bottom", fill="x")

root.mainloop()
