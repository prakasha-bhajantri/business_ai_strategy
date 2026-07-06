from fastapi import FastAPI
from pydantic import BaseModel

user = FastAPI()

class Student(BaseModel):
    name:str
    age:int
    course: str

@user.get("/")
def home():
    return {
        "message": "Welcome to AI Dev"
    }

@user.get("/student")
def get_student_():
    return {
        "name": "A",
        "course": "Business Mgt",
        "completed": False
    }

@user.get("/student/{student_id}")
def get_student(student_id):
    return {
        "student_id": student_id,
        "name": "B",
        "course": "AI"
    }


@user.get("/search")
def search(name):
    return {
        "search": name
    }

@user.get("/course")
def course(topic, duration):
    return {
        "topic": topic,
        "duration": duration
    }

@user.post("/student")
def create_student(student:Student):
    return {
        "message": "Student is created",
        "student": student
    }