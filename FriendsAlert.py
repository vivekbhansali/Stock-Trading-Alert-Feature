import datetime
import unittest

__author__ = 'Vivek Bhansali'

def getAlerts(user_id):
    '''
    This functions calculates the alerts for the user based on the
    transactions of his/her friends. It gives the list of alerts in the
    format <net_friends>,<BUY|SELL>,<ticker> for user to make a decision.

    :param user_id: User ID of the user who wants the alerts
    :return: list of stock alerts (ranked high to low) based on transactions of friends
    '''

    alerts = []
    alerts_dict = dict()

    records = createRecords(user_id)
    sell = []
    buy = []
    for statement in records.values():
        for x in statement['SELL']:
            sell.append(x)
        for y in statement['BUY']:
            buy.append(y)

    sell_map = createStockCountMap(sell)
    buy_map = createStockCountMap(buy)

    if len(buy_map) == 0 and len(sell_map) == 0:
        pass

    elif len(sell_map) == 0 and len(buy_map) != 0:
        for x in buy_map:
            net_number = abs(buy_map[x])
            value = str(net_number) + ',BUY,' + x
            if not net_number in alerts_dict:
                alerts_dict[net_number] = [value]
            else:
                alerts_dict[net_number].append(value)

    elif len(buy_map) == 0 and len(sell_map) != 0:
        for y in sell_map:
            net_number = abs(sell_map[y])
            value = str(net_number) + ',SELL,' + y
            if not net_number in alerts_dict:
                alerts_dict[net_number] = [value]
            else:
                alerts_dict[net_number].append(value)
    else:
        for x in buy_map:
            for y in sell_map:
                if x == y:
                    net_number = buy_map[x] - sell_map[y]
                    if net_number > 0:
                        value = str(net_number) + ',BUY,' + x
                        net_number = abs(net_number)
                        if not net_number in alerts_dict:
                            alerts_dict[net_number] = [value]
                        else:
                            alerts_dict[net_number].append(value)
                        break

                    elif net_number < 0:
                        value = str(abs(net_number)) + ',SELL,' + y
                        net_number = abs(net_number)
                        if not net_number in alerts_dict:
                            alerts_dict[net_number] = [value]
                        else:
                            alerts_dict[net_number].append(value)
                        break

                    else:
                        pass
                else:
                    if (buy_map.has_key(x) and not sell_map.has_key(x)):
                        net_number = abs(buy_map[x])
                        value = str(net_number) + ',BUY,' + x
                        if not net_number in alerts_dict:
                            alerts_dict[net_number] = [value]
                        else:
                            alerts_dict[net_number].append(value)
                        break

                    elif (sell_map.has_key(y) and not buy_map.has_key(y)):
                        net_number = abs(sell_map[y])
                        value = str(net_number) + ',SELL,' + y
                        if not net_number in alerts_dict:
                            alerts_dict[net_number] = [value]
                        else:
                            alerts_dict[net_number].append(value)
                        break

    alerts = sortAlertsDictionary(alerts_dict, alerts)

    return alerts

def sortAlertsDictionary(alerts_dict, alerts):
    '''

    :param alerts_dict: Dictionary to keep net_number associated with corresponding alert
    :param alerts: list of alerts
    :return: sorted list of alerts based on net_number
    '''
    key_list = alerts_dict.keys()
    key_list.sort(reverse=True)

    for key in key_list:
        for alert in alerts_dict[key]:
            alerts.append(alert)

    return alerts

def createRecords(user_id):
    '''
    This function creates a record of dictionary with all the information of stocks
    bought and sold within past week by every user.

    :param user_id: User ID of the user who wants the alerts
    :return: returns a nested dictionary of record with each user as a key and
    two lists containing BUY and SELL stocks corresponding to each user
    '''
    records = {}
    friends = getFriendsListForUser(user_id)

    for friend in friends:
        statement = {}
        sell_stocks = []
        buy_stocks = []
        trades = getTradeTransactionsForUser(friend)
        for trade in trades:
            transaction = trade.split(',')
            if checkDateInRange(transaction[0]):
                if transaction[1] == 'SELL':
                    sell_stocks.append(transaction[2])
                elif transaction[1] == 'BUY':
                    buy_stocks.append(transaction[2])
            else:
                pass
            statement['SELL'] = sell_stocks
            statement['BUY'] = buy_stocks
        records[friend] = statement

    return records

def createStockCountMap(stock_list):
    '''
    This fucntion counts the occurrences of each ticker from the list

    :param stock_list: list containing multiple tickers
    :return: a dictionary with ticker as key and count of occurences of that ticker as corresponding value
    '''
    stock_map = {}

    for stock in stock_list:
        if stock_map.has_key(stock):
            stock_map[stock] = stock_map.get(stock) + 1
        else:
            stock_map[stock] = 1

    return stock_map

def checkDateInRange(date):
    """
    It checks if the input date is in range between current date and last 7 days

    :param date: date of the transaction
    :return: Returns True only if the date is within the past week of the current date
     or returns False
    """

    todays_date = datetime.datetime.now()
    margin = datetime.timedelta(days = 8)
    input_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    return todays_date - margin < input_date <= todays_date

