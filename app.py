from roster import create_student, check_in, list_today

def main():
    while True:
        print("\n=== KAB Attendance ===")
        print("1. Create student")
        print("2. Check-in (Present/Late)")
        print("3. List today's check-ins")
        print("4. Exit")
        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            sid = input("Student ID: ")
            create_student(name, sid)
        elif choice == "2":
            sid = input("Student ID: ")
            status = input("Status (Present/Late): ")
            check_in(sid, status)
        elif choice == "3":
            list_today()
        elif choice == "4":
            print("Bye")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()