# -*- coding: utf-8 -*-
# Alexandr Sorokousov
# sorok.web@gmail.com
# TG @sorokousov
# ---------------------
import os
import threading
import time
from datetime import datetime
from config import number_of_threads
from models import db, Task, create_tables
from class_parser import YahooFinanceHistory


@db.connection_context()
def run_parse(task):
    print('Котировка:', task.quote)

    # Отмечаем старт парсинга котировки
    task.started = True
    task.started_at = datetime.now()
    task.save()

    fin = YahooFinanceHistory(quote=task.quote.lower())
    fin.run_magic()


@db.connection_context()
def starter():
    tasks = Task.select().where(Task.started == False)

    if not tasks:
        return

    print(len(tasks), 'новых заданий')
    for ind, task in enumerate(tasks, start=1):

        print('Задание:', ind, '; Активных потоков:', threading.active_count() - 1)

        while True:

            if threading.active_count() < number_of_threads:
                threading.Thread(target=run_parse, args=(task,)).start()
                break
            else:
                time.sleep(0.1)


if __name__ == '__main__':
    print('Ожидание прогрузки MySql')
    time.sleep(5)
    print('Парсер запущен')
    print(os.environ['MYSQL_DATABASE'],
          os.environ['MYSQL_USER'],
          os.environ['MYSQL_PASSWORD'],
          os.environ['MYSQL_HOST'])
    print('--->')
    db.connect(reuse_if_open=True)
    create_tables()
    db.close()
    while True:
        starter()
        time.sleep(5)