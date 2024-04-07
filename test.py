from db import db
import users
from sqlalchemy import text

def test():
    sql1 = text("INSERT INTO topic (id, topic_name) VALUES (1, 'Yleinen')")
    sql2 = text("INSERT INTO topic (id, topic_name) VALUES (2, 'Opiskelu')")
    sql3 = text("INSERT INTO topic (id, topic_name) VALUES (3, 'Matkustus')")
    sql4 = text("INSERT INTO topic (id, topic_name) VALUES (4, 'Lemmikit')")
    all = [sql1, sql2, sql3, sql4]
    for sql in all:
        db.session.execute(sql)