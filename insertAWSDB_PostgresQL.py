import insertUtil as ut
import psycopg2


#Tạo kết nối với RDS PostgreSQL và thêm dữ liệu vào
conn = psycopg2.connect(host='database-postgresql.cxla1knoy4uq.us-east-1.rds.amazonaws.com', database='covid19_postgressql', user='postgres', password='12345678', port='5432')
print('Open DB successfully')
ut.insert(conn)
ut.select(conn)
conn.close()
print('Successfully')