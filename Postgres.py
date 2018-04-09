# This will be the file that has our Postgres class

import logging
import psycopg2

class Postgres():
    """
    This class will provide our setup, connection, cursor, and SQL Commands
    """
    def __init__(self, database=None, user=None, password=None):
        self.database = database
        self.user = user
        self.password = password
        self._ready = False
        self.cursor = None
        self.conn = None

    def connect(self):
        """
        This method handles connecting to the database and obtaining a cursor
        """
        try:
            self.conn = psycopg2.connect(dbname=self.database,
                                         user=self.user,
                                         password=self.password)
            self.cursor = self.conn.cursor()
            self._ready = True
        except:
            logging.error("Can't connect to the database")
            self._ready = False

        return self._ready

    def executeCommand(self, command=None):
        """
        This method executes and commits the SQL statements.
        It takes as an input a command (string).
        If it fails to write, rollback
        """
        if not self._ready:
            logging.error("Connection not ready.")
            return None

        logging.info(command)
        try:
            self.cursor.execute(command)
            self.conn.commit()
            logging.info("Successful SQL command execution: %s" % command)
            return True
        except:
            self.conn.rollback()
            logging.error("Unsuccessful SQL command execution: %s" % command)
            return False

    def createTable(self, table_name=None, table_list=[]):
        """
        This method can be used to create a table in the database.
        It takes an input of table_name (string) and table_list (list)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False
        if len(table_list) == 0:
            return False

        table_string = "create table " + table_name + "("
        for column, type in table_list:
            table_string += "%s %s," % (column, type)
        table_string = table_string[:-1]
        table_string += ");"

        return self.executeCommand(table_string)

    def insertData(self, table_name=None, values=[]):
        """
        This method will insert 1 row of data into the database.
        It has inputs of table_name (string) and values (list)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False
        if len(values) == 0:
            return False

        command_string = "insert into " + table_name + " ("
        for column in values[0]:
            command_string += column + ","
        command_string = command_string[:-1]
        command_string += ") values ("

        for data in values[1]:
            if type(data).__name__ == 'str':
                command_string += "\'%s\'," % data
            elif type(data).__name__ == 'float':
                command_string += "%f," % data
            elif type(data).__name__ == 'int':
                command_string += "%d," % data
            else:
                command_string += "\'%s\'," % str(data)
        command_string = command_string[:-1]
        command_string += ");"

        return self.executeCommand(command_string)

    def queryAllData(self, table_name=None):
        """
        This method will return all data in the table.
        It takes input of table_name (string)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False

        command_string = "select * from " + table_name
        self.executeCommand(command_string)

        if self.cursor.rowcount != 0:
            return self.cursor.fetchall()
        else:
            logging.error("Query failed to run. Table is empty.")
            return None

    def querySpecificData(self, table_name=None, query_data=None):
        """
        This method will return specific data in the table.
        It takes input of table_name (string) and query_data (string)
        """
        if not self._ready:
            return None
        if table_name is None:
            return False
        if query_data is None:
            return False

        command_string = "select * from " + table_name + " where " + query_data
        self.executeCommand(command_string)

        if self.cursor.rowcount != 0:
            return self.cursor.fetchone()
        else:
            logging.error("Query failed to run. There is no %s in %s" %(query_data, table_name))
            return None
