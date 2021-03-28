# -*- coding: utf-8 -*-
# Alexandr Sorokousov
# sorok.web@gmail.com
# TG @sorokousov
# ---------------------
import os
from datetime import datetime
from models import Task, HistoryQuote


def remove_file(file_name):
    try:
        os.remove(file_name)
        print(f"Файл удалён: {file_name}")
    except: pass


def file_to_db(file_name, quote):
    """Потрошим файл и пишем пачкой в базу"""
    task = Task.get_or_none(Task.quote == quote)

    with open(file_name, 'r') as file:
        lines = file.readlines()
        if len(lines) > 1:
            lines.pop(0)
        else:
            task.reason_stop = 'Файл пустой'
            task.stopped = True
            task.completed_at = datetime.now()
            task.save()
            remove_file(file_name=file_name)
            return False

        lines = [{
            'quote': quote,
            'date': line.split(',')[0].strip(),
            'open': line.split(',')[1].strip(),
            'high': line.split(',')[2].strip(),
            'low': line.split(',')[3].strip(),
            'close': line.split(',')[4].strip(),
            'adj_close': line.split(',')[5].strip(),
            'volume': line.split(',')[6].strip()
        } for line in lines]

        # Перед записью новых, удалим существующие записи если они есть
        HistoryQuote.delete().where(HistoryQuote.quote == quote).execute()

        HistoryQuote.insert_many(rows=lines).execute()
        task.successful = True
        task.stopped = False
        task.reason_stop = 0
        task.successful = True
        task.completed_at = datetime.now()
        task.save()
        print(f"{quote}: В БД записано {len(lines)} строк")

    remove_file(file_name=file_name)
    return True