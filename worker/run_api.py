# -*- coding: utf-8 -*-
# Alexandr Sorokousov
# sorok.web@gmail.com
# TG @sorokousov
# ---------------------
import os
import time

from flask import Flask, request, jsonify, abort
import json

from models import Task, db, HistoryQuote, create_tables

app = Flask(__name__)


@app.route("/api/tasks", methods=["POST"])
@db.connection_context()
def task():
    try:
        data_ = request.get_data(as_text=True)
        data = json.loads(data_)
    except:
        data = {}

    if not data:
        return abort(404)

    if 'quote' not in data:
        return abort(400)

    # Проверяем наличие котировки, если нет, пишем задачу и возвращаем 202, если есть, возвращаем 409
    task = Task.get_or_none(Task.quote == data['quote'])
    if not task:
        task = Task.create(quote=data['quote'])
        return jsonify({'task': task.__data__ if task else None})
    else:
        return jsonify({'error': "Задача с такой котировкой уже существует"})


@app.route('/api/tasks/<quote>', methods=['GET'])
@app.route('/api/tasks/', methods=['GET'])
@db.connection_context()
def get_task(quote=None):
    if not quote:
        tasks = []
        for i in Task.select():
            tasks.append({
                'quote': i.quote,
                'started': i.started,
                'successful': i.successful,
                'stopped': i.stopped,
                'reason_stop': i.reason_stop,
                'added_at': i.added_at,
                'started_at': i.started_at,
                'completed_at': i.completed_at,
            })

        return jsonify({'tasks': tasks})

    task = Task.get_or_none(Task.quote == quote)
    return jsonify({'task': task.__data__ if task else None})


@app.route('/api/quotes/<quote>', methods=['GET'])
@db.connection_context()
def get_quote(quote):
    if not quote:
        return abort(404)

    history = []
    for i in HistoryQuote.select().where(HistoryQuote.quote == quote):
        history.append({
            'date': i.date,
            'open': i.open,
            'high': i.high,
            'low': i.low,
            'close': i.close,
            'adj_close': i.adj_close,
            'volume': i.volume,
        })

    return jsonify({quote: history})


if __name__ == '__main__':
    print('Ожидание прогрузки MySql')
    time.sleep(5)
    print('API запущен')
    app.run(host='0.0.0.0', port=5000, debug=True)
