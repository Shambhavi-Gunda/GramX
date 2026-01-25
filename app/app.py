from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db import create_db_and_tables, get_async_session, Post
from app.imagekit import imagekit
from app.schemas import UserRead, UserCreate, UserUpdate
import shutil
import tempfile
import os
from app.users import auth_backend, current_active_user, fastapi_users
from fastapi.middleware.cors import CORSMiddleware
from app.db import User 


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- AUTH ROUTERS ----------------

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])


# ---------------- UPLOAD ----------------

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_active_user)
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
            user_id=user.id,
            caption=caption,
            url=result.url,
            file_type="video" if file.content_type.startswith("video") else "image",
            file_name=result.name,
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

    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
        file.file.close()


# ---------------- FEED ----------------

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_active_user)
):
    result = await session.execute(
        select(Post)
        .options(selectinload(Post.user))
        .order_by(Post.created_at.desc())
    )

    posts = result.scalars().all()

    return {
        "posts": [
            {
                "id": post.id,
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": post.user.email if post.user else None
            }
            for post in posts
        ]
    }


# ---------------- DELETE ----------------

@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_active_user)
):
    result = await session.execute(
        select(Post).where(Post.id == post_id)
    )

    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    await session.delete(post)
    await session.commit()

    return {"success": True, "message": "Post deleted successfully"}

#to run backend: uvicorn app.app:app --host 127.0.0.1 --port 8001 --reload