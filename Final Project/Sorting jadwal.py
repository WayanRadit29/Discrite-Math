from datetime import datetime

# Data tugas
tasks = [
    {"nama": "Tugas A", "deadline": "2024-11-15", "prioritas": 2, "importance": 1, "urgency": 1},  # Penting dan Mendesak
    {"nama": "Tugas B", "deadline": "2024-11-13", "prioritas": 3, "importance": 1, "urgency": 0},  # Penting tetapi Tidak Mendesak
    {"nama": "Tugas C", "deadline": "2024-11-20", "prioritas": 1, "importance": 0, "urgency": 1},  # Tidak Penting tapi Mendesak
    {"nama": "Tugas D", "deadline": "2024-11-12", "prioritas": 3, "importance": 0, "urgency": 0},  # Tidak Penting dan Tidak Mendesak
]

# Mengubah deadline ke format tanggal
for task in tasks:
    task["deadline"] = datetime.strptime(task["deadline"], "%Y-%m-%d")

# Menentukan kategori berdasarkan Eisenhower Matrix
def categorize_task(task):
    if task["importance"] == 1 and task["urgency"] == 1:
        return "Do It"
    elif task["importance"] == 0 and task["urgency"] == 1:
        return "Delegate"
    elif task["importance"] == 1 and task["urgency"] == 0:
        return "Schedule"
    else:
        return "Cut Off"

# Mengurutkan berdasarkan kategori Eisenhower Matrix, lalu deadline
tasks_sorted = sorted(tasks, key=lambda x: (categorize_task(x), x["deadline"], x["prioritas"]))

# Menampilkan hasil
for task in tasks_sorted:
    category = categorize_task(task)
    print(f"{task['nama']} - Deadline: {task['deadline'].strftime('%Y-%m-%d')} - Prioritas: {task['prioritas']} - Kategori: {category}")
