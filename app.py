      import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- SETTING HALAMAN ---
st.set_page_config(page_title="Line Sachet Monitoring", page_icon="📊")
st.title("Line Sachet Monitoring")

# --- INISIALISASI DATA ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    jam_mulai = st.text_input("Jam Mulai (HH:MM)", "09:41")
with col2:
    durasi = st.radio("Durasi:", [40, 50], horizontal=True)

# --- LOGIKA TAMBAH LOG ---
if st.button("Tambah Log"):
    try:
        t_start = datetime.strptime(jam_mulai.strip(), "%H:%M")
        t1 = t_start + timedelta(minutes=3)
        t2 = t1 + timedelta(minutes=12)
        t3 = t2 + timedelta(minutes=3)
        t_selesai = t_start + timedelta(minutes=durasi)

        st.session_state.logs.append({
            "3m + 12m": f"{t_start.strftime('%H:%M')} | {t1.strftime('%H:%M')} | {t2.strftime('%H:%M')} | {t3.strftime('%H:%M')}",
            "Proses": f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}",
            "Hasil Mixing": f"{t_start.strftime('%H:%M')} - {t_selesai.strftime('%H:%M')}"
        })
        st.success("Log berhasil ditambahkan!")
    except ValueError:
        st.error("Format jam salah! Gunakan HH:MM")

# --- MENAMPILKAN DATA ---
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    st.table(df)
    
    # Tombol Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "Log_Produksi.csv", "text/csv")

    if st.button("Hapus Semua Data"):
        st.session_state.logs = []
        st.rerun()
  
