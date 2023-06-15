import pyodbc
from pyodbc import Error
from utils.logger import get_logger

class DbManager:
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
            self.logger.info("successfull connection!")
        except Error as e:
            self.logger.error(f"Couldn't connect. connection string: {self.conn_str}")
        
    def disconnect(self):
        """ close the database connection """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.logger.info(f"disconectiong from {self.database} at {self.server}")

    def _get_column_names(self, table):
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
        
        column_names = self._get_column_names(table)
        placeholders = ', '.join('?' * len(column_names))
        sql = f'INSERT INTO {table} VALUES ({placeholders})'
        
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(data))
        self.conn.commit()
        self.logger.info(f"Data: {data} inserted at {self.server}:{self.database}:{table}")
    

    def get_data(self, table, condition=None):
        """
        Fetch data from a table. 
        `condition` is a string that describes the condition for selection. 
        For example, "id=1" or "name='John'".
        If condition is None, then all rows will be selected.
        """
        if not self.conn:
            self.logger.warn("There is no database connection.")
            return

        cursor = self.conn.cursor()

        if condition:
            sql = f'SELECT * FROM {table} WHERE {condition}'
        else:
            sql = f'SELECT * FROM {table}'

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.logger.info(f"Fetched data: '{rows}' from {self.server}:{self.database}:{table}")
            return rows
        except Error as e:
            self.logger.error(f"Couldn't fetch data. Error: {str(e)}")
    
    def get_column_values(self, table, column, condition=None):
        """
        Fetch a column data from a table. 
        `column` is the name of the column to fetch. 
        `condition` is a string that describes the condition for selection. 
        For example, "id=1" or "name='John'".
        If condition is None, then all rows will be selected.
        """
        if not self.conn:
            self.logger.warn("There is no database connection.")
            return

        cursor = self.conn.cursor()

        if condition:
            sql = f'SELECT {column} FROM {table} WHERE {condition}'
        else:
            sql = f'SELECT {column} FROM {table}'
        
        self.logger.info(f"sql query for get values: {sql}")
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.logger.info(f"Fetched data: '{rows}' from {self.server}:{self.database}:{table}")
            return [row[0] for row in rows]
        except Error as e:
            self.logger.error(f"Couldn't fetch data. Error: {str(e)}")

    def get_table_names(self):
        """ Retrieve the table names of the database """
        if not self.conn:
            self.logger.warn("There is no database connection.")
            return

        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except Error as e:
            self.logger.error(f"Couldn't fetch table names. Error: {str(e)}")
