from datetime import datetime

#Fungsi untuk meminta input dari pengguna
def get_task_input():
    nama = input("Masukkan nama tugas: ")
    deadline = input("Masukkan deadline tugas (format YYYY-MM-DD): ")
    prioritas = int(input("Masukkan prioritas tugas: "))
    return {"nama": nama, "deadline": deadline, "prioritas": prioritas}

#Input tugas dari pengguna
tasks = []
task_count = int(input("Berapa banyak tugas yang ingin dimasukkan? "))
for _ in range(task_count):
    task = get_task_input()
    tasks.append(task)

#Mengubah deadline ke format tanggal
for task in tasks:
    task["deadline"] = datetime.strptime(task["deadline"], "%Y-%m-%d")

#Mengurutkan berdasarkan deadline dan prioritas
tasks_sorted_by_priority_and_deadline = sorted(tasks, key=lambda x: (x["deadline"], -x["prioritas"]))

#Menampilkan hasil
for task in tasks_sorted_by_priority_and_deadline:
    print(f"{task['nama']} - Deadline: {task['deadline'].strftime('%Y-%m-%d')} - Prioritas: {task['prioritas']}")