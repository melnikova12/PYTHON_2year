from flask import Flask
from flask import request, render_template, redirect, url_for
import csv
import json


app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        lang = request.args['lang']
        age = request.args['age']
        town = request.args['town']
        cheese = request.args['cheese']
        stone = request.args['stone']
        fill_csv([lang, age, town, cheese, stone])  # дописать список при добавлении чего-то кроме твОрог/творОг
        return redirect(url_for("thanks"))
    return render_template("main_page.html")


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


def fill_csv(list_data):
    with open('data.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t')
        spamwriter.writerow(list_data)


def read_csv():
    data = []
    with open('data.csv', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            data.append(row)
    return data


@app.route('/json')
def show_json():
    data = read_csv()
    data_json = [{"lang": i[0], "age": i[1], "town": i[2], "cheese": i[3], "stone": i[4]} for i in data]
    str_json = json.dumps(data_json, indent=1, ensure_ascii=False)
    return render_template("json.html", json_str=str_json)


@app.route('/stats')
def stats():
    data = read_csv()
    return render_template('stats.html', len1=len(data), data=data)


@app.route ('/search')
def search():
    data = read_csv()
    towns = []
    for i in data:
        if i[2] not in towns:
            towns.append(i[2])
    langs = []
    for i in data:
        if i[0] not in langs:
            langs.append(i[0])
    if request.args:
        lang = request.args['lang']
        age = request.args['age']
        town = request.args['town']
        search = request.args['search']
        global results_list
        results_list = find_in_csv(lang, age, town, search)
        if not results_list:
            return redirect(url_for("not_found"))
        return redirect(url_for("results"))
    return render_template('search.html', towns=towns, langs=langs)


def find_in_csv(lang, age, town, search):
    data = read_csv()
    results = []
    for row in data:
        if search in row:
            if lang != "Любой" and lang == row[0]:
                if age != "Любой" and age == row[1]:
                    if town != "Любой" and town == row[2]:
                        results.append(row)
                    elif town == "Любой":
                        results.append(row)
                elif age == "Любой":
                    if town != "Любой" and town == row[2]:
                        results.append(row)
                    elif town == "Любой":
                        results.append(row)
            elif lang == "Любой":
                if age != "Любой" and age == row[1]:
                    if town != "Любой" and town == row[2]:
                        results.append(row)
                    elif town == "Любой":
                        results.append(row)
                elif age == "Любой":
                    if town != "Любой" and town == row[2]:
                        results.append(row)
                    elif town == "Любой":
                        results.append(row)
    return results


@app.route('/results')
def results():
    return render_template("results.html", len1=len(results_list), data=results_list)


@app.route('/not_found')
def not_found():
    return render_template("not_found.html")


if __name__ == '__main__':
    app.run(debug=False)
    
    
