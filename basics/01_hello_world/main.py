from fastapi import FastAPI
import json

app = FastAPI() #this creates an instance of the FastAPI class, which is the main entry point for creating a FastAPI application.

@app.get("/") #this is a route decorator that tells FastAPI that the function below is to be used for the GET method on the root path ("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return{"message": "This is a simple FastAPI application that returns a greeting message."}

def load_data():
    with open('myresume.json') as f:
        data = json.load(f)
        
    return data

@app.get("/myresume")
def myresume():
    data = load_data()
    
    return data

#To run the application, you would typically use a command like `uvicorn main:app --reload` in the terminal, where `main` is the name of the Python file (without the .py extension) and `app` is the instance of the FastAPI class.