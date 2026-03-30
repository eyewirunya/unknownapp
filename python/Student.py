class Student:
    def __init__(self, student_id=None, name=None, major=None):
        self.id = student_id
        self.name = name
        self.major = major
        self.enrolled_courses = []
        self.completed_courses = []

    def is_enrolled_in(self, course_code):
        return course_code in self.enrolled_courses

    def has_completed(self, course_code):
        return course_code in self.completed_courses

    def enroll_in(self, course_code):
        if not self.is_enrolled_in(course_code):
            self.enrolled_courses.append(course_code)
            return True
        return False

    def drop_course(self, course_code):
        if course_code in self.enrolled_courses:
            self.enrolled_courses.remove(course_code)
            return True
        return False

    def __str__(self):
        return f"ID: {self.id:<12}  Name: {self.name:<25}  Major: {self.major}"