from flask import app
from app import DB, recievers
from utils.Filters import mainFilter


def selectFilter(data):
    filter = mainFilter(data)
    print(filter)
    filter1 = ''
    response = []

    print(recievers)
    if filter:
        data = DB.session.execute('SELECT count(*) as count,EXTRACT(year FROM date) as year  '
                                  'FROM customer where ' + filter + ' group by date ;')
        for i in data:
            response.append({"y": i['count'], "x": int(i['year'])})
        sendEmail = DB.session.execute('SELECT  customer_email as mail '
                                       'FROM customer where ' + filter + ' ;')
        recievers.clear()
        for i in sendEmail:
            recievers.append(i['mail'])
    else:
        data = DB.session.execute('SELECT count(*) as count,EXTRACT(year FROM date) as year   '
                                  'FROM customer  group by EXTRACT(year FROM '
                                  'date) ;')

        for i in data:
            response.append({"y": i['count'], "x": int(i['year'])})
        sendEmail = DB.session.execute('SELECT  customer_email as mail '
                                       'FROM customer;')
        for i in sendEmail:
            recievers.append(i['mail'])

        # recievers.append(i['mail'])
    # print(response)
    print(recievers)
    return {'response': response}


def getLimit(attribute_name):
    return {'min': getData(attribute_name, 'min'), 'max': getData(attribute_name, 'max')}


def getData(attribute_name, lim):
    data = DB.session.execute('SELECT ' + lim + '(' + attribute_name + ') FROM customer ;')
    for i in data:
        return str(i[0])

