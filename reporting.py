"""Absence & Reporting module (Student B).

Reads and updates attendance_log.json with the shape:
{
  "students": [{"student_id": "S001", "name": "Ann"}],
  "records":  [{"student_id": "S001", "date": "2025-01-15",
                "status": "Present", "timestamp": "..."}]
}
"""
import json
import os
from datetime import date, datetime

LOG_FILE = "attendance_log.json"
THRESHOLD = 85.0  # below this % a student is chronically absent
ATTENDED = ("Present", "Late")


def load_log():
    if not os.path.exists(LOG_FILE):
        return {"students": [], "records": []}
    with open(LOG_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    data.setdefault("students", [])
    data.setdefault("records", [])
    return data


def save_log(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def school_days(data):
    """Every date that has at least one record counts as a school day."""
    return sorted({r["date"] for r in data["records"]})


def mark_absentees(day=None):
    """Flag every registered student with no record on `day` as Absent.
    Returns the list of students newly marked absent."""
    day = day or date.today().isoformat()
    data = load_log()
    seen = {r["student_id"] for r in data["records"] if r["date"] == day}
    flagged = []
    for s in data["students"]:
        if s["student_id"] not in seen:
            data["records"].append({
                "student_id": s["student_id"],
                "date": day,
                "status": "Absent",
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            })
            flagged.append(s)
    save_log(data)
    return flagged


def status_by_day(data, student_id):
    """Map date -> status for one student. Missing days count as Absent."""
    recorded = {r["date"]: r["status"] for r in data["records"]
                if r["student_id"] == student_id}
    return {d: recorded.get(d, "Absent") for d in school_days(data)}


def attendance_rate(data, student_id):
    days = status_by_day(data, student_id)
    if not days:
        return 100.0
    attended = sum(1 for s in days.values() if s in ATTENDED)
    return round(attended / len(days) * 100, 1)


def absence_streaks(data, student_id):
    """Return (longest streak, current streak) of consecutive absent school days."""
    longest = current = 0
    for d, status in sorted(status_by_day(data, student_id).items()):
        if status == "Absent":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest, current


def chronic_absentees(data=None, threshold=THRESHOLD):
    data = data or load_log()
    result = []
    for s in data["students"]:
        rate = attendance_rate(data, s["student_id"])
        if rate < threshold:
            longest, current = absence_streaks(data, s["student_id"])
            result.append({**s, "rate": rate, "longest": longest, "current": current})
    return sorted(result, key=lambda x: x["rate"])


def print_chronic_report():
    data = load_log()
    days = len(school_days(data))
    rows = chronic_absentees(data)
    print(f"\n=== Chronic Absence Report (below {THRESHOLD:.0f}%) ===")
    print(f"School days on record: {days}")
    if not rows:
        print("No chronically absent students.")
        return
    print(f"{'ID':<10}{'Name':<22}{'Rate':>7}{'Max streak':>12}{'Now':>6}")
    for r in rows:
        print(f"{r['student_id']:<10}{r['name']:<22}{r['rate']:>6}%"
              f"{r['longest']:>12}{r['current']:>6}")


def run_mark_absentees():
    day = input("Date (YYYY-MM-DD, blank for today): ").strip() or None
    try:
        if day:
            datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return
    flagged = mark_absentees(day)
    if not flagged:
        print("Nobody to flag, everyone already has a record.")
    for s in flagged:
        print(f"Marked absent: {s['student_id']} {s['name']}")


def run_student_rate():
    sid = input("Student ID: ").strip()
    data = load_log()
    if not any(s["student_id"] == sid for s in data["students"]):
        print("Student not found.")
        return
    longest, current = absence_streaks(data, sid)
    print(f"Attendance rate: {attendance_rate(data, sid)}%")
    print(f"Longest absence streak: {longest} day(s), current: {current}")