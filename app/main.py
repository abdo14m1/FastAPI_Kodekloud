from fastapi import FastAPI, Response, status, HTTPException
from .database import Database
from .models import Post
from .config import get_settings

settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
)

db = Database()
cur = db.get_cursor()


@app.get("/")
def hello():
    return {"message": "Hello World!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    return {"data": db.create_post(post.model_dump())}


@app.get("/posts")
def getPosts():
    posts = db.get_posts()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found"
        )
    return {"data": posts}


@app.get("/posts/{post_id}")
def getPost(post_id: int):
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(post_id: int):
    if not db.delete_post(post_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def updatePost(post_id: int, post_updated: Post):
    post = db.update_post(post_id, post_updated.model_dump())
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    return {"data": post}
