from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from config_execution_api import tickers, account, port_key
import threading
import pandas as pd
import time 

#contains all the IB wrapper functions
class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self) 
        self.hist_dict = {}
        self.bid_price_dict = {}
        self.ask_price_dict = {}
        self.pos_dict = {}
        self.account_dict = {}
        self.order_dict = {}
        self.data_event = False
        self.hist_data_event = False
        self.execution_dict = {}
        
#####   wrapper function for reqHistoricalData. this function gives the candle historical data
    def historicalData(self, reqId, bar):
        self.data_event = False
        if tickers[reqId] not in self.hist_dict:
            self.hist_dict[tickers[reqId]] = pd.DataFrame([{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}])#.set_index('Date')
        else:
            df = pd.DataFrame([{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}])#.set_index('Date')
            self.hist_dict[tickers[reqId]] = pd.concat([self.hist_dict[tickers[reqId]],df], axis=0, ignore_index=True)
 
#####   wrapper function for reqHistoricalData. this function triggers when historical data extraction is completed      
    def historicalDataEnd(self, reqId, start, end):       
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        self.data_event = True
        if len(self.hist_dict.keys()) >= len(tickers):
            self.hist_data_event = True
    
##### wrapper function for reqMktData. this function handles streaming market data  (last current price)
    def tickPrice(self, reqId, tickType, price, attrib):    
        super().tickPrice(reqId, tickType, price, attrib)
        if tickers[reqId] in self.bid_price_dict and tickers[reqId] in self.ask_price_dict:
            self.cancelMktData(reqId)
        else:
            if tickType == 1:
                self.bid_price_dict[tickers[reqId]] = price
            elif tickType == 2 :
                self.ask_price_dict[tickers[reqId]] = price
    
####    wrapper function for reqAccountUpdates. Get account information
    def updateAccountValue(self, key, val, currency, accountName):
        self.data_event = False 
        super().updateAccountValue(key, val, currency, accountName)
        keys = ['AccruedCash', 'AvailableFunds', 'BuyingPower','CashBalance', 'Currency','EquityWithLoanValue', 
        'ExcessLiquidity', 'FullAvailableFunds', 'FullInitMarginReq','FundValue', 
        'FutureOptionValue', 'FuturesPNL', 'GrossPositionValue',  'InitMarginReq', 
        'IssuerOptionValue','MaintMarginReq',  'NetLiquidation', 'RealizedPnL',
        'TotalCashBalance', 'TotalCashValue', 'UnrealizedPnL' ]
        if key in keys and currency == 'USD':
            self.account_dict[key] = val

####    wrapper function for reqAccountUpdates. Signals the end of account information
    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
        print("AccountDownloadEnd. Account:", accountName)
        #if len(self.pos_dict) >= len(tickers):
        self.reqAccountUpdates(False, account) #cancel update account subscription
        self.data_event = True
        
####    wrapper function for reqAccountUpdates. Signals the end of account information
    def position(self, account, contract, position, avgCost):
        super().position(account, contract, position, avgCost)
        self.pos_dict = {}
        self.pos_dict[contract.symbol] = {'SecurityType': contract.secType,
                                          'Quantity':position, 
                                          'AverageCost':avgCost}
        
    def positionEnd(self):
        print('Latest position data Extracted')
        
#### wrapper function for reqOpenOrders. this function gives the open orders
    def openOrder(self, orderId, contract, order, orderState):
        self.data_event = False
        self.order_dict = {} #reset to zero
        super().openOrder(orderId, contract, order, orderState)
        self.order_dict[contract.symbol] = {"PermId": order.permId,
                                            "OrderId": orderId, 
                                            "SecType": contract.secType,
                                            "Action": order.action, 
                                            "OrderType": order.orderType,
                                            "Quantity": order.totalQuantity, 
                                            "CashQty": order.cashQty, 
                                            "LmtPrice": order.lmtPrice, 
                                            "AuxPrice": order.auxPrice, 
                                            "Status": orderState.status}
#####   wrapper function, this function triggers when order extraction is completed 
    def openOrderEnd(self):
        print("Open Orders Retrieved")
        self.data_event = True
        
#####   wrapper function for reqExecutions.   this function gives the executed orders                
    def execDetails(self, reqId, contract, execution):
        super().execDetails(reqId, contract, execution)
        self.execution_dict[contract.symbol] = {"PermId":execution.permId,
                                                "Side":execution.side, 
                                                "Shares":execution.shares, 
                                                "Price":execution.price,
                                                "AvPrice":execution.avgPrice, 
                                                "cumQty":execution.cumQty}
        
#####   wrapper function, this function is called once all executions have been sent to a client in response to reqExecutions()
    def execDetailsEnd(self, reqId:int):
        print("Executed Order Info Retrieved")
        
####  wrapper function for reqIds. this function manages the Order ID.
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        
    
#establish the deamon thread that holds the api connection 
def API_connection():   
    app = TradeApp()
    app.connect(host='127.0.0.1', port= port_key, clientId=23) #port 4002 for ib gateway paper trading/7497 for TWS paper trading
    con_thread = threading.Thread(target=app.run, daemon=True)
    con_thread.start()
    while app.isConnected() == False:
        print('Waiting for Connection')	
        continue
    
    print('Established Connection')	
    return app

    
    
app = API_connection()
