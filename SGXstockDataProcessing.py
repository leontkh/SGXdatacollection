import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

style.use('ggplot')


#saves a list of all tickers on SGX
def save_sgx_tickers():
    initials=['1','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] #initials of all ticker codes to assist in scraping eoddata.com
    tickers = []
    
    for alphabet in initials:
        resp = requests.get('https://eoddata.com/stocklist/SGX/{}.htm'.format(alphabet))
        soup = bs.BeautifulSoup(resp.text,"lxml")
        table = soup.find('table', {'class':'quotes'})
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(ticker)
    
    with open("sgxtickers.pickle","wb") as f:
        pickle.dump(tickers, f)
        
    print('Ticker codes collected!')
    
    return tickers


#Retrieves stock data from Yahoo Finance and saves each ticker code in separate csv files
def get_data_from_yahoo(reload_sgx=False):
    
    if reload_sgx:
        tickers = save_sgx_tickers()
    else:
        with open("sgxtickers.pickle","rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('sgxstock_dfs'):
        os.makedirs('sgxstock_dfs')
    
    start = dt.datetime(2005,1,1)
    end = dt.datetime(2020,6,7)
    
    for ticker in tickers:
        if not os.path.exists('sgxstock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader("{}.SI".format(ticker), 'yahoo', start, end)
            except:
                continue
            df.to_csv('sgxstock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
    print('Data retrieved from Yahoo! Finance!')


#Compiles the stock data based on their Adjusted CLose values
def compile_data():
    
    if not os.path.exists('sgxtickers.pickle'):
        save_sgx_tickers()
    
    with open("sgxtickers.pickle","rb") as f:
        tickers = pickle.load(f)

    if not os.path.exists('sgxstock_dfs'):
        get_data_from_yahoo()
        
    main_df = pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        try:
            df = pd.read_csv('sgxstock_dfs/{}.csv'.format(ticker))
        except:
            continue
        
        df.set_index('Date', inplace=True)
        
        if df['Volume'][-44:].sum(axis=0, skipna=True) ==0:     #removing stock data that are not active recently
            continue
        
        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 ==0:
            print ('Data for {} ticker codes collected'.format(count))

    print(main_df.head())
    print('Data compiled')
    main_df.to_csv('sgx_joined_closes.csv')

def visualize_data():
    if not os.path.exists('sgx_joined_closes.csv'):
        compile_data()
        
    df = pd.read_csv('sgx_joined_closes.csv')
    df_corr = df.corr()
    print(df_corr)

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) +0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) +0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()

def compile_corr():
    if not os.path.exists('sgx_joined_closes.csv'):
        compile_data()
        
    df = pd.read_csv('sgx_joined_closes.csv')
    df_corr = df.corr()
    df_corr_sum = pd.DataFrame()
    df_corr_sum['Mean corr'] = (df_corr).sum(axis=0, skipna=True)
    df_corr_sum['Mean square corr'] = (df_corr**2).sum(axis=0, skipna=True)
    
    df_corr.to_csv('sgx_corr.csv')
    df_corr_sum.to_csv('sgx_corr_means.csv')


visualize_data()
compile_corr()
