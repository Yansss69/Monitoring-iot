import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Line Sachet Monitoring", page_icon="📊")
st.title("Line Sachet Monitoring")

if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    jam_mulai = st.text_input("Jam Mulai (HH:MM)", "09:41")
with col2:
    durasi = st.radio("Durasi:", [40, 50], horizontal=True)

# --- FUNGSI LOGIKA ---
def hitung_waktu(jam_mulai, durasi):
    t_start = datetime.strptime(jam_mulai.strip(), "%H:%M")
    t1 = t_start + timedelta(minutes=3)
    t2 = t1 + timedelta(minutes=12)
    t3 = t2 + timedelta(minutes=3)
    t_selesai = t_start + timedelta(minutes=durasi)
    return {
        "3m + 12m": f"{t_start.strftime('%H:%M')} | {t1.strftime('%H:%M')} | {t2.strftime('%H:%M')} | {t3.strftime('%H:%M')}",
        "Proses": f"{t1.strftime('%H:%M')} - {t2.strftime('%H:%M')}",
        "Hasil Mixing": f"{t_start.strftime('%H:%M')} - {t_selesai.strftime('%H:%M')}"
    }

# --- FITUR TAMBAH ---
if st.button("Tambah Log"):
    try:
        st.session_state.logs.append(hitung_waktu(jam_mulai, durasi))
        st.success("Log ditambahkan!")
    except ValueError:
        st.error("Format jam salah!")

# --- FITUR EDIT & HAPUS ---
if st.session_state.logs:
    st.subheader("Data Log")
    df = pd.DataFrame(st.session_state.logs)
    
    # Pilih baris untuk diedit/dihapus
    index_to_edit = st.selectbox("Pilih baris untuk tindakan:", range(len(df)), format_func=lambda x: f"Baris {x+1}")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Edit Baris Terpilih"):
            st.session_state.logs[index_to_edit] = hitung_waktu(jam_mulai, durasi)
            st.rerun()
    with col_b:
        if st.button("Hapus Baris Terpilih"):
            st.session_state.logs.pop(index_to_edit)
            st.rerun()

    st.table(df)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "Log_Produksi.csv", "text/csv")
