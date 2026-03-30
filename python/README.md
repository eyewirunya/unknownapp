# Python Version of Course Enrollment System

This is a Python implementation of the "Register for Course" use case from the Java Course Enrollment System.

## Files

- `TimeSlot.py`: Represents a scheduled time slot for a course
- `Course.py`: Represents a course in the catalog
- `Student.py`: Represents a student
- `EnrollmentSystem.py`: Core business logic for enrollment
- `DataManager.py`: Handles loading and saving data to JSON files
- `register_course.py`: Main script demonstrating the register course functionality

## How to Run

```bash
python3 register_course.py
```

The script will:
1. Load existing data or seed default data
2. Display available students
3. Prompt for a student ID
4. Display available courses
5. Prompt for a course code to register
6. Attempt to register the student for the course
7. Save the updated data

## Features Implemented

- Course registration with validation
- Prerequisite checking
- Time conflict detection
- Capacity limits
- Data persistence with JSON