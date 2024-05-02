CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT);

CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    admin_status INTEGER);

CREATE TABLE topic (
    id SERIAL PRIMARY KEY,
    topic_name TEXT UNIQUE);

CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users,
    topic_id INTEGER REFERENCES topic,
    created_at TIMESTAMP);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    chat_id INTEGER REFERENCES chats,
    sent_at TIMESTAMP);