def getFriendsListForUser(user_id):
    """
    Function returns list of distinct User IDs corresponding to the friends of the inout user

    :param user_id: User ID of the user who wants the alerts
    :return: returns list of User Ids of the friends of the user
    """
    friends_list = { 'User1': ['12AB', '13XY', '14PS'],
                     'User2': ['15QW','19MH','20JK'],
                     'User3': ['17VB'],
                     'User4': ['20JK'],
                     'User5': ['12AB', '13XY', '14PS', '15QW', '16ZX', '17VB', '18UP', '19MH', '20JK']
                      }

    return friends_list[user_id]

def getTradeTransactionsForUser(user_id):
    '''
    This function returns list of trades ordered by trade date with the most recent trade first in the list.

    :param user_id: User ID of a friend
    :return: List of transactions of a friend
    '''
    trades_list = { '12AB': ['2017-01-26,SELL,GOOG', '2017-01-25,SELL,AMZN', '2017-01-25,BUY,YHOO', '2017-01-24,BUY,TSLA', '2017-01-24,BUY,NFLX'],
                    '13XY': ['2017-01-26,SELL,AMZN', '2017-01-26,SELL,YHOO', '2017-01-25,BUY,GOOG', '2017-01-24,BUY,NFLX', '2017-01-24,SELL,TSLA'],
                    '14PS': ['2017-01-26,SELL,YHOO', '2017-01-26,BUY,AMZN', '2017-01-26,BUY,GOOG', '2017-01-25,BUY,TSLA', '2017-01-25,BUY,NFLX'],
                    '15QW': ['2017-01-26,BUY,GOOG', '2017-01-25,SELL,AMZN', '2017-01-25,BUY,AMZN', '2017-01-25,BUY,YHOO', '2017-01-24,BUY,GOOG'],
                    '16ZX': ['2017-01-26,SELL,YHOO', '2017-01-26,SELL,AMZN', '2017-01-26,SELL,NFLX', '2017-01-25,SELL,GOOG', '2017-01-25,SELL,YHOO'],
                    '17VB': ['2017-01-26,BUY,YHOO', '2017-01-26,BUY,AMZN', '2017-01-26,BUY,AMZN', '2017-01-25,BUY,GOOG', '2017-01-24,BUY,YHOO'],
                    '18UP': ['2017-01-26,BUY,GOOG', '2017-01-24,SELL,AMZN', '2017-01-23,BUY,AMZN', '2017-01-18,BUY,YHOO', '2017-01-18,BUY,GOOG'],
                    '19MH': ['2017-01-26,SELL,YHOO', '2017-01-23,BUY,AMZN', '2017-01-17,BUY,AMZN', '2017-01-16,BUY,GOOG', '2017-01-15,BUY,YHOO'],
                    '20JK': ['2017-01-10,SELL,YHOO', '2017-01-10,BUY,AMZN', '2017-01-09,BUY,AMZN', '2017-01-08,BUY,GOOG', '2017-01-08,BUY,YHOO']
                     }

    return trades_list[user_id]

class StockAlertsFromFriends_UnitTests(unittest.TestCase):

    def test_MixedTransactions(self):
        print "---Test Case: Mixed Trades---"
        print "This test case contains three friends of 'User1' containing," \
              " mixed number of BUY/SELL Transactions"
        print 'getAlerts(\'User1\') -> ',getAlerts('User1')
        self.assertEqual(getAlerts('User1'), ['3,BUY,NFLX', '1,BUY,GOOG', '1,SELL,YHOO', '1,SELL,AMZN', '1,BUY,TSLA'])

        print ""

    def test_FewTransactionsOlderThanWeek(self):
        print "---Test Case: Few Trades Older Than A Week---"
        print "This test case contains mixed number of BUY/SELL Transactions" \
              " and few transactions older than past week which are not considered in alerts"
        print 'getAlerts(\'User2\') -> ',getAlerts('User2')
        self.assertEqual(getAlerts('User2'), ['2,BUY,GOOG', '1,BUY,AMZN'])

        print ""

    def test_AllTransactionsOlderThanWeek(self):
        print "---Test Case: All Trades Older Than A Week---"
        print "All Transactions are dated older than one week. Hence, we get an empty set"
        print 'getAlerts(\'User4\') -> ',getAlerts('User4')
        self.assertEqual(getAlerts('User4'), [])

        print ""

    def test_AllBuyTransactions(self):
        print "---Test Case: All BUY Trades---"
        print "All Transactions are only BUY transactions"
        print 'getAlerts(\'User3\') -> ',getAlerts('User3')
        self.assertEqual(getAlerts('User3'), ['2,BUY,YHOO', '2,BUY,AMZN', '1,BUY,GOOG'])

        print ""

    def test_AllTransactions(self):
        print "---Test Case: All Trades---"
        print "A user with all friends"
        print 'getAlerts(\'User5\') -> ',getAlerts('User5')
        self.assertEqual(getAlerts('User5'), ['4,BUY,GOOG', '2,BUY,NFLX', '1,SELL,YHOO', '1,BUY,AMZN', '1,BUY,TSLA'])

        print ""

def main():
    unittest.main()

if __name__ == '__main__':
        main()