# Задание: Заменить хардкод на шаблонизатор Jinja
#          Переменные: title, photo, name, links
#          links — словарь, ключи: url, text

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    context = {
        "title": "Моя визитная карточка",
        "photo": "/static/image/photo.jpeg",
        "name": "Саша",
        "links": [
            {
                "url": "https://vk.com/geekbrainsru",
                "text": "ВКонтакте"
            },
            {
                "url": "https://geekbrains_ru.t.me/",
                "text": "Telegram",
            }
        ]
    }

    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run()
