import pandas as pd
import numpy as np
import streamlit as st
import datetime
import random
import plotly_express as px

from datetime import datetime, timedelta

def get_dates_between_2_dates(start_date, end_date):
    dates = []
    # Iterate over the range of dates and append them to the list
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    return dates

basic_stock_data = pd.read_csv("data/stock_basic_new.csv",encoding="gbk")

def generate_random_ratings(rating_name):
    random_ratings = [random.randrange(0,random.randrange(500,10000))/100-random.randrange(0,random.randrange(500,10000))/100 for i in np.arange(basic_stock_data.shape[0])]
    return pd.DataFrame({"股票名称":basic_stock_data['name'],"大盘":basic_stock_data['market'],"行业":basic_stock_data['industry'],rating_name:random_ratings}).sort_values(rating_name,ascending=False)

def split_by_market(df):
    market_1 = df.loc[df['大盘']=="主板"]
    market_2 = df.loc[df['大盘']=="科创板"]
    market_3 = df.loc[df['大盘']=="创业板"]
    market_4 = df.loc[df['大盘']=="北交所"]
    return market_1,market_2,market_3,market_4

def generate_daily_ratings_of_stock(length):
    daily_ratings = [random.randrange(60,120)]
    for i in np.arange(1,length):
        daily_ratings.append(daily_ratings[i-1]+random.randrange(-40,40))
    return daily_ratings
    

def generate_daily_of_several_stocks(df,top_x,start_date,end_date):
    date_format = "%Y%m%d"  # Format of the input dates
    # Convert the input strings to datetime objects
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    length = (end-start).days+1
    result = pd.DataFrame({"日期":get_dates_between_2_dates(start,end)})
    for stock_name in df.head(top_x)['股票名称']:
        result[stock_name] = generate_daily_ratings_of_stock(length)
    return result


b1_ratings = generate_random_ratings("强势系数B1")
b2_ratings = generate_random_ratings("强势系数B2")
b2_market_1, b2_market_2,b2_market_3,b2_market_4 = split_by_market(b2_ratings)
b3_ratings = generate_random_ratings("强势系数B3")
b4_ratings = generate_random_ratings("强势系数B4")
b4_market_1, b4_market_2,b4_market_3,b4_market_4 = split_by_market(b4_ratings)

def display_table(df,head,font_size):
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    # Display a static table
    st.table(df.head(head))
    
    st.markdown(
        """
        <style>
        table {
            font-size: """+str(font_size)+"""px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_table_with_expander(df,expander_name,head,font_size):
    with st.expander(expander_name):
        display_table(df,head,font_size)


def display_data(df,expander_name,head,font_size,start_date,end_date):
    with st.expander(expander_name):
        display_table(df,head,font_size)
        
        daily = generate_daily_of_several_stocks(df,head,str(start_date),str(end_date))
        px_plot = px.line(daily,x="日期",y=daily.columns.drop("日期"),labels={"value":"强势系数"})
        st.plotly_chart(px_plot)
    
    

#-------------------------------------------------



st.title("股票强势系数分析-V2")
st.header("输入参数")
#basic_stock_data = pd.read_csv("data/basic_stock_data.csv")

ts_codes = st.text_input("以下可输入想要排序的股票名字或者股票代码。注意多个股票之间要用英文逗号分割。",value="平安银行,873223.BJ,万科A,000006.SZ").split(",")
start_time = int(st.text_input("以下输入开始计算强势系数的时间。格式是YYYYMMDD",value="20220915"))
end_time = int(st.text_input("以下输入停止计算强势系数的时间",value="20230323"))
top_rows_displayed = int(st.text_input("显示多少个最高股票",value=10))
b1_ma_days = int(st.text_input("B1使用的均线天数（可参考B1公式）",value=5))
b2_ma_days = int(st.text_input("B2使用的均线天数（可参考B2公式）",value=5))
b3_time_segment = int(st.text_input("B3涨速时段时长（可参考B3定义文档）",value=5))
b4_time_segment = int(st.text_input("B4涨速时段时长（可参考B4定义文档）",value=5))
b3_top_segment_count = int(st.text_input("B3相对涨速最靠前的数量（可参考B3定义文档）",value=3))
b4_top_segment_count = int(st.text_input("B4相对涨速最靠前的数量（可参考B4定义文档）",value=3))
b3_index_scale_factor = int(st.text_input("B3板块涨速放大因子（可参考B3定义文档）",value=1))
b4_index_scale_factor = int(st.text_input("B4大盘涨速放大因子（可参考B4定义文档）",value=1))
st.header("计算结果")
display_data(b1_ratings,"根据强势系数B1排序的股票",top_rows_displayed,1,start_time,end_time)
display_data(b2_ratings,"根据强势系数B2排序的股票",top_rows_displayed,1,start_time,end_time)
display_data(b2_market_1,"根据强势系数B2排序的主板股票",top_rows_displayed,1,start_time,end_time)
display_data(b2_market_2,"根据强势系数B2排序的科创板股票",top_rows_displayed,1,start_time,end_time)
display_data(b2_market_3,"根据强势系数B2排序的创业板股票",top_rows_displayed,1,start_time,end_time)
display_data(b2_market_4,"根据强势系数B2排序的北交所股票",top_rows_displayed,1,start_time,end_time)
display_data(b3_ratings,"根据强势系数B3排序的股票",top_rows_displayed,1,start_time,end_time)
display_data(b4_ratings,"根据强势系数B4排序的股票",top_rows_displayed,1,start_time,end_time)
display_data(b4_market_1,"根据强势系数B4排序的主板股票",top_rows_displayed,1,start_time,end_time)
display_data(b4_market_2,"根据强势系数B4排序的科创板股票",top_rows_displayed,1,start_time,end_time)
display_data(b4_market_3,"根据强势系数B4排序的创业板股票",top_rows_displayed,1,start_time,end_time)
display_data(b4_market_4,"根据强势系数B4排序的北交所股票",top_rows_displayed,1,start_time,end_time)