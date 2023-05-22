import sqlite3
from sqlite3 import Error

class DBManager:
    def __init__(self, db_file):
        """ initialize the DBManager with the database file name """
        self.db_file = db_file
        self.conn = None

        

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
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
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        return [col[1] for col in columns]
    
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
