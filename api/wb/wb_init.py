from datetime import datetime, timedelta


url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'

dateFrom = int((datetime.now() - timedelta(days=90)).timestamp())
dateTo = int(datetime.now().timestamp())

params = {
        'isAnswered': "false",
        'take': 100,
        'skip': 0,
        'order': 'dateDesc',
        'dateFrom': dateFrom,
        'dateTo': dateTo
    }