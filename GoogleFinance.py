# This file contain GoogleFinance class, attributes, methods

import datetime
import logging
import time
import urllib.request


class GoogleFinance:
    """
    This class will open and get the financial data from Google Finance and save it as csv
    """
    def __init__(self, symbol='', start_date=''):
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.base_url = 'http://finance.google.com/finance/historical?q='
        logging.info("GoogleFinance object created: symbol = %s and start_date = %s "
                     % (symbol, time.strftime('%Y/%m/%d',start_date)))

    def get_historical_stock_data(self, filename):
        """
        This method is to get historical stock data from google finance and save it as csv file.

        ex:
        a_google_finance.historical_stock_data("goog")
        """
        today_date = datetime.datetime.today()
        url = '%s%s&startdate=%s&enddate=%s&output=csv' % (self.base_url, self.symbol,
                                                           time.strftime('%Y/%m/%d',self.start_date),
                                                           datetime.datetime.strftime(today_date,'%Y/%m/%d'))
        logging.info("Going to %s" %url)

        try:
            url_data = urllib.request.urlopen(url)
            csv_data = (url_data.read()).decode("utf-8-sig").encode("utf8-")
            try:
                csv_file = open(filename, 'w', newline='')
                csv_file.write(csv_data.decode("utf-8"))
                csv_file.close()
            except:
                print("Failed to open and write file")
                logging.error("Failed to open and write %s" % filename)
        except:
            print("Failed to get data from url")
            logging.error("Failed to get data from: %s" % url)