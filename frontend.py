import streamlit as st
import requests
import base64
import urllib.parse

# ---------------- CONFIG ----------------
st.set_page_config(page_title="GramX", layout="wide")
st.success("✅ Streamlit frontend loaded")

BASE_URL = "http://127.0.0.1:8001"

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- HELPERS ----------------
def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=10, **kwargs)
    except requests.exceptions.RequestException as e:
        st.error("🚨 Backend not reachable. Make sure FastAPI is running.")
        st.code(str(e))
        st.stop()


# ---------------- LOGIN ----------------
def login_page():
    st.title("🚀 Welcome to Simple Social")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if email and password:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login", type="primary", use_container_width=True):
                response = safe_request(
                    "post",
                    f"{BASE_URL}/auth/jwt/login",
                    data={"username": email, "password": password},
                )

                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]

                    user_response = safe_request(
                        "get", f"{BASE_URL}/users/me", headers=get_headers()
                    )

                    if user_response.status_code == 200:
                        st.session_state.user = user_response.json()
                        st.rerun()
                    else:
                        st.error("Failed to fetch user info")

                else:
                    st.error("Invalid email or password")

        with col2:
            if st.button("Sign Up", use_container_width=True):
                response = safe_request(
                    "post",
                    f"{BASE_URL}/auth/register",
                    json={"email": email, "password": password},
                )

                if response.status_code == 201:
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Registration failed")

    else:
        st.info("Enter your email and password above")


# ---------------- UPLOAD ----------------
def upload_page():
    st.title("📸 Share Something")

    uploaded_file = st.file_uploader(
        "Choose media",
        type=["png", "jpg", "jpeg", "mp4", "avi", "mov", "mkv", "webm"],
    )
    caption = st.text_area("Caption", placeholder="What's on your mind?")

    if uploaded_file and st.button("Share", type="primary"):
        with st.spinner("Uploading..."):
            response = safe_request(
                "post",
                f"{BASE_URL}/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                },
                data={"caption": caption},
                headers=get_headers(),
            )

            if response.status_code == 200:
                st.success("Post uploaded successfully!")
                st.rerun()
            else:
                st.error("Upload failed")


# ---------------- IMAGE TRANSFORM ----------------
def encode_text_for_overlay(text):
    return urllib.parse.quote(
        base64.b64encode(text.encode("utf-8")).decode("utf-8")
    ) if text else ""


def create_transformed_url(original_url, caption=None):
    if not caption:
        return original_url

    encoded = encode_text_for_overlay(caption)
    overlay = f"l-text,ie-{encoded},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"

    parts = original_url.split("/")
    return f"{'/'.join(parts[:4])}/tr:{overlay}/{'/'.join(parts[4:])}"


# ---------------- FEED ----------------
def feed_page():
    st.title("🏠 Feed")

    response = safe_request("get", f"{BASE_URL}/feed", headers=get_headers())

    if response.status_code != 200:
        st.error("Failed to load feed")
        return

    posts = response.json().get("posts", [])

    if not posts:
        st.info("No posts yet. Be the first to share something!")
        return

    for post in posts:
        st.markdown("---")

        # ✅ CORRECT EMAIL DISPLAY
        uploader_email = post.get("email") or "Unknown User"

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**{uploader_email}** • {post['created_at'][:10]}")

        with col2:
            if post.get("is_owner"):
                if st.button("🗑️", key=f"del_{post['id']}"):
                    safe_request(
                        "delete",
                        f"{BASE_URL}/posts/{post['id']}",
                        headers=get_headers(),
                    )
                    st.rerun()

        caption = post.get("caption", "")
        media_url = post.get("url", "")

        # ---------- CRASH PROTECTION ----------
        if not media_url or media_url == "dummy_url":
            st.warning("⚠️ Media unavailable for this post")
            continue

        # ---------- IMAGE ----------
        if post["file_type"] == "image":
            st.image(create_transformed_url(media_url, caption), width=300)

        # ---------- VIDEO ----------
        else:
            st.video(media_url)
            if caption:
                st.caption(caption)


# ---------------- MAIN ROUTER ----------------
if st.session_state.user is None:
    login_page()
else:
    st.sidebar.title(f"👋 Hi {st.session_state.user['email']}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    page = st.sidebar.radio("Navigate", ["🏠 Feed", "📸 Upload"])

    if page == "🏠 Feed":
        feed_page()
    else:
        upload_page()

#to run frontend - streamlit : streamlit run frontend.py
