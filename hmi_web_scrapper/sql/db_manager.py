import pyodbc
from pyodbc import Error

from utils.logger import get_logger

class DBManager:
    def __init__(self, server, database, user, password):
        """ initialize the DBManager with the database details """
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.conn_str = 'DRIVER={FreeTDS};SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.user+';PWD='+ self.password+';TDS_Version=7.3'
        self.conn = None
        self.logger = get_logger(__name__)

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.conn_str)
        except Error as e:
            self.logger.error(f"Couldn't connect. connection string: {self.conn_str}")
        
    def disconnect(self):
        """ close the database connection """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.logger.info(f"disconectiong from {self.database} at {self.server}")

    def __get_column_names(self, table):
        """ retrieve the column names of a table """
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
            columns = cursor.fetchall()
            return [col[0] for col in columns]
        except Exception as e:
            self.logger.error(f"Error: {e}")

            
    def insert(self, table, data):
        """
        Insert data into table.
        `data` is a list containing the values to be inserted.
        The order of the values should correspond to the table's column order.
        """
        if not self.conn:
            self.logger.warn("There is no database connection.")
            return
        
        column_names = self.__get_column_names(table)
        placeholders = ', '.join('?' * len(column_names))
        sql = f'INSERT INTO {table} VALUES ({placeholders})'
        
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(data))
        self.conn.commit()
        self.logger.info(f"Data: {data} inserted at {self.server}:{self.database}:{table}")
