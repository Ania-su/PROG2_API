from fastapi import FastAPI, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response, HTMLResponse, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()
security = HTTPBasic()

@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return Response(content="pong", media_type="text/plain", status_code=200)


@app.get("/home", response_class=HTMLResponse)
async def home():
    html_content = "<html><body><h1>Welcome home!</h1></body></html>"
    return HTMLResponse(content=html_content, status_code=200)

posts = []

class Post(BaseModel):
    Author: str
    Title: str
    Content: str
    Creation_datetime: str

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def add_posts(new_posts: List[Post]):
    posts.extend(new_posts)
    return posts


@app.get("/posts")
async def get_posts():
    return posts

@app.put("/posts")
async def put_posts(post: Post):
    for i, existing in enumerate(posts):
        if existing.title == post.title:
            if existing != post:
                posts[i] = post
            return posts

    posts.append(post)
    return posts

@app.get("/ping/auth")
async def get_ping_authorized(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "123456")

    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return Response(content="pong", media_type="text/plain", status_code=200)
