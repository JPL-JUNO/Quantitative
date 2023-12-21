"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-20 22:26:20
@Description  : 
"""

import yfinance as yf
import streamlit as st
import datetime
import pandas as pd
import cufflinks as cf
from plotly.offline import iplot

cf.go_offline()


@st.cache_data
def get_sp500_components():
    # Define a function for
    # downloading a list of S&P 500 constituents from Wikipedia:
    # df = pd.read_html(
    #     'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # df = df[0]
    # tickers = df['Symbols'].to_list()
    # tickers_companies_dict = dict(
    #     zip(df['Symbols'], df['Security'])
    # )
    tickers = ['AAPL', 'IBM', 'MSFT', 'TSLA']
    tickers_companies_dict = {
        'AAPL': 'Apple Inc.',
        'IBM': 'IBM',
        'MSFT': 'Microsoft',
        'TSLA': 'Tesla, Inc.',
    }
    return tickers, tickers_companies_dict


@st.cache_data
def load_data(symbol, start, end):
    # Define a function for downloading historical stock prices using yfinance:
    return yf.download(symbol, start, end)


@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')


st.sidebar.header('Stock Parameters')

available_tickers, tickers_companies_dict = get_sp500_components()
ticker = st.sidebar.selectbox(
    'Ticker',
    available_tickers,
    format_func=tickers_companies_dict.get
)
start_date = st.sidebar.date_input(
    'Start date',
    datetime.date(2019, 1, 1)
)
end_date = st.sidebar.date_input(
    'End date',
    datetime.date.today()
)

if start_date > end_date:
    st.sidebar.error('The end date must fall after the start date')

# Define the part of the sidebar used for tuning the details of the technical analysis:
st.sidebar.header('Technical Analysis Parameters')
volume_flag = st.sidebar.checkbox(label='Add Volume')

exp_sam = st.sidebar.expander('SMA')
sam_flag = exp_sam.checkbox(label='Add SMA')
sma_periods = exp_sam.number_input(
    label='SMA Periods',
    min_value=1,
    max_value=50, value=20, step=1
)

exp_bb = st.sidebar.expander('Bollinger Bands')
bb_flag = exp_bb.checkbox(label='Add Bollinger Bands')
bb_periods = exp_bb.number_input(label='BB Periods',
                                 min_value=1, max_value=50,
                                 value=20, step=1)
bb_std = exp_bb.number_input(label='# of standard deviations',
                             min_value=1, max_value=4,
                             value=2, step=1)

exp_rsi = st.sidebar.expander('Relative Strength Index')
rsi_flag = exp_rsi.checkbox(label='Add RSI')
rsi_periods = exp_rsi.number_input(
    label='RSI Period',
    min_value=1,
    max_value=50,
    value=20,
    step=1
)

rsi_upper = exp_rsi.number_input(label='RSI Upper',
                                 min_value=50, max_value=90, value=70,
                                 step=1)
rsi_lower = exp_rsi.number_input(label='RSI Lower',
                                 min_value=10, max_value=50, value=30,
                                 step=1)


st.title('A simple web app for technical analysis')
st.write('''
         ### User manual
         * you can select any company from the S&P 500 constituents
         * you can select the time period of your interest
         * you can download the selected data as a CSV file
         * you can add the following Technical Indicators to the plot: Simple Moving Average, Bollinger Bands, Relative Strength Index
         * you can experiment with different parameters of the indicators
         ''')

df = load_data(ticker, start_date, end_date)

data_exp = st.expander('Preview data')
available_cols = df.columns.tolist()

columns_to_show = data_exp.multiselect(
    'Columns',
    available_cols,
    default=available_cols,
)


data_exp.dataframe(df[columns_to_show])

csv_file = convert_df_to_csv(df[columns_to_show])

data_exp.download_button(
    label='Download selected as CSV',
    data=csv_file,
    file_name=f'{ticker}_stock_price.csv',
    mime='text/csv',
)

title_str = f"{tickers_companies_dict[ticker]}'s stock price"
qf = cf.QuantFig(df, title=title_str)
if volume_flag:
    qf.add_volume()
if sam_flag:
    qf.add_sma(periods=sma_periods)
if bb_flag:
    qf.add_bollinger_bands(periods=bb_periods,
                           boll_std=bb_std)
if rsi_flag:
    qf.add_rsi(periods=rsi_periods,
               rsi_upper=rsi_upper,
               rsi_lower=rsi_lower,
               showbands=True)

fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)
