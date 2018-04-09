# This will be our top level UI module. Menubar & Toolbar options: File -> Exit, Help -> About.
# This program gets stock data that is specified in our GUI from Google Finance
# then scrape the officers info from Yahoo Finance.

import os
import logging
import sys
import time
import GoogleFinance
from PyQt4 import QtGui
from PyQt4 import QtCore
import UI_about
import UI_central
import Postgres
import requests
import bs4


class UI(QtGui.QMainWindow):
    """
    This will be our main window
    """
    def __init__(self, parent=None, configuration=None):
        super(UI, self).__init__(parent)

        # Setting configuration

        self.config = configuration
        try:
            self.config.read("stocks.cfg")
        except:
            print("Config fail")
            sys.exit(2)

        log_file = 'default.log'
        if self.config.has_section('LOGGING'):
            if self.config.has_option('LOGGING', 'LOG_FILE'):
                log_file = self.config.get('LOGGING', "LOG_FILE")

        try:
            logging.basicConfig(filename=log_file,
                                level=logging.DEBUG,
                                format='%(asctime)s, %(levelname)s, %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p')
        except:
            print("No %s file created" % log_file)
            sys.exit(3)

        logging.info("Program has started.")

        # Connect to database

        self.password = os.getenv('PASSWORD')
        self.db = Postgres.Postgres(database='postgres', user='postgres', password=self.password)
        if not self.db.connect():
            return

        self.db.createTable(table_name='known_stocks', table_list= [('SYMBOL','text'),('SHARES','integer')])

        # Create Exit and About Action and add them to menubar and toolbar

        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        aboutAction = QtGui.QAction('About',self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About')
        aboutAction.triggered.connect(self.aboutAction)
                                                      
        self.statusBar().showMessage('')
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        helpMenu = menuBar.addMenu('Help')
        fileMenu.addAction(exitAction)
        helpMenu.addAction(aboutAction)

        exitToolbar = self.addToolBar('Exit')
        exitToolbar.addAction(exitAction)
        aboutToolbar = self.addToolBar('About')
        aboutToolbar.addAction(aboutAction)

        # Add UI central and connect the button to methods

        self.central = UI_central.UI_central()
        self.central.addButton.clicked.connect(self.addButtonClicked)
        self.central.officersButton.clicked.connect(self.stockButtonClicked)
        self.setCentralWidget(self.central)

        # Add stocks found in known_stocks to stock combobox
        known_stocks = self.db.queryAllData(table_name="known_stocks")
        for line_item in known_stocks:
            self.central.stockCombo.addItem(line_item[0])

        self.setWindowTitle("Python Programming 1 Lab 10")
        self.show()

    def addButtonClicked(self):
        """
        This method will read every info that we select at our interface, then proceed to get the data we selected,
        the log it into the specific database
        """
        date = self.central.calendar.selectedDate()
        date_string = "{0} {1} {2}".format(
            date.day(), date.longMonthName(date.month()),
            date.year())
        stock = self.central.stockEdit.toPlainText().upper()

        try:
            number_shares = int(self.central.numberStockEdit.toPlainText())
        except ValueError:
            number_shares = 0

        # If stock is new, then write it in config, known_stock table, and add stock to combobox option

        if self.config.has_section(stock):
            print("%s Stocks are found!" % stock)
            logging.info("%s Stocks are found!" % stock)
        else:
            if not self.db.insertData(table_name='known_stocks', values=[('SYMBOL', 'SHARES'),
                                                                         (stock, number_shares)]):
                logging.error("Data not inserted: (%s, %s)" % (stock, number_shares))
            self.central.stockCombo.addItem(stock)
            self.config.add_section(stock)
            self.config.set(stock, "SHARES", number_shares)
            self.config.set(stock, "DATE", date_string)
            try:
                f = open("stocks.cfg", "w")
                self.config.write(f)
            except:
                print("Config file is not created")
                logging.error("Config file is not created")

        # Create Google Finance instance and get historical data

        start_date = time.strptime(date_string, "%d %B %Y")
        a_google_finance = GoogleFinance.GoogleFinance(stock, start_date)
        filename = stock + ".csv"
        a_google_finance.get_historical_stock_data(filename)

        if not self.db.createTable(table_name=stock, table_list=[('DATE','date'),('STOCK_PRICE','money')]):
            logging.error("Table %s not created" % stock)
            return

        # Read file to add data to table

        try:
            file = open(filename, "r")
            for line in file:
                data = line.split(',')
                if data[0] == 'Date':
                    continue
                else:
                    data_date = time.strftime('%Y-%m-%d',time.strptime(data[0],'%d-%b-%y'))
                    data_float = float(data[4])
                    if not self.db.insertData(table_name=stock, values=[('DATE','STOCK_PRICE'),(data_date,data_float)]):
                        logging.error("Data not inserted: (%s, %s)" % (data_date,data_float))
        except:
            logging.error("No such file: %s" % filename)

    def stockButtonClicked(self):
        """
        This method will get officers data from selected stock
        """
        self.central.officersTextEdit.clear()
        stock = self.central.stockCombo.currentText()
        url_string = "https://finance.yahoo.com/quote/%s/profile?p=%s" % (stock,stock)

        try:
            r = requests.get(url_string)
        except:
            logging.error("Failed at requesting this url: %s" % url_string)
            self.central.officersTextEdit.setText("Failed to get %s" % url_string)
            return

        try:
            soup = bs4.BeautifulSoup(r.text)
        except:
            logging.error("Failed on soup")
            self.central.officersTextEdit.setText("Failed on soup")
            return

        try:
            table = soup.find_all("table")
            rows = table[0].find_all("tr")
            data = []
            officers_string = ''
            for row in rows:
                cols = row.find_all('td')
                cols = [str.text.strip() for str in cols]
                data.append([str for str in cols if str])
            for x in data:
                if x == []:
                    continue
                else:
                    for y in x:
                        officers_string += y + ", "
                    officers_string = officers_string[:-2]
                    officers_string += "\n"
            self.central.officersTextEdit.setText(officers_string)
        except:
            logging.error("Failed on formatting the table")
            self.central.officersTextEdit.setText("Failed on formatting the table")
            return

        self.updateGraph(stock)

    def updateGraph(self,symbol = None):
        """
        This method will update Graph and take one parameter symbol (string).
        """
        if symbol is None:
            return

        data = self.db.queryAllData(table_name=symbol)
        prices = [float(y.strip("$").replace(',','')) for x,y in data]
        dates = [x for x,y in data]
        self.central.qtMpl.addLine(dates,prices,symbol)

    def aboutAction(self):
        """
        Display our ABOUT GUI
        """
        about = UI_about.UI_about()
        about.exec_()
        return