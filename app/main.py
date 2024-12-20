from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

posts = [
    {
        "title": "title1", 
        "content": "content1", 
        "id": 1,
        "published": True,
        "rating": None
    },
    {
        "title": "title2", 
        "content": "content2", 
        "id": 2, 
        "published": False,
        "rating": None
    }
]

def findPost(post_id: int):
    try:
        return [ post for post in posts if post['id'] == post_id ][0] 
    except Exception as exc:
        return None

def create_app() -> FastAPI:
    app = FastAPI()
    
    @app.get("/")
    def hello():
        return {
            "message": "Hello World!"
        }

    @app.post("/posts", status_code=status.HTTP_201_CREATED)
    def createPost(post: Post):
        post_dict = post.model_dump()
        post_dict['id'] = randrange(1,10000)
        posts.append(post_dict)
        return {"data": post_dict }

    @app.get("/posts")
    def getPosts():
        return {
            "data": posts
        }

    @app.get("/posts/{post_id}")
    def getPost(post_id: int):
        post = findPost(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} doesn't exist")
        return {
            "data": post
        }

    @app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
    def deletePost(post_id: int):
        post = findPost(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} doesn't exist")
        posts.remove(post)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.put("/posts/{post_id}")
    def updatePost(post_id: int, post: Post):
        try:
            new_post = post.dict()
            new_post['id'] = post_id
            old_post = findPost(post_id)
            posts[posts.index(old_post)] = new_post
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} doesn't exist") from exc
        return {
            "data": post
        }

    return app

app = create_app()
