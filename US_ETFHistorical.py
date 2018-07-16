import fix_yahoo_finance as yf
import pandas as pd

def pull_data(ticker_symbol,start,end):    
    data = yf.download(ticker_symbol,start,end,progress=False)   # downloads data from yahoo finance and stores into data variable(which is a pandas dataframe)
    #print(data)
    closeIndex=data['Close']
    return closeIndex

if __name__=='__main__':

    df=pd.read_csv('US ETFs.csv')
    print(df.columns)
    tksymbols=df.iloc[:,0].values.tolist()   # select a column='tckr symbol' and convert to list


    stdate='2018-04-01'
    enddate='2018-06-30'

    dailyQuotes=pull_data(tksymbols,stdate,enddate)
    
    print(dailyQuotes)

    dailyQuotes.to_csv('US Historical-3months.csv',index=True)

    
