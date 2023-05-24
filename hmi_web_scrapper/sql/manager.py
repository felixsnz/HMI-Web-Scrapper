import pyodbc
from pyodbc import Error

class DBManager:
    def __init__(self, driver, server, database, user, password):
        """ initialize the DBManager with the database details """
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        try:
            self.conn = pyodbc.connect('DRIVER={'+self.driver+'};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.user+';PWD='+ self.password)
        except Error as e:
            print(e)
        
    
    def disconnect(self):
        """ close the database connection """
        if self.conn:
            self.conn.close()
            self.conn = None

    def __get_column_names(self, table):
        """ retrieve the column names of a table """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
        columns = cursor.fetchall()
        return [col[0] for col in columns]
    
    def insert(self, table, data):
        """
        Insert data into table.
        `data` is a list containing the values to be inserted.
        The order of the values should correspond to the table's column order.
        """
        if not self.conn:
            print('No database connection')
            return
        
        column_names = self.__get_column_names(table)
        placeholders = ', '.join('?' * len(column_names))
        sql = f'INSERT INTO {table} VALUES ({placeholders})'
        
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(data))
        self.conn.commit()
        print('Data inserted successfully')
