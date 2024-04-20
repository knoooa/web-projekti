from db import db
import users
from sqlalchemy import text

def get_messages(chat_name):
    sql = text("SELECT M.content, U.username, M.sent_at FROM messages M JOIN users U ON M.user_id = U.id WHERE M.chat_id = (SELECT id FROM chats WHERE title = :chat_name) ORDER BY M.id")
    results = db.session.execute(sql, {"chat_name": chat_name})
    return results.fetchall()

def send_message(content, chat_id):
    user_id = users.user_id()
    if content=="" or content.strip()=="":
        return False
    if user_id == 0:
        return False
    
    sql = text("INSERT INTO messages (content, user_id, chat_id, sent_at) VALUES (:content, :user_id, :chat_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id, "chat_id":chat_id})
    db.session.commit()
    return True

def get_topics():
    sql = text("SELECT topic_name FROM topic")
    results = db.session.execute(sql)
    return results.fetchall()

def get_chats(topic_name):
    sql = text("SELECT title FROM chats WHERE topic_id = (SELECT id FROM topic WHERE topic_name = :topic_name)")
    res = db.session.execute(sql, {"topic_name": topic_name})
    return res.fetchall()

def get_chat_id(chat_name):
    sql = text("SELECT id FROM chats WHERE title = :chat_name")
    result = db.session.execute(sql, {"chat_name": chat_name})
    chat_id = result.scalar()
    return chat_id

def get_topic_id(topic_name):
    sql = text("SELECT id FROM topic WHERE topic_name = :topic_name")
    result = db.session.execute(sql, {"topic_name": topic_name}).fetchone()
    return result[0]
    
def create_chat(title, user_id, topic_id):
    if len(title.strip())<3:
        return False
    sql = text("SELECT title FROM chats")
    result = db.session.execute(sql).fetchall()
    for row in result:
        if title == row[0]:
            return False
    
    sql = text("INSERT INTO chats (title, user_id, topic_id, created_at) VALUES(:title, :user_id, :topic_id, NOW())")
    db.session.execute(sql, {"title":title, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    return True

def get_username(chat_name):
    sql = text("SELECT username FROM users WHERE id = (SELECT user_id FROM chats WHERE title = :chat_name)")
    result = db.session.execute(sql, {"chat_name": chat_name}).fetchone()
    if result:
        return result[0]
    else:
        return None

def created_at(chat_name):
    chat_id = get_chat_id(chat_name)
    sql = text("SELECT chats.created_at FROM chats WHERE title=:chat_name AND id=:chat_id")
    result = db.session.execute(sql, {"chat_name":chat_name, "chat_id":chat_id}).fetchone()
    return result[0]
    
def my_messages():
    user_id = users.user_id()
    sql = text("SELECT content, chat_id, sent_at FROM messages WHERE user_id=:user_id ORDER BY sent_at DESC")
    result = db.session.execute(sql, {"user_id":user_id}).fetchall()
    return result

def get_chat_name(chat_id):
    sql = text("SELECT title FROM chats WHERE id=:chat_id")
    result = db.session.execute(sql, {"chat_id":chat_id}).fetchone()
    return result[0]