# This contains our test cases for Postgres

import os
import nose
import logging
import Postgres


class Test_Postgres:
    def __init__(self):
        self.logcapture = nose.plugins.logcapture.LogCapture()
        self.logcapture.start()
        logging.basicConfig(filename="testlog.log",
                            level=logging.DEBUG,
                            format='%(asctime)s, %(levelname)s, %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        self.cursor = None
        self.conn = None
        pass

    def setup(self):
        self.logcapture.begin()
        self.password = os.getenv('PASSWORD')
        self.a_postgres = Postgres.Postgres(database='postgres', user='postgres', password=self.password)
        self.empty_postgres = Postgres.Postgres()

    def teardown(self):
        self.logcapture.end()
        self.empty_postgres.executeCommand("DROP TABLE ")
        self.a_postgres.executeCommand("DROP TABLE test4")

    def test_ctor(self):
        """
        Test Postgres constructor method
        """
        assert self.empty_postgres.database == None
        assert self.empty_postgres.user == None
        assert self.empty_postgres.password == None

        assert self.a_postgres.database == 'postgres'
        assert self.a_postgres.user == 'postgres'
        assert self.a_postgres.password == self.password

    def test_connect(self):
        """
        Test Postgres connect method
        """
        assert self.empty_postgres.connect() == False
        assert self.a_postgres.connect() == True

    def test_createTable(self):
        """
        Test Postgres createTable method
        """
        self.table_list = [("name", "text"), ("number", "integer")]
        self.wrong_table_list = [("name","string"), ("number","int")]

        self.empty_postgres.connect()
        self.empty_postgres.createTable()
        self.a_postgres.connect()
        self.a_postgres.createTable()
        self.a_postgres.createTable(table_name="test1")
        self.a_postgres.createTable(table_name="test3", table_list=self.wrong_table_list)
        self.a_postgres.createTable(table_name="test4",table_list=self.table_list)


    def test_insertData(self):
        """
        Test Postgres insertData method
        """
        self.wrong_value = [("name", "number"), (3.98, None)]
        self.correct_value = [("name", "number"), ("Nina", 35)]

        self.empty_postgres.connect()
        self.empty_postgres.insert_single_row()
        self.a_postgres.connect()
        self.a_postgres.insert_single_row()
        self.a_postgres.insert_single_row(table_name="test4")
        self.a_postgres.insert_single_row(table_name="test4", values=self.wrong_value)
        self.a_postgres.insert_single_row(table_name="test4", values=self.correct_value)