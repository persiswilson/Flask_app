# FLASK BLOG APPLICATION
---
## A simple **monolithic Flask web application** with user authentication, posts, comments, and notifications.  
This project demonstrates **full-stack development** with Flask, SQLite, SQLAlchemy, Jinja2 templates, Bootstrap, and Toastr.
---
# Features
- **User Authentication**
  - Signup, Login, Logout with secure password hashing
  - JWT authentication for protected routes
- **Post Management**
  - Create, view, edit, and delete posts
  - Authorization: only post owners can edit/delete
- **Comment System**
  - Add comments to posts  
  - Cascade delete (removes comments if post is deleted)
- **UI & Notifications**
  - Bootstrap for styling  
  - Toastr for success/error notifications
---
## Technologies Used  
### Backend  
- **Flask** – Web framework for Python  
- **Flask-Login** – User authentication and session management  
- **Flask-JWT-Extended** – JWT-based authentication for APIs  
- **SQLAlchemy** – ORM for database interaction  
- **SQLite** – Lightweight relational database  

### Frontend  
- **Jinja2** – Templating engine for dynamic HTML  
- **Bootstrap** – Styling and responsive UI  
- **Toastr.js** – Popup notifications for user feedback  

### Others  
- **Werkzeug** – Secure password hashing  
- **Python 3.x** – Programming language  
- **HTML, CSS, JavaScript** – Core web technologies
## Project Structure
flask_app/
- app.py # Main Flask app
- models.py # Database models (User, Post, Comment)
- templates/ # HTML Templates
  - base.html
  - login.html
  - signup.html
  - posts.html
  - create_post.html
  - edit_post.html
- static/ # CSS, JS (Bootstrap, Toastr)
- requirements.txt # Dependencies
## Installation and setup
### 1. Create virtual environment and activate
     python -m venv venv
     source venv/bin/activate   # macOS/Linux
     venv\Scripts\activate      # Windows
### 2. Install dependencies
     pip install -r requirements.txt
### 3. Run the app
     python app.py

    
