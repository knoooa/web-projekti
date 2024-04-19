from app import app
from flask import render_template, request, redirect, session, url_for
import users, messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    username = session.get("username")
    topics = messages.get_topics()
    return render_template("welcome.html", username=username, topics=topics)
    
@app.route("/topic/<topic_name>")
def topic_chats(topic_name):
    chats = messages.get_chats(topic_name)
    return render_template("topic_chats.html", chats=chats, topic_name=topic_name)

@app.route("/chat/<chat_name>")
def chat_messages(chat_name):
    msgs = messages.get_messages(chat_name)
    username = messages.get_username(chat_name)
    created_at = messages.created_at(chat_name)
    return render_template("chats.html", msgs=msgs, created_at=created_at, chat_name=chat_name, user_id=username)

@app.route("/chats")
def chats():
    list = messages.get_messages()
    return render_template("chats.html", count=len(list), messages=list)

@app.route("/create_chat", methods=["POST", "GET"])
def create_chat():
    chat_title = request.form['chat_title']
    topic_name = request.form['topic_name'] 
    topic_id = messages.get_topic_id(topic_name)
    user_id = users.user_id()
    messages.create_chat(chat_title, user_id, topic_id)
    return redirect(url_for('topic_chats', topic_name=topic_name))

@app.route("/my_messages")
def my_messages():
    msgs = messages.my_messages()
    return redirect(msgs=msgs)

#-------------------------------------------------

@app.route("/new_message")
def new():
    return render_template("new_message.html")

@app.route("/send", methods=["POST", "GET"])
def send():
    content = request.form["content"]
    chat_name = request.form["chat_name"]
    chat_id = messages.get_chat_id(chat_name)

    if messages.send_message(content, chat_id):
        return redirect(url_for('chat_messages', chat_name=chat_name))
    else:
        return render_template("error.html", message="Viestiä ei voitu lähettää, yritä uudelleen")

#-------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/welcome")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
        
        
@app.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        
        result = users.register(username, password1)
        if result == 2:
            return render_template("error.html", message="Tämä käyttäjänimi on jo käytössä")
        elif result:
            return redirect("/login")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

#-------------------------------------------