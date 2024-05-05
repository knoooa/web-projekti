from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from db import db
import secrets

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["csrf_token"] = secrets.token_hex(16)
            session["user_id"] = user.id
            return True
        else:
            return False
        

def logout():
    del session["user_id"]


def register(username, password):
    if not (1 < len(username.strip()) <= 15) or not (3 <= len(password.strip()) <= 20):
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

def check_old_password(old_password):
    id = user_id()
    sql = text("SELECT password FROM users WHERE id=:id")
    result = db.session.execute(sql, {"id": id})
    user = result.fetchone()

    if check_password_hash(user.password,old_password):
        return True
    else:
        return False

def change_password(new_password):
    userid = user_id()
    hash_value = generate_password_hash(new_password)
    new_password = hash_value
    sql = text("UPDATE users SET password = :new_password WHERE id = :userid")
    res = db.session.execute(sql, {"new_password":new_password, "userid":userid})
    db.session.commit()
    if res.rowcount>0:
        return True
    return False
                

def delete_user(userid):
        sql = text("DELETE FROM messages WHERE user_id = :userid") 
        db.session.execute(sql, {"userid": userid})

        sql2 = text("DELETE FROM chats WHERE user_id = :userid")
        db.session.execute(sql2, {"userid": userid})

        sql3 = text("DELETE FROM admin WHERE user_id = :userid")
        db.session.execute(sql3, {"userid":userid})

        sql4 = text("DELETE FROM users WHERE id = :userid")
        db.session.execute(sql4, {"userid": userid})

        db.session.commit()


def admin_status(user_id):
    sql = text("SELECT admin_status FROM admin WHERE user_id=:user_id")
    res = db.session.execute(sql, {"user_id":user_id}).fetchone()
    if res:
        return 1
    else:
        return 0
