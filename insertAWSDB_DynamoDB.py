from inspect import Attribute
import boto3
import pandas as pd

dynamodb = boto3.resource('dynamodb')

tablename = 'datacovid'


# Tạo bảng trên dynamoDB bằng module boto3 với khoá chính là id (partition key)
def createTable():
    table = dynamodb.create_table(
        TableName = tablename,
        KeySchema = [
            {
                'AttributeName' : 'id',
                'KeyType' : 'HASH'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName' : 'id',
                'AttributeType' : 'N',
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits' : 10,
            'WriteCapacityUnits' : 10,
        }
    )
    table.wait_util_exists()

def insert():
    # Tương tự, mình chỉ xét 5 ngày đầu tháng 1/2022
    dt=['01-01-2022','01-02-2022','01-03-2022','01-04-2022','01-05-2022']
    counter = 1
    table = dynamodb.Table(tablename)
    for d in dt:
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + d + '.csv'
        df = pd.read_csv(url, index_col=0)
        cols = list(df.columns)
        for index, row in df.iterrows():
            dct = {'id':counter}
            for x in cols:
                dct[str(x).lower()] = str(row[x])
            dct['date'] = d
            table.put_item(
                Item = dct
            )
            print('total ' + str(counter) + ' row inserted')
            counter = counter + 1
    print('insert complete')

table = dynamodb.Table(tablename)
try:
    createTable()
    print('create table successfully')
except:
    print('table has already existed')
insert()

#Tạo bảng và thêm dữ liệu và bảng
