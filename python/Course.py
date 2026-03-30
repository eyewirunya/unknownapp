from TimeSlot import TimeSlot

class Course:
    def __init__(self, code=None, title=None, credits=3, capacity=30, time_slot=None):
        self.code = code
        self.title = title
        self.credits = credits
        self.capacity = capacity
        self.time_slot = time_slot
        self.prerequisites = []
        self.enrolled_students = []

    def get_enrollment_count(self):
        return len(self.enrolled_students)

    def is_full(self):
        return len(self.enrolled_students) >= self.capacity

    def get_available_seats(self):
        return max(0, self.capacity - len(self.enrolled_students))

    def has_student(self, student_id):
        return student_id in self.enrolled_students

    def enroll_student(self, student_id):
        if self.is_full() or self.has_student(student_id):
            return False
        self.enrolled_students.append(student_id)
        return True

    def remove_student(self, student_id):
        if student_id in self.enrolled_students:
            self.enrolled_students.remove(student_id)
            return True
        return False

    def __str__(self):
        prereq_str = "None" if not self.prerequisites else ", ".join(self.prerequisites)
        time_str = str(self.time_slot) if self.time_slot else "TBA"
        return (f"{self.code:<10} {self.title:<40} Credits: {self.credits}  "
                f"Capacity: {len(self.enrolled_students)}/{self.capacity}  "
                f"Time: {time_str:<18}  Prerequisites: {prereq_str}")