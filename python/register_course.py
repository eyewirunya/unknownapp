#!/usr/bin/env python3

from EnrollmentSystem import EnrollmentSystem, EnrollmentResult
from DataManager import DataManager

def main():
    system = EnrollmentSystem()
    data_manager = DataManager()

    # Load data or seed defaults
    if data_manager.data_files_exist():
        try:
            data_manager.load_data(system)
            print("[INFO] Data loaded from disk.")
        except Exception as e:
            print(f"[WARN] Could not load saved data: {e}")
            print("[INFO] Starting with default data.")
            data_manager.seed_default_data(system)
    else:
        print("[INFO] First run detected — loading default course catalog and sample students.")
        data_manager.seed_default_data(system)

    # Simple demo: Register a student for a course
    print("\n=== Course Enrollment Demo ===")
    print("Available students:")
    for student in system.get_all_students():
        print(f"  {student}")

    student_id = input("\nEnter Student ID to register: ").strip()
    student = system.get_student(student_id)
    if not student:
        print(f"[ERROR] Student {student_id} not found.")
        return

    print(f"\nWelcome, {student.name}!")
    print("\nAvailable courses:")
    print(f"{'Code':<10} {'Title':<40} {'Credits':<8} {'Seats':<12} {'Time':<18} Prerequisites")
    print("-" * 100)
    for course in system.get_all_courses():
        print(course)

    course_code = input(f"\nEnter course code to register {student.name} for: ").strip().upper()
    result = system.register_course(student_id, course_code)
    if result.success:
        print(f"[SUCCESS] {result.message}")
    else:
        print(f"[ERROR] {result.message}")

    # Save data
    try:
        data_manager.save_data(system)
        print("[INFO] Data saved.")
    except Exception as e:
        print(f"[ERROR] Could not save data: {e}")

if __name__ == "__main__":
    main()