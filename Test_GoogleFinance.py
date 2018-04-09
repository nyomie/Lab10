# This contains our test cases for GoogleFinance

import time
import logging
import nose
import GoogleFinance


class Test_GoogleFinance:
    def __init__(self):
        self.logcapture = nose.plugins.logcapture.LogCapture()
        self.logcapture.start()
        logging.basicConfig(filename='testlog.log',
                            level=logging.DEBUG,
                            format='%(asctime)s, %(levelname)s, %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        pass

    def setup(self):
        self.logcapture.begin()
        self.a_start_date = time.strptime('2017/08/14','%Y/%m/%d')
        self.goog_GoogleFinance = GoogleFinance.GoogleFinance(symbol='goog', start_date=self.a_start_date)
        self.random_GoogleFinance = GoogleFinance.GoogleFinance(symbol="abcde", start_date=self.a_start_date)

    def teardown(self):
        self.logcapture.end()
        del(self.goog_GoogleFinance)
        del(self.random_GoogleFinance)
        print("logcapture: %s " % (self.logcapture.formatLogRecords()))

    def test_ctor(self):
        """
        Test GoogleFinance constructor method
        """
        assert self.goog_GoogleFinance.symbol == "GOOG"
        assert self.goog_GoogleFinance.start_date == self.a_start_date
        assert self.random_GoogleFinance.symbol == "ABCDE"
        assert self.random_GoogleFinance.start_date == self.a_start_date

    def test_stock(self):
        """
        Test GoogleFinance get_historical_stock_data method
        """
        self.goog_GoogleFinance.get_historical_stock_data("")
        self.goog_GoogleFinance.get_historical_stock_data("GOOG")
        self.random_GoogleFinance.get_historical_stock_data("ABCDE")
