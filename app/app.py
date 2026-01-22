from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import create_db_and_tables, get_async_session, Post

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


# ---------------- UPLOAD POST ----------------

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="dummy_url",
        file_type=file.content_type,
        file_name=file.filename
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)

    return {
        "id": post.id,
        "caption": post.caption,
        "url": post.url,
        "file_type": post.file_type,
        "file_name": post.file_name,
        "created_at": post.created_at
    }


# ---------------- GET FEED ----------------

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Post).order_by(Post.created_at.desc())
    )

    posts = result.scalars().all()

    posts_data = [
        {
            "id": post.id,
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
        }
        for post in posts
    ]

    return {"posts": posts_data}
