# attribute_name={customer_name,customer_gender,customer_age,location,pincode,date,total_purchase,quantity,product_type}
#
# type=0
# customer_name
# location
# product_type
# customer_gender
#
# filterType=0
# =>particular string
# filterType=1
# => a-z

# type=1
#
# pincode
# customer_age
# particular search
# total_purchase
#
# filterType=0
# contains
# filterType=2
# particular number
#
# filterType=1
# limit 0-100
#

#
# data=[attribute_name
#     , type,filterType,
#       {
#
#       }
#       ]
#
# data=app.DB.session.execute('SELECT * FROM customer  WHERE 1=0;')
#         for i in data:
#             print(i)
# #
from datetime import datetime


def stringFilter(stringTypeData):
    if stringTypeData['filterType'] == 1:
        return "{} like \'%{}%\' ".format(stringTypeData['attribute'], stringTypeData['data'])
    if stringTypeData['filterType'] == 0:
        return "{} = \'{}\' ".format(stringTypeData['attribute'], stringTypeData['data'])
    if stringTypeData['filterType'] == 2:
        return "{} <= \'{}\' AND {} >=\'{}\' ".format(stringTypeData['attribute'], stringTypeData['data']['max'],
                                                      stringTypeData['column'], stringTypeData['data']['min'])


def numberFilter(numberTypeData):
    if numberTypeData['filterType'] == 0:
        return "{} = {}".format(numberTypeData['attribute'], int(numberTypeData['data']))
    if numberTypeData['filterType'] == 1:
        return "{} <= {} AND {} >={}".format(numberTypeData['attribute'], (numberTypeData['data']['max']),
                                             numberTypeData['attribute'], (numberTypeData['data']['min']))


def dateFiler(dateTypeData):
    if dateTypeData['filterType'] == 0:
        return "EXTRACT(year FROM {}) <= {} AND EXTRACT(year FROM {}) >= {}".format(
            "date", dateTypeData['data']['max'][0:4], "date",
            dateTypeData['data']['min'][0:4])


def mainFilter(data):
    result = ''
    for i in range(0, len(data)):
        if data[i]['type'] == 0:

            result += stringFilter(data[i]) + 'AND '
        else:
            if data[i]['type'] == 1:
                result += numberFilter(data[i]) + 'AND '
            else:
                result += dateFiler(data[i]) + ' AND '

    print(result)
    result = result[:-4]
    return result
