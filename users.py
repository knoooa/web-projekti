#from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from db import db

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        #if user.password == password:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False
        

def logout():
    del session["user_id"]


def register(username, password):
    if len(username.strip())<=1 or len(password.strip())<=7:
        return 3
    hash_value = generate_password_hash(password)
    password = hash_value
    sql_check_username = text("SELECT COUNT(*) FROM users WHERE username = :username")
    result = db.session.execute(sql_check_username, {"username": username})
    username_in_use = result.fetchone()[0]
    
    if username_in_use > 0:
        return 2
    
    try:
        sql_register_user = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql_register_user, {"username": username, "password": password})
        db.session.commit()
    except:
        return False
    
    return True

def user_id():
    return session.get("user_id",0)