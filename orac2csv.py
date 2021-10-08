import sys
import cx_Oracle
import pandas as psql
from sqlalchemy import create_engine


class SQLExtractor:
    """
        This class defines the basic functions to convert
        the MS SQL database tables to CSV.
    """
    def __init__(self, server, database, username, password, dsn, port):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.dsn = dsn

    def connect_to_database(self):
        """
            Connects to database
        """
        listener = server + ':' + port +'/orcl'
        print(listener)
        try:
            conn = cx_Oracle.connect(user=username,password=password,dsn=listener)
            print(conn)
            print('DATABASE CONNECTED')
            return conn
        except Exception as exc:
            print(f'DATABASE ERROR: {exc}')


    def convert_to_csv(self, conn, table_name):
        """
            Converts given database table to csv.
        """
        try:
            countsql = "SELECT count(*) FROM " + self.database + "." + table_name
            cursor = conn.cursor()
            cursor.execute(countsql)
            counts = cursor.fetchone()
            count = counts[0]
            print(count)
            ii = int(count)/100000
            
            iii = 0
            iiii = 100000
            while int(ii) > 0:
                sql = "SELECT * FROM " + self.database + "." + table_name + " WHERE ROWNUM<= " + str(iiii) + " MINUS SELECT * FROM " + self.database + "." + table_name + " WHERE ROWNUM< %s" % str(iii)
                df = psql.read_sql(sql, conn)
                df.to_csv(sys.argv[8] + table_name + str(iii) + ".csv", index=False)
                iiii = iiii + 100000
                iii = iii + 100000
                ii = ii - 1
            sql = "SELECT * FROM " + self.database + "." + table_name + " WHERE ROWNUM<= " + str(iiii) + " MINUS SELECT * FROM " + self.database + "." + table_name + " WHERE ROWNUM< %s" % str(iii)
            df = psql.read_sql(sql, conn)
            df.to_csv(sys.argv[8]+table_name + ".csv", index=False)
            print(f'table '+ table_name + ' saved as ' + table_name + '.csv')
        except Exception as exc:
            print(f'DATABASE ERROR: {exc}')



print('-' * 80)
print('CONVERT MS SQL DATABASE TABLES TO CSV')
print('-' * 80)

if __name__ == "__main__":
    try:
        server =  str(sys.argv[1]) # 'ISRAJ-IDARE\SQLEXPRESS'
        database = str(sys.argv[6]) # 'TEST_HITACHI'
        username = str(sys.argv[4])
        password = str(sys.argv[5])
        dsn = str(sys.argv[3])
        port = str(sys.argv[2])
    except:
        print("orac2csv.exe <server> <port> <dsn> <username> <password> <database> <table> <filepath>")
        exit()
    #server =  str(input("Enter Server: ")) # 'ISRAJ-IDARE\SQLEXPRESS'
    #database = str(input("Enter Database Name: ")) # 'TEST_HITACHI'
    #username = str(input("Enter Username: "))
    #password = str(input("Enter Password: "))
    #server = 'localhost'
    #database = 'gen'
    #username = 'sa'
    #password = '123456'

    sql = SQLExtractor(server, database, username, password, dsn, port)
    conn = sql.connect_to_database()


    running = True

    while running:
        table_name = str(sys.argv[7])
        #table_name = 'place'

        if table_name.lower() != 'exit':
            sql.convert_to_csv(conn, table_name)
            running = False
        else:
            conn.close()
            running = False