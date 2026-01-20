from fastapi import FastAPI,HTTPException

app = FastAPI()
# this API is designed to handle data; accepting requests from the frontend or client and returning responses

# endpoint
text_posts = {1:{"title":"New Post","content":"cool test post"}}

@app.get("/posts")
def get_all_posts():
    return text_posts

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404,detail="Post not found")
    return text_posts.get(id)
