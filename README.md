# test_task_DataOx
Задание https://github.com/sorokousov/test_task_DataOx/blob/main/Python%20Test%20Task.pdf

Парсить котировки с сайта можно с помощью простого запроса по URL:
https://query1.finance.yahoo.com/v7/finance/download/ZOM?period1=0&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true

Но это слишком просто, поэтому я использовал Selenium со всеми шагами со стартовой страницы https://finance.yahoo.com/, что конечно же повлияло на скорость работы парсера. После добавления задачи, в зависимости от мощности железа, нужно немного подождать и проверить готовность соответствующим запросом.

В файле *config.py* можно установить
- количество потоков для запуска парсера
- максимальное время в секундах на каждый шаг работы парсера
- максимальное время в секундах ожидания загрузки файла


#Запуск

*git clone https://github.com/sorokousov/test_task_DataOx.git*

*docker-compose up --build*

# API запросы
***Создать задачу***

>**Request:**
```
POST http://localhost:5000/api/tasks
Accept: application/json

{
"quote": "ZUO"
}
```
>**Response:**
```
{
  "task": {
    "added_at": "Sun, 28 Mar 2021 12:50:37 GMT",
    "quote": "ZUO"
  }
}
```
***Выбрать задачу***

>**Request:**
```
GET http://localhost:5000/api/tasks/ZOM
```
>**Response:**
```
{
  "task": {
    "added_at": "Sun, 28 Mar 2021 13:45:30 GMT",  # Дата добавления задачи
    "completed_at": "Sun, 28 Mar 2021 13:50:56 GMT",  # Дата завершения работы парсера
    "id": 4,  
    "quote": "ZOM",
    "reason_stop": "0",  # Поле содержит ошибки работы парсера
    "started": true,  # Парсер обрабатывает задачу
    "started_at": "Sun, 28 Mar 2021 13:50:41 GMT",  # Дата старта обработки задачи
    "stopped": false,  # Флаг остановки обработки с ошибкой
    "successful": true  # Парсер успешно обработал задачу
  }
}
```
***Выбрать все задачи***

>**Request:**
```
GET http://localhost:5000/api/tasks
```
>**Response:**
```
{
  "tasks": [
    ...
    {
      "added_at": "Sun, 28 Mar 2021 13:45:30 GMT",
      "completed_at": "Sun, 28 Mar 2021 13:50:56 GMT",
      "quote": "ZOM",
      "reason_stop": "0",
      "started": true,
      "started_at": "Sun, 28 Mar 2021 13:50:41 GMT",
      "stopped": false,
      "successful": true
    }
    ...
  ]
}
```
***Выбрать котировку***

>**Request:**
```
GET http://localhost:5000/api/quotes/zom
```
>**Response:**
```
{
  "zom": [
    {
      "adj_close": "2.389000",
      "close": "2.389000",
      "date": "2017-11-21",
      "high": "2.450000",
      "low": "2.180000",
      "open": "2.350000",
      "volume": "18100"
    },
    {
      "adj_close": "2.395000",
      "close": "2.395000",
      "date": "2017-11-22",
      "high": "2.430000",
      "low": "2.395000",
      "open": "2.409000",
      "volume": "16000"
    },
    ...
  ]
}
```
***Выбрать все котировки***

>**Request:**
```
GET http://localhost:5000/api/quotes
```
>**Response:**
```
{
  "quotes": [
    {
      "PD": [
        {
          "adj_close": "38.250000",
          "close": "38.250000",
          "date": "2019-04-11",
          "high": "39.610001",
          "low": "36.000000",
          "open": "36.750000",
          "volume": "9287900"
        },
        ...
      ],
      "ZOM": [
        {
          "adj_close": "2.389000",
          "close": "2.389000",
          "date": "2017-11-21",
          "high": "2.450000",
          "low": "2.180000",
          "open": "2.350000",
          "volume": "18100"
        },
        ...
      ]
    }
  }
}
```
