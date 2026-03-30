from Course import Course
from Student import Student
from TimeSlot import TimeSlot

class EnrollmentResult:
    def __init__(self, success, message):
        self.success = success
        self.message = message

    @staticmethod
    def success(message):
        return EnrollmentResult(True, message)

    @staticmethod
    def failure(message):
        return EnrollmentResult(False, message)

class EnrollmentSystem:
    TUITION_PER_CREDIT = 300.0

    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self, student):
        if student and student.id not in self.students:
            self.students[student.id] = student
            return True
        return False

    def get_student(self, student_id):
        return self.students.get(student_id)

    def update_student(self, student_id, new_name=None, new_major=None):
        student = self.students.get(student_id)
        if student:
            if new_name and new_name.strip():
                student.name = new_name
            if new_major and new_major.strip():
                student.major = new_major
            return True
        return False

    def get_all_students(self):
        return list(self.students.values())

    def add_course(self, course):
        if course and course.code not in self.courses:
            self.courses[course.code] = course
            return True
        return False

    def get_course(self, course_code):
        return self.courses.get(course_code)

    def update_course(self, course_code, new_title=None, new_credits=None, new_capacity=None):
        course = self.courses.get(course_code)
        if course:
            if new_title and new_title.strip():
                course.title = new_title
            if new_credits and new_credits > 0:
                course.credits = new_credits
            if new_capacity and new_capacity > 0:
                course.capacity = new_capacity
            return True
        return False

    def get_all_courses(self):
        return list(self.courses.values())

    def register_course(self, student_id, course_code):
        student = self.students.get(student_id)
        if not student:
            return EnrollmentResult.failure(f"Student not found: {student_id}")

        course = self.courses.get(course_code)
        if not course:
            return EnrollmentResult.failure(f"Course not found: {course_code}")

        if student.is_enrolled_in(course_code):
            return EnrollmentResult.failure(f"You are already enrolled in {course_code}.")

        if course.is_full():
            return EnrollmentResult.failure(f"Course {course_code} is full (capacity: {course.capacity}).")

        for prereq in course.prerequisites:
            if not student.has_completed(prereq):
                prereq_course = self.courses.get(prereq)
                prereq_title = prereq_course.title if prereq_course else prereq
                return EnrollmentResult.failure(
                    f"Prerequisite not met: you must complete '{prereq_title}' ({prereq}) "
                    f"before enrolling in {course_code}."
                )

        for enrolled_code in student.enrolled_courses:
            enrolled = self.courses.get(enrolled_code)
            if (enrolled and enrolled.time_slot and course.time_slot and
                enrolled.time_slot.overlaps(course.time_slot)):
                return EnrollmentResult.failure(
                    f"Schedule conflict: {course_code} ({course.time_slot}) overlaps with "
                    f"{enrolled_code} ({enrolled.time_slot})."
                )

        student.enroll_in(course_code)
        course.enroll_student(student_id)
        return EnrollmentResult.success(f"Successfully enrolled in {course_code} – {course.title}.")

    def drop_course(self, student_id, course_code):
        student = self.students.get(student_id)
        if not student:
            return EnrollmentResult.failure(f"Student not found: {student_id}")

        course = self.courses.get(course_code)
        if not course:
            return EnrollmentResult.failure(f"Course not found: {course_code}")

        if not student.is_enrolled_in(course_code):
            return EnrollmentResult.failure(f"You are not enrolled in {course_code}.")

        student.drop_course(course_code)
        course.remove_student(student_id)
        return EnrollmentResult.success(f"Successfully dropped {course_code} – {course.title}.")

    def get_student_schedule(self, student_id):
        student = self.students.get(student_id)
        if not student:
            return []
        schedule = []
        for code in student.enrolled_courses:
            course = self.courses.get(code)
            if course:
                schedule.append(course)
        return schedule

    def get_course_roster(self, course_code):
        course = self.courses.get(course_code)
        if not course:
            return []
        roster = []
        for sid in course.enrolled_students:
            student = self.students.get(sid)
            if student:
                roster.append(student)
        return roster

    def calculate_tuition(self, student_id):
        student = self.students.get(student_id)
        if not student:
            return -1.0
        total_credits = 0
        for code in student.enrolled_courses:
            course = self.courses.get(code)
            if course:
                total_credits += course.credits
        return total_credits * self.TUITION_PER_CREDIT