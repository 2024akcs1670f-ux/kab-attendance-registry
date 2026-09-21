import json
import os
from datetime import datetime

FILE = "attendance_log.json"

def load():
    if not os.path.exists(FILE):
        return {"students": {}, "records": []}
    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_student(name, student_id):
    data = load()
    if student_id in data["students"]:
        print("Student already exists")
        return
    data["students"][student_id] = {"name": name, "id": student_id}
    save(data)
    print("Student created:", name)

def check_in(student_id, status):
    data = load()
    if student_id not in data["students"]:
        print("Student not found")
        return
    if status not in ["Present", "Late"]:
        print("Status must be Present or Late")
        return
    today = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["records"].append({
        "student_id": student_id,
        "name": data["students"][student_id]["name"],
        "date": today,
        "status": status,
        "timestamp": time
    })
    save(data)
    print("Checked in as", status)

def list_today():
    data = load()
    today = datetime.now().strftime("%Y-%m-%d")
    print("\nToday's check-ins:")
    found = False
    for r in data["records"]:
        if r["date"] == today:
            print(r["name"], "-", r["status"])
            found = True
    if not found:
        print("No check-ins today")