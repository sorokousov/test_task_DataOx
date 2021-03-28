# -*- coding: utf-8 -*-
# Alexandr Sorokousov
# sorok.web@gmail.com
# TG @sorokousov
# ---------------------
from datetime import datetime
import peewee as pw
import os

db = pw.MySQLDatabase(database=os.environ['MYSQL_DATABASE'],
                      user=os.environ['MYSQL_USER'],
                      password=os.environ['MYSQL_PASSWORD'],
                      host=os.environ['MYSQL_HOST'],
                      autoconnect=False)


class Task(pw.Model):
    quote = pw.CharField(max_length=100)
    started = pw.BooleanField(default=False)
    successful = pw.BooleanField(default=False)
    stopped = pw.BooleanField(default=False)
    reason_stop = pw.CharField(max_length=100, null=True)
    added_at = pw.DateTimeField(default=datetime.now())
    started_at = pw.DateTimeField(null=True)
    completed_at = pw.DateTimeField(null=True)

    class Meta:
        database = db


class HistoryQuote(pw.Model):
    quote = pw.CharField(max_length=100)
    date = pw.CharField(max_length=20)
    open = pw.CharField(max_length=20)
    high = pw.CharField(max_length=20)
    low = pw.CharField(max_length=20)
    close = pw.CharField(max_length=20)
    adj_close = pw.CharField(max_length=20)
    volume = pw.CharField(max_length=20)

    class Meta:
        database = db


def create_tables():
    Task.create_table()
    HistoryQuote.create_table()

