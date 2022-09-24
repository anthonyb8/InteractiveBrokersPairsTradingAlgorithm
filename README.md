******Interactive Brokers Pairs Trading Algorithm******

**Project Description:**

The Interactive Brokers Native API is the foundation of this project. I chose Interactive Brokers because of the API's robust set of functions that lend    themselves to algorithmic trading. Interactive Brokers provides the  ability to trade a wide range of assets and markets, it is a highly regarded brokerage for algorithmic trading. This project is currently divided into two directories. The first, titled 'Pairs Identifier', is used to search for cointegrated pairs in a stock universe. In the code upload, I set the universe to a finite number of stocks, but it could be set to an entire exchange or a hand-picked universe based on whatever criteria you deem necessary.This directory will generate a csv file that ranks the cointegrated pairs based on the strength of the relationship. In the second directory, you'll find the strategy executor.  Because of the way the execution directory is currently constructed, you must manually enter the pair to be traded. Currently, the system is only designed to trade one pair at a time. In the future, I hope to add the ability to trade multiple pairs.

I began developing this project because of my passion fro quantitative trading,  with the goal of deploying on my personal portfolio. I'm always looking for ways to improve the project, so if anyone is interested in contributing, or if you have any questions or comments, please let me know. 

**How to Install and Run the Project**

  1. Create Interactive Brokers Pro account
  2. Download IB workstation or Gateway(I suggest workstation at first)
  3. Download python(I run the Anaconda version) 
  4. Necessary Libraries:
    - ibapi.client
    - ibapi.wrapper
    - pandas
  5. Download both files(Note you will need to input IB account number)
  6. With IB workstation or gateway open run Pair Identifier 
  7. In the execution conifg_strategy you will need to fill in the pair of tickers you want to trade



