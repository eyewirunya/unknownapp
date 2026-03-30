import json
import os
from Course import Course
from Student import Student
from TimeSlot import TimeSlot

class DataManager:
    DATA_DIR = "data"
    STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
    COURSES_FILE = os.path.join(DATA_DIR, "courses.json")

    def save_data(self, system):
        os.makedirs(self.DATA_DIR, exist_ok=True)

        # Save students
        student_list = system.get_all_students()
        with open(self.STUDENTS_FILE, 'w') as f:
            json.dump([self.student_to_dict(s) for s in student_list], f, indent=2)

        # Save courses
        course_list = system.get_all_courses()
        with open(self.COURSES_FILE, 'w') as f:
            json.dump([self.course_to_dict(c) for c in course_list], f, indent=2)

    def load_data(self, system):
        # Load courses first
        if os.path.exists(self.COURSES_FILE):
            with open(self.COURSES_FILE, 'r') as f:
                course_data = json.load(f)
                for data in course_data:
                    course = self.dict_to_course(data)
                    system.add_course(course)

        # Load students
        if os.path.exists(self.STUDENTS_FILE):
            with open(self.STUDENTS_FILE, 'r') as f:
                student_data = json.load(f)
                for data in student_data:
                    student = self.dict_to_student(data)
                    system.add_student(student)

    def seed_default_data(self, system):
        # Default courses
        system.add_course(Course("CS101", "Intro to Programming", 3, 30, TimeSlot("MWF", "09:00", "10:00")))
        system.add_course(Course("CS201", "Data Structures", 3, 25, TimeSlot("MWF", "10:00", "11:00")))
        system.add_course(Course("CS301", "Algorithms", 3, 25, TimeSlot("TTh", "09:00", "10:30")))
        system.add_course(Course("CS401", "Operating Systems", 3, 20, TimeSlot("TTh", "10:30", "12:00")))
        system.add_course(Course("MATH101", "Calculus I", 4, 35, TimeSlot("MWF", "08:00", "09:00")))
        system.add_course(Course("MATH201", "Calculus II", 4, 30, TimeSlot("MWF", "11:00", "12:00")))
        system.add_course(Course("ENG101", "Technical Writing", 2, 40, TimeSlot("TTh", "13:00", "14:00")))
        system.add_course(Course("NET101", "Computer Networks", 3, 25, TimeSlot("MWF", "14:00", "15:00")))
        system.add_course(Course("DB101", "Database Systems", 3, 25, TimeSlot("TTh", "14:00", "15:30")))
        system.add_course(Course("SE101", "Software Engineering", 3, 30, TimeSlot("MWF", "15:00", "16:00")))

        # Set prerequisites
        system.get_course("CS201").prerequisites = ["CS101"]
        system.get_course("CS301").prerequisites = ["CS201"]
        system.get_course("CS401").prerequisites = ["CS301"]

        # Sample students
        alice = Student("STU001", "Alice Johnson", "Computer Science")
        alice.completed_courses = ["CS101"]
        system.add_student(alice)

        bob = Student("STU002", "Bob Smith", "Mathematics")
        system.add_student(bob)

        carol = Student("STU003", "Carol Williams", "Information Technology")
        carol.completed_courses = ["CS101", "CS201"]
        system.add_student(carol)

    def data_files_exist(self):
        return os.path.exists(self.STUDENTS_FILE) and os.path.exists(self.COURSES_FILE)

    def student_to_dict(self, student):
        return {
            "id": student.id,
            "name": student.name,
            "major": student.major,
            "enrolledCourses": student.enrolled_courses,
            "completedCourses": student.completed_courses
        }

    def dict_to_student(self, data):
        student = Student(data["id"], data["name"], data["major"])
        student.enrolled_courses = data.get("enrolledCourses", [])
        student.completed_courses = data.get("completedCourses", [])
        return student

    def course_to_dict(self, course):
        return {
            "code": course.code,
            "title": course.title,
            "credits": course.credits,
            "capacity": course.capacity,
            "timeSlot": {
                "days": course.time_slot.days if course.time_slot else None,
                "startTime": course.time_slot.start_time if course.time_slot else None,
                "endTime": course.time_slot.end_time if course.time_slot else None
            } if course.time_slot else None,
            "prerequisites": course.prerequisites,
            "enrolledStudents": course.enrolled_students
        }

    def dict_to_course(self, data):
        time_slot_data = data.get("timeSlot")
        time_slot = TimeSlot(time_slot_data["days"], time_slot_data["startTime"], time_slot_data["endTime"]) if time_slot_data else None
        course = Course(data["code"], data["title"], data["credits"], data["capacity"], time_slot)
        course.prerequisites = data.get("prerequisites", [])
        course.enrolled_students = data.get("enrolledStudents", [])
        return course