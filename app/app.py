from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import create_db_and_tables, get_async_session, Post
from app.imagekit import imagekit

import shutil
import tempfile
import os

from fastapi import Path
import uuid



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# ---------------- UPLOAD ----------------

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    temp_path = None

    try:
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_path = tmp.name

        result = imagekit.upload_file(
            file=open(temp_path, "rb"),
            file_name=file.filename
        )

        if not result or not result.url:
            raise HTTPException(status_code=500, detail="ImageKit upload failed")

        post = Post(
            caption=caption,
            url=result.url,
            file_type="video" if file.content_type.startswith("video") else "image",
            file_name=result.name
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
            "created_at": post.created_at.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        file.file.close()


# ---------------- FEED ----------------

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Post).order_by(Post.created_at.desc())
    )

    posts = result.scalars().all()

    return {
        "posts": [
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
    }

@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        result = await session.execute(
            select(Post).where(Post.id == post_id)
        )

        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
