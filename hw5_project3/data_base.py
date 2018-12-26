import sqlite3
import os
from flask import Flask
from flask import request, render_template


app = Flask(__name__)


def create_bd():
    if not os.path.exists(os.path.join('.', "bd.sqlite")):
        conn = sqlite3.connect(os.path.join('.', "bd.sqlite"))
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS info(id INTEGER PRIMARY KEY AUTOINCREMENT, article_name VARCHAR NOT NULL,'
                  'article_url VARCHAR NOT NULL)')
        c.execute('CREATE TABLE IF NOT EXISTS texts(id INTEGER PRIMARY KEY AUTOINCREMENT, lemmatised VARCHAR NOT NULL,'
                  'plain_text VARCHAR NOT NULL)')
        conn.commit()


def watch_dirs(p):
    files_list = []
    for root, dirs, files in os.walk(p):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list


def fill_bd():
    if os.path.exists(os.path.join('.', "bd.sqlite")):
        conn = sqlite3.connect(os.path.join('.', "bd.sqlite"))
        c = conn.cursor()
        files_plain = watch_dirs('Clean_Papers')
        files_parsed = watch_dirs('Parsed_Papers_txt')
        for i in range(len(files_plain)):
            try:
                with open(files_plain[i], encoding='utf-8') as f:
                    text = f.readlines()
                title = text[1]
                url = text[3]
                text_plain = text[4]
                with open(files_parsed[i], encoding='utf-8') as f:
                    text = f.readlines()
                text_parsed = text[4]
                c.execute('INSERT INTO info(article_name, article_url) VALUES (?, ?)', [title, url])
                c.execute('INSERT INTO texts(lemmatised, plain_text) VALUES (?, ?)', [text_parsed, text_plain])
            except UnicodeDecodeError:
                continue
            except IndexError:
                continue
        conn.commit()


@app.route('/')
def index():
    if request.args:
        search = request.args['question']
        result = search_info(search)
        return render_template("page.html", result=result)
    return render_template("page.html", result="")


def search_info(search):
    conn = sqlite3.connect(os.path.join('.', "bd.sqlite"))
    c = conn.cursor()
    c.execute('SELECT * FROM info INNER JOIN texts ON info.id = texts.id')
    result = c.fetchall()
    urls = []
    for i in result:
        if search in i[5]:
            url = i[2]
            url = url.split()[1]
            urls.append(url)
    if not urls:
        return ['Ничего не найдено']
    return urls


if __name__ == '__main__':
    app.run(debug=False)
