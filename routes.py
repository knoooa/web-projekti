from app import app
from flask import render_template, request, redirect, session
import users


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    username = session.get("username")
    return render_template("welcome.html", username=username)



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