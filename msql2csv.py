import sys
import pyodbc
import pandas.io.sql as psql


class SQLExtractor:
    """
        This class defines the basic functions to convert
        the MS SQL database tables to CSV.
    """
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def connect_to_database(self):
        """
            Connects to database
        """
        try:
            conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=' + self.server + '; '
                      'Database='+ self.database + ';'
                      'UID='+ self.username + ';'
                      'PWD='+ self.password + ';'
                      'Trusted_Connection=no;'
					  'Persist Security Info=True;')
            print(conn)
            print('DATABASE CONNECTED')
            return conn
        except Exception as exc:
            print(f'DATABASE ERROR: {exc}')

    def get_table_list(self, conn):
        """
            Fetches all table names from given database
        """
        try:
            sql = "SELECT TABLE_NAME FROM [" + self.database + "].INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            cursor = conn.cursor()
            cursor.execute(sql)
            for (table_name,) in cursor:
                print(table_name)
        except Exception as exc:
            print(f'DATABASE ERROR: {exc}')

    def convert_to_csv(self, conn, table_name):
        """
            Converts given database table to csv.
        """
        try:
            countsql = "SELECT count(*) FROM " + self.database + ".dbo." + table_name
            cursor = conn.cursor()
            cursor.execute(countsql)
            counts = cursor.fetchone()
            count = counts[0]
            print(count)
            ii = int(count)/100000
            iii = 0
            while int(ii) > 0:
                sql = "SELECT * FROM " + self.database + ".dbo." + table_name + " ORDER BY 1 OFFSET %s ROWS FETCH NEXT 100000 ROWS ONLY" % str(iii)
                df = psql.read_sql(sql, conn)
                df.to_csv(sys.argv[6] + table_name + str(ii) + ".csv", index=False)
                iii = iii + 100000
                ii = ii - 1
            sql = "SELECT * FROM " + self.database + ".dbo." + table_name + " ORDER BY 1 OFFSET %s ROWS FETCH NEXT 100000 ROWS ONLY" % str(iii)
            df = psql.read_sql(sql, conn)
            df.to_csv(sys.argv[6]+table_name + ".csv", index=False)
            print(f'table '+ table_name + ' saved as ' + table_name + '.csv')
        except Exception as exc:
            print(f'DATABASE ERROR: {exc}')



print('-' * 80)
print('CONVERT MS SQL DATABASE TABLES TO CSV')
print('-' * 80)

if __name__ == "__main__":
    server =  str(sys.argv[1]) # 'ISRAJ-IDARE\SQLEXPRESS'
    database = str(sys.argv[2]) # 'TEST_HITACHI'
    username = str(sys.argv[3])
    password = str(sys.argv[4])
    #server =  str(input("Enter Server: ")) # 'ISRAJ-IDARE\SQLEXPRESS'
    #database = str(input("Enter Database Name: ")) # 'TEST_HITACHI'
    #username = str(input("Enter Username: "))
    #password = str(input("Enter Password: "))
    #server = 'localhost'
    #database = 'gen'
    #username = 'sa'
    #password = '123456'

    sql = SQLExtractor(server, database, username, password)
    conn = sql.connect_to_database()

    print(' ' * 40)
    print('Getting '+ database + ' tables . . .')
    print('-' * 40)
    print('Tables of database ' + database)
    print('-' * 40)

    list_a = sql.get_table_list(conn)
    print(list_a)
    print('-' * 40)
    print(' ' * 40)

    running = True

    while running:
        #table_name = str(input("Enter Table Name or EXIT: "))
        table_name = str(sys.argv[5])
        #table_name = 'place'

        if table_name.lower() != 'exit':
            sql.convert_to_csv(conn, table_name)
            running = False
        else:
            conn.close()
            running = False