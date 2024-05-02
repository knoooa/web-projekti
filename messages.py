from db import db
import users
from sqlalchemy import text

def get_messages(chat_name):
    sql = text("SELECT M.content, U.username, M.sent_at, M.id FROM messages M JOIN users U ON M.user_id = U.id \
               WHERE M.chat_id = (SELECT id FROM chats WHERE title = :chat_name) ORDER BY M.id")
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
    sql = text("SELECT topic_name FROM topic ORDER BY topic_name")
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

def get_count(chat_name):
    chat_id = get_chat_id(chat_name)
    sql = text("SELECT COUNT(id) FROM messages WHERE chat_id = :chat_id")
    res = db.session.execute(sql, {"chat_id": chat_id}).fetchone()
    if res:
        return res[0]
    return 0

def get_title_count(topic_name):
    topic_id = get_topic_id(topic_name)
    sql = text("SELECT COUNT(id) FROM chats WHERE topic_id = :topic_id")
    res = db.session.execute(sql, {"topic_id": topic_id}).fetchone()
    if res:
        return res[0]
    return 0

def search(word):
    sql = text("SELECT id FROM messages WHERE content LIKE :word")
    res = db.session.execute(sql, {"word":f'%{word}%'}).fetchall()
    if res or res!=None:
        return res
    else:
        return "Ei viestejä"

def get_content(id):
    sql = text("SELECT * FROM messages WHERE id=:id")
    res = db.session.execute(sql, {"id":id[0]}).fetchone()
    return res
    
def create_topic(topic_name):
    topic_name = topic_name[0].capitalize() + topic_name[1:].lower()
    if len(topic_name) <= 20 and len(topic_name.strip()) > 0:
        try:
            sql = text("INSERT INTO topic (topic_name) VALUES (:topic_name)")
            db.session.execute(sql, {"topic_name": topic_name})
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
    return False

def delete_topic(topic_name):
    try:
        sql = text("DELETE FROM topic WHERE topic_name=:topic_name")
        db.session.execute(sql, {"topic_name":topic_name})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
    
def delete_chat(chat_name):
    try:
        sql = text("DELETE FROM chats WHERE title=:chat_name")
        db.session.execute(sql, {"title":chat_name})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
    
def delete_message(message_id):
    try:
        sql = text("DELETE FROM messages WHERE id=:id")
        db.session.execute(sql, {"id":int(message_id)})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False