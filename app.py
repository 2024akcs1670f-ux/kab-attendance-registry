
from reporting import (mark_absentees, print_chronic_report,
                       run_mark_absentees, run_student_rate)

def main():
    while True:
        print("\n=== KAB Attendance Registry ===")
        print("4. Mark absentees")
        print("5. Chronic absence report")
        print("6. Student attendance rate and streaks")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "4":
            run_mark_absentees()
        elif choice == "5":
            print_chronic_report()
        elif choice == "6":
            run_student_rate()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()