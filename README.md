# SGXdatacollection
Collection of stock data for stock on the Singapore Exchange (SGX)

The program collects and evaluates the correlation of price movement between stocks on the SGX. This is for the user to select stocks that are more independent of each other, reducing the beta of their portfolio. 

**DISCLAIMER: Stocks with low correlation are only candidates for further consideration. By no means should the stock be bought without further research, even if this program has shown that it has low correlation. PLEASE DO FURTHER RESEARCH ON THE FUNDAMENTALS AND TECHNICALS OF THE COMPANY**

The sgx_corr_sums.csv file has a good summary of the correlation. Minimising 'Sum square of corr' find the most uncorrelated stock. Further information on correlation values can be found in 'Sum of corr' (note that corr can be positive or negative). Further confirmation can be done referring to the sgx_corr.csv file.

This program requires the following libraries:
bs4 
datetime  
matplotlib
numpy 
os
pandas
pandas_datareader
pickle
requests
