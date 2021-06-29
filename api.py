import flask
import os
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    print(cursor.description)
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/historic/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('historic_data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM HISTORIC_AQ').fetchall()
    print(all_books)
    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/historic', methods=['GET'])
def api_filter():
    query_parameters = request.args

    #id = query_parameters.get('id')
    city = query_parameters.get('city')
    #author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    # if id:
    #     query += ' id=? AND'
    #     to_filter.append(id)
    if city:
        query += ' city=? AND'
        to_filter.append(city)
    # if author:
    #     query += ' author=? AND'
    #     to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('historic_data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()