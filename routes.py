from app import app
from flask import render_template, request, redirect, session
import users, messages


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    username = session.get("username")
    return render_template("welcome.html", username=username)

@app.route("/chats")
def chats():
    list = messages.get_messages()
    return render_template("chats.html", count=len(list), messages=list)

@app.route("/new_message")
def new():
    return render_template("new_message.html")

@app.route("/send", methods=["POST", "GET"])
def send():
    content = request.form["content"]
    if messages.send_message(content):
        return redirect("/chats")
    else:
        return render_template("error.html", message="Viestiä ei voitu lähettää, yritä uudelleen")



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