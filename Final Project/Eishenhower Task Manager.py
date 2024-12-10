import streamlit as st
import pandas as pd
from datetime import datetime

#Fungsi buat hitung skor dan nentuin kategori tugas
def calculate_score_and_category(task):
    try:
        #Bobot buat ngitung skor, makin penting makin gede
        weights = {"Deadline": 0.4, "Prioritas": 0.3, "Durasi": 0.2, "Kesulitan": 0.1}
        prioritas_mapping = {"Tinggi": 3, "Sedang": 2, "Rendah": 1}
        kesulitan_mapping = {"Sulit": 3, "Sedang": 2, "Mudah": 1}

        #Hitung selisih hari dari deadline ke hari ini
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) #Biar fokus ke tanggal aja
        deadline_date = datetime.strptime(task["Deadline"], "%Y-%m-%d") #strp = string parse time (memecah string menjadi blok-blok jenis waktu (hari, bulan, dst))
        days_until_deadline = (deadline_date - today).days
        deadline_score = 1 if days_until_deadline <= 0 else days_until_deadline

        #Rumus buat total skor
        score = (
            weights["Deadline"] * deadline_score +
            weights["Prioritas"] * prioritas_mapping[task["Prioritas"]] +
            weights["Durasi"] * task["Durasi"] +
            weights["Kesulitan"] * kesulitan_mapping[task["Kesulitan"]]
        )

        #Nentuin kategori tugas berdasarkan Eisenhower Matrix
        urgency_threshold = 7
        if deadline_score <= urgency_threshold and prioritas_mapping[task["Prioritas"]] >= 2:
            category = "Do First"
        elif deadline_score > urgency_threshold and prioritas_mapping[task["Prioritas"]] >= 2:
            category = "Schedule"
        elif deadline_score <= urgency_threshold and prioritas_mapping[task["Prioritas"]] < 2:
            category = "Delegate"
        else:
            category = "Eliminate"

        return score, category
    except Exception as e:
        raise ValueError(f"Ada masalah waktu ngitung skor atau kategori: {e}")

#Judul aplikasi, biar user tahu ini alat keren buat ngatur tugas!
st.markdown("# Task Manager with Eisenhower Matrix")

#User bisa pilih mau input manual atau upload file CSV
method = st.radio("Mau input data gimana nih?", ["Input Manual", "Unggah File CSV"])

tasks = []

if method == "Input Manual":
    st.write("Oke, langsung aja masukin detail tugas:")
    num_tasks = st.number_input("Berapa banyak tugas yang mau dimasukin?", min_value=1, step=1)

    for i in range(num_tasks):
        with st.expander(f"Tugas {i+1}"):
            judul = st.text_input(f"Judul Tugas {i+1}")
            deadline = st.date_input(f"Deadline {i+1}").strftime("%Y-%m-%d")
            prioritas = st.selectbox(f"Prioritas {i+1}", ["Tinggi", "Sedang", "Rendah"])
            durasi = st.number_input(f"Durasi {i+1} (jam)", min_value=1)
            kesulitan = st.selectbox(f"Kesulitan {i+1}", ["Sulit", "Sedang", "Mudah"])
            tasks.append({
                "Judul Tugas": judul,
                "Deadline": deadline,
                "Prioritas": prioritas,
                "Durasi": durasi,
                "Kesulitan": kesulitan
            })

elif method == "Unggah File CSV":
    file = st.file_uploader("Upload file CSV kalian ya", type=["csv"])
    if file is not None:
        try:
            tasks_df = pd.read_csv(file)
            expected_columns = ["Judul Tugas", "Deadline", "Prioritas", "Durasi", "Kesulitan"]
            if not all(col in tasks_df.columns for col in expected_columns):
                st.error(f"File CSV harus punya kolom: {expected_columns}")
                tasks = []  #Kosongkan tasks kalo format salah
            else:
                tasks = tasks_df.to_dict(orient="records")
        except Exception as e:
            st.error(f"Ada masalah pas baca file CSV: {e}")

#Tombol buat proses tugas
if st.button("Proses Tugas"):
    if not tasks:
        st.warning("Yah, nggak ada tugas buat diproses nih!")
    else:
        valid_tasks = []
        for task in tasks:
            try:
                #Cek masing-masing tugas, valid apa enggak
                if not isinstance(task["Judul Tugas"], str) or task["Judul Tugas"] is None or task["Judul Tugas"] == "":
                    raise ValueError("Judul Tugas nggak valid.")
                datetime.strptime(task["Deadline"], "%Y-%m-%d")  #Validasi format tanggal
                if task["Prioritas"] not in ["Tinggi", "Sedang", "Rendah"]:
                    raise ValueError("Prioritas nggak valid.")
                if not isinstance(task["Durasi"], (int, float)) or task["Durasi"] <= 0:
                    raise ValueError("Durasi harus angka positif.")
                if task["Kesulitan"] not in ["Sulit", "Sedang", "Mudah"]:
                    raise ValueError("Kesulitan nggak valid.")

                #Kalau lolos validasi, hitung skor dan kategori
                task["Skor"], task["Kategori"] = calculate_score_and_category(task)
                valid_tasks.append(task)
            except Exception as e:
                st.warning(f"Ada masalah di tugas ini: {task}, Error: {e}")

        if valid_tasks:
            #Urutkan tugas berdasarkan kategori dan skor
            category_priority = {"Do First": 1, "Schedule": 2, "Delegate": 3, "Eliminate": 4}
            sorted_tasks = sorted(valid_tasks, key=lambda x: (category_priority[x["Kategori"]], -x["Skor"]))

            #Tampilkan hasilnya
            sorted_df = pd.DataFrame(sorted_tasks)
            st.write("Hasil Tugas yang Diurutkan:")
            st.dataframe(sorted_df)

            #Download hasil ke CSV
            csv = sorted_df.to_csv(index=False)
            st.download_button(label="Unduh Hasil ke CSV", data=csv, file_name="sorted_tasks.csv", mime="text/csv")
