from flask import render_template, redirect, request, session, make_response
from Server import app, User, db
from json import loads, dumps


@app.route('/')
def index():
    file = open("Server/data/products.json")

    if session.get("user"):
        if session.get("admin"):
            return render_template("index.html", user = session["user"], data=loads(file.read()), admin=True)
        return render_template("index.html", user = session["user"], data=loads(file.read()), admin=False)
    
    return render_template('index.html', user=False, data=loads(file.read()), admin=False)


@app.route('/login')
def login():
    error = request.cookies.get('userID')
    if error == None:
        return render_template('login.html', error = False)
    return render_template('login', error=str(error))


@app.route('/signup')
def signin():
    return render_template('signup.html')


@app.route('/login/check', methods=["POST"])
def login_check():
    try:
        user = request.form["username"]
        password = request.form["pass"]
        data = User.query.get(user)

        if user == data.user:
            if password == data.password:
                session["user"] = user
                if data.admin == 1:
                    session["admin"] = 1
                else:
                    session["admin"] = 0
                return redirect("/")
        return "error"
    except Exception as er:
        return str(er)

@app.route('/signup/check', methods=["POST"])
def sign_in_check():
    try:
        user = request.form["username"]
        password = request.form["pass"]
        if user == "" or password == "":
            pass
        db.session.add(User(user=user, password=password))
        db.session.commit()
        session["user"] = user
        
        return redirect('/')
    except Exception:
        return "Error"

@app.route('/insert')
def insert():
    if session["admin"] == 1:
        file = open('Server/data/num.tmp', 'r')
        id = int(file.read()) + 1 
        file = open('Server/data/num.tmp', 'w')
        file.write(str(id))
        return render_template("insert.html", data = False, id = id)
    return "You do not have access to this section"

@app.route('/insert/<id>')
def insert_id(id):
    if session["admin"] == 1:
        try:
            file = open("Server/data/products.json", "r")
            data = loads(file.read())

            return render_template("insert.html", data = data[str(id)], id = id)
        except Exception as er:
            return str(er)
    return "You do not have access to this section"

@app.route('/insert/operation', methods=["POST"])
def operation():
    if session["admin"] == 1:
        file = open("Server/data/products.json", 'r')
        data = loads(file.read())
        file = open("Server/data/products.json", 'w')
        try:
            id = request.form["id"]
            name = request.form["name"]
            title = request.form["title"]
            info = request.form["info"]
            precio = request.form["precio"]
            
            data[str(id)] = {
                "name":name,
                "title":title,
                "info":info,
                "precio":precio
                }
            file.write(dumps(data))
            return redirect('/')
        except Exception:
            return "error"
    return "You do not have access to this section "
    

@app.route('/delete/<id>',)
def delete(id):
    try:
        if session["admin"] == 1:
            file = open("Server/data/products.json", 'r')
            data:dict = loads(file.read())
            file = open("Server/data/products.json", 'w')
            data.pop(id)
            file.write(dumps(data))
            return redirect('/')
        return "You do not have access to this section "
    except Exception:
        return "error"