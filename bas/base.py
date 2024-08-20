import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='telegrambotdb'
)

mycursor = mydb.cursor()

print('Бот запущен!')
