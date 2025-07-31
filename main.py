from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()

@app.get('/hello')
def get_hello( name : str ):
    return JSONResponse({"message" : f"Hello {name}"}, status_code=200)
