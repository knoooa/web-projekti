from db import db
import users
from sqlalchemy import text

def get_messages():
    sql = text("SELECT M.content, U.username, m.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id")
    results = db.session.execute(sql)
    return results.fetchall()
    
def send_message(content):
    user_id = users.user_id()
    
    if user_id == 0:
        return False
    
    sql = text("INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True

