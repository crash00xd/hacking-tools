from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configure o banco ANTES de inicializar o SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    author = db.Column(db.String())

    # Formata qualquer objeto do post em dicionário
    def to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)

        return result


# Rota vulnerável para testes - http://127.0.0.1:5000/test?nome=payload
@app.route("/test")
def test():
    nome = request.args.get("nome")
    return "Hello {}".format(nome)


# Rota vulnerável para testes com cookies configurados - http://127.0.0.1:5000/test2?nome=payload
@app.route("/test2")
def test2():
    nome = request.args.get("nome")
    response = make_response("Hello {}".format(nome))
    response.set_cookie("info", "session")
    return response


# Busca todos os posts no banco e dados e mostra na página /index.html
@app.route("/")
def home():
    #nome = request.args.get("nome")
    #return render_template("index.html", nome=nome)
    posts = Post.query.all()
    assert isinstance(posts, object)
    return render_template("index.html", posts=posts)


# Adiciona o post no banco de dados
@app.route("/post/add", methods=["GET","POST"])
def add_post():
    try:
        form = request.form
        post = Post(title=form["title"], content=form["content"], author=form["author"])
        db.session.add(post)
        db.session.commit()
    except Exception as error:
        app.logger.error(error)
        print("Error: ", error)

    return redirect(url_for("home"))


# Deleta o post no banco de dados
@app.route("/post/<int:id>/del", methods=["GET","POST"])
def delete_post(id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
    except Exception as error:
        app.logger.error(error)
        print("Error: ", error)

    return redirect(url_for("home"))


# Editar o post no banco de dados
@app.route("/post/<int:id>/edit", methods=["GET","POST"])
def edit_post(id):
    if request.method == "POST":
        try:
            post = Post.query.get(id)
            form = request.form
            post.title = form["title"]
            post.content = form["content"]
            post.author = form["author"]
            db.session.commit()
        except Exception as error:
            app.logger.error(error)
            print("Error: ", error)

        return redirect(url_for("home"))
        
    else:
        try:
            post = Post.query.get(id)
            return render_template("edit.html",post=post)
        except Exception as error:
            print("Error: ", error)

    return redirect(url_for("home"))


## APIS
# Busca todos os posts no banco e dados e mostra na página /index.html
@app.route("/api/posts")
def api_list_posts():
    try:
        posts = Post.query.all()
        return jsonify([post.to_dict() for post in posts])
    except Exception as error:
        app.logger.error(error)
        print("Error: ", error)

    return jsonify([])


# Adiciona o post no banco de dados
@app.route("/api/post", methods=["PUT"])
def api_add_post():
    try:
        data = request.get_json()
        post = Post(title=data["title"], content=data["content"], author=data["author"])
        db.session.add(post)
        db.session.commit()
        return jsonify({"Success": True})
    except Exception as error:
        app.logger.error(error)
        print("Error: ", error)

    return jsonify({"Success": False})


# Deleta o post no banco de dados
@app.route("/api/post/<int:id>", methods=["DELETE"])
def api_delete_post(id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"Success": True})
    except Exception as error:
        app.logger.error(error)
        print("Error: ", error)

    return jsonify({"Success": False})


# Editar o post no banco de dados
@app.route("/api/post/<int:id>", methods=["PUT"])
def api_edit_post(id):
    try:
        post = Post.query.get(id)
        data = request.get_json()
        post.title = data["title"]
        post.content = data["content"]
        post.author = data["author"]
        db.session.commit()
        return jsonify({"Success": True})
    except Exception as error:
        print("Error: ", error)

    return jsonify({"Success": False})


# Definindo security headers em nossa aplicação web
@app.after_request
def add_header(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "script-src 'none'"
    response.headers["Access-Control-Allow-Origin"] = "*" # Header muito perigoso
    response.headers["Access-Control-Allow-Credentials"] = "true" # Header muito perigoso
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


with app.app_context():
    db.create_all()

app.run(debug=True)