# Deployment Guide

The easiest and most cost-effective way to host this Flask application is using **Render** (free tier available) or **PythonAnywhere**.

## Option 1: Deploy to Render (Recommended)

1.  **Push your code to GitHub**:
    *   Create a new repository on GitHub.
    *   Push all the files in this folder to that repository.
    
2.  **Create a Render account**:
    *   Go to [render.com](https://render.com) and sign up/login.

3.  **Create a Web Service**:
    *   Click "New +" -> "Web Service".
    *   Connect your GitHub repository.
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app` (This is already in your `Procfile`, so Render might auto-detect it, but safe to specify).

4.  **Deploy**:
    *   Click "Create Web Service". Render will build your app and give you a live URL (e.g., `https://your-app-name.onrender.com`).

---

## Option 2: PythonAnywhere

1.  **Sign up**: Go to [pythonanywhere.com](https://www.pythonanywhere.com/).
2.  **Upload Code**:
    *   Use the "Files" tab to upload your zip file or clone your git repo via their "Consoles" tab (Bash).
3.  **Virtual Env**:
    *   Open a Bash console.
    *   Run: `mkvirtualenv --python=/usr/bin/python3.10 myenv`
    *   Run: `pip install -r requirements.txt`
4.  **Web App Config**:
    *   Go to "Web" tab.
    *   "Add a new web app" -> Select Flask -> Select Python 3.10.
    *   Edit the **WSGI configuration file** (link on the Web tab).
    *   Update the path to point to your `app.py`.

## Important Notes

*   **requirements.txt**: I have created this file for you. It contains `flask`, `flask-cors`, and `gunicorn`.
*   **Procfile**: I have created this file. It tells cloud platforms how to start your app (`gunicorn app:app`).
