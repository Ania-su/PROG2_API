from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
def hello():
    print("Hello World")
