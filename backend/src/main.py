from fastapi import FastAPI
import os

app = FastAPI()

API_KEY = os.environ.get('API_KEY')
MY_PROJECT = os.environ.get('MY_PROJECT') or "This is my project"

if not API_KEY:
    raise NotImplementedError('API KEY not set')

@app.get("/")
def read_index():
    return {'hello': "Hello World", "project_name": MY_PROJECT}