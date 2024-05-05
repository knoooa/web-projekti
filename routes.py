from app import app
from flask import render_template, request, redirect, session, url_for, abort, flash
import users, messages, secrets

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    username = session.get("username")
    topics = messages.get_topics()
    admin_status = users.admin_status(users.user_id())
    return render_template("welcome.html", username=username, adminstatus=admin_status, topics=topics, get_count=messages.get_title_count)
    
@app.route("/topic/<topic_name>")
def topic_chats(topic_name):
    chats = messages.get_chats(topic_name)
    adminstatus = users.admin_status(users.user_id())
    return render_template("topic_chats.html", chats=chats, topic_name=topic_name, get_count=messages.get_count, created_at=messages.created_at, adminstatus=adminstatus, get_username=messages.get_username)

@app.route("/chat/<chat_name>")
def chat_messages(chat_name):
    msgs = messages.get_messages(chat_name)
    username = messages.get_username(chat_name)
    created_at = messages.created_at(chat_name)
    adminstatus = users.admin_status(users.user_id())
    return render_template("chats.html", msgs=msgs, created_at=created_at, chat_name=chat_name, username=username, user_id=users.user_id(), adminstatus=adminstatus)

@app.route("/create_chat", methods=["POST", "GET"])
def create_chat():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    chat_title = request.form['chat_title']
    topic_name = request.form['topic_name'] 
    topic_id = messages.get_topic_id(topic_name)
    user_id = users.user_id()

    if messages.create_chat(chat_title, user_id, topic_id):
        return redirect(url_for("topic_chats", topic_name=topic_name))
    else:
        flash("Keskustelua ei voitu aloittaa, koska samanlainen keskustelu on jo olemassa :-(")
        return redirect(url_for("topic_chats", topic_name=topic_name))

@app.route("/my_messages")
def my_messages():
    msgs = messages.my_messages()
    return render_template("my_messages.html", msgs=msgs, get_chat_name=messages.get_chat_name)

@app.route("/profile")
def profile():
    username = session.get("username")
    return render_template("profile.html", username=username)

@app.route("/remove_account")
def remove_account():
    return render_template("remove_account.html", username=session.get("username"), userid=users.user_id())

@app.route("/delete_user")
def delete_user():
    userid = users.user_id()
    try:
        delete = users.delete_user(userid)
        if delete == False:
            flash("Käyttäjän poistaminen ei onnistunut, yritä uudelleen")
            return redirect(url_for("profile"))
        else:
            return render_template("index.html", message="Käyttäjä poistettiin onnistuneesti")
    except Exception as e:
        flash("Virhe poistaessa käyttäjää: {}".format(str(e)))
    return render_template("index.html")

@app.route("/change_password", methods=["POST", "GET"])
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")
    else:
        old = request.form["old"]
        new_password = request.form["new1"]
        new_password2 = request.form["new2"]

        if new_password != new_password2:
            flash("Salasanat eivät täsmää")
            return redirect(url_for("change_password"))
        elif not users.check_old_password(old):
            flash("Vanha salasana on väärin")
            return redirect(url_for("change_password"))
        
        result = users.change_password(new_password)
        if result:
            return render_template("index.html", message="Salasana vaihdettiin onnistuneesti")
        else:
            flash("Virhe")
            return redirect(url_for("change_password"))
        
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        results = messages.search(search_query)
        return render_template('found.html', ids=results, get_content=messages.get_content, get_chat=messages.get_chat_name)
    else:
        return render_template('search.html')
    
@app.route("/create_topic", methods=["POST"])
def create_topic():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    topic_name = request.form["topic_name"]
    create = messages.create_topic(topic_name)
    if create:
        return redirect(url_for("welcome"))
    else:
        flash("Tämän niminen aihe on jo olemassa")
        return redirect(url_for("welcome"))
    
#----------------------------------------------
    
@app.route("/delete_topic/<topic_name>", methods=["GET", "POST"])
def delete_topic(topic_name):
    delete = messages.delete_topic(topic_name)
    if delete:
        return redirect(url_for("welcome"))
    else:
        return render_template("error.html", message="virhe")

@app.route("/delete_chat/<topic_name>/<chat_name>", methods=["GET", "POST"])
def delete_chat(chat_name, topic_name):
    delete = messages.delete_chat(chat_name)
    if delete:
        return redirect(url_for("topic_chats", topic_name=topic_name))
    else:
        return render_template("error.html", message="virhe")

@app.route("/delete_message/<chat_name>/<message_id>", methods=["GET", "POST"])
def delete_message(chat_name, message_id):
    delete = messages.delete_message(message_id)
    if delete:
        return redirect(url_for("chat_messages", chat_name=chat_name))
    else:
        return render_template("error.html", message="virhe")
    

#----------------------------------------------------------

@app.route("/new_message")
def new():
    return render_template("new_message.html")

@app.route("/send", methods=["POST", "GET"])
def send():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    chat_name = request.form["chat_name"]
    chat_id = messages.get_chat_id(chat_name)

    if messages.send_message(content, chat_id):
        return redirect(url_for('chat_messages', chat_name=chat_name))
    else:
        flash("Viestiä ei voitu lähettää, yritä uudelleen")
        return redirect(url_for('chat_messages', chat_name=chat_name))

#-----------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            return render_template("index.html", message="Väärä tunnus tai salasana")
        
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
            return render_template("register.html", message="Salasanat eivät täsmää")
        
        result = users.register(username, password1)
        if result == 3:
            return render_template("register.html", message="Käyttäjänimen tulee olla vähintään 2 ja salasanan 4 merkkiä")
        elif result == 2:
            return render_template("register.html", message="Tämä käyttäjänimi on jo käytössä")
        elif result:
            flash("Käyttäjä luotiin onnistuneesti. Kirjaudu sisään.")
            return redirect("/login") 
        else:
            return render_template("register.html", message="Rekisteröinti ei onnistunut")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
