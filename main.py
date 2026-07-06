from fastapi import FastAPI
from utilities import parse_first_two_letters_from_name

app = FastAPI()

@app.post("/student")
def create_student(name):
    
    parsed_name = parse_first_two_letters_from_name(name)

    return {
        "Name": name,
        "Parsed Name": parsed_name
    }