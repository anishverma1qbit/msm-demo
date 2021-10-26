import streamlit as st
from datetime import date
import yfinance as yf
from plotly import graph_objs as go

appTitle = "1QBit CME Market Sentiment Meter Demo"

st.title(appTitle)

dmCode = ["C","CL","EC","ES","GC","NG","S","TYF"]

futSelectPrompt = "Please select the futures product of interest."

selectedFut = st.sidebar.selectbox(futSelectPrompt,dmCode)

dateSelectPrompt = "Please select the date range you want to examine."

dateRange = st.sidebar.date_input(label = dateSelectPrompt, value = [date(2012,1,3), date(2021,10,22)])

st.text(dateRange)

