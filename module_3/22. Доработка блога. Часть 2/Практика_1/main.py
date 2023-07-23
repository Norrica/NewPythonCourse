from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index/")
def index():
    context = {
        "page_name": "Главная",
    }

    return render_template("index.html", **context)


@app.route("/blog/")
def blog():
    context = {
        "page_name": "Блог",
    }

    return render_template("blog.html", **context)


@app.route("/contacts/")
def contacts():
    context = {
        "page_name": "Контакты",
    }

    return render_template("contacts.html", **context)


if __name__ == "__main__":
    app.run()
