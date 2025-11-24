from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI(title="User Auth API")

# ---------- DATABASE ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="zayan123",
        database="user_system"
    )

def create_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255)
        )
    """)
    db.commit()
    db.close()

create_table()

# ---------- MODELS ----------
class User(BaseModel):
    email: str
    password: str

class ResetPassword(BaseModel):
    email: str
    new_password: str

# ---------- ROUTES ----------
@app.post("/signup")
def signup(user: User):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    if cursor.fetchone():
        db.close()
        raise HTTPException(400, "Email already exists")

    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)",
                   (user.email, user.password))
    db.commit()
    db.close()

    return {"message": "Registration Successful!"}

@app.post("/login")
def login(user: User):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (user.email, user.password)
    )
    result = cursor.fetchone()
    db.close()

    if result:
        return {"message": "Login Successful"}
    else:
        raise HTTPException(401, "Invalid email or password")

@app.post("/reset_password")
def reset_password(data: ResetPassword):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE users SET password=%s WHERE email=%s",
        (data.new_password, data.email)
    )
    db.commit()
    db.close()

    return {"message": "Password reset successful!"}
