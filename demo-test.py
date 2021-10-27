import streamlit as st
from datetime import date
import datetime
from plotly import graph_objs as go
import pandas as pd
import numpy as np

# Plotting Dictionaries
spxAxisLimitDict={
    "C"   : [2,10],
    "CL"  : [0,150],
    "EC"  : [0,2],
    "ES"  : [1000,5000],
    "GC"  : [1000,2500],
    "NG"  : [0,8],
    "S"   : [5,20],
    "TYF" : [100,200]
}

histxAxisLimitDict={
    "C"   : [-1.00, 1.00],
    "CL"  : [-1.00, 1.00],
    "EC"  : [-1.00, 1.00],
    "ES"  : [-1.00, 1.00],
    "GC"  : [-1.00, 1.00],
    "NG"  : [-1.00, 1.00],
    "S"   : [-1.00, 1.00],
    "TYF" : [-1.00, 1.00]
}

histyAxisLimitDict={
    "C"   : [0, 4],
    "CL"  : [0, 4],
    "EC"  : [0, 7],
    "ES"  : [0, 4],
    "GC"  : [0, 4],
    "NG"  : [0, 4],
    "S"   : [0, 4],
    "TYF" : [0, 12]
}

appTitle = "1QBit CME Market Sentiment Meter Demo"

st.title(appTitle)

dmCode = ["C","CL","EC","ES","GC","NG","S","TYF"]

futSelectPrompt = "Please select the futures product of interest."

selectedFut = st.sidebar.selectbox(futSelectPrompt,dmCode)

dateSelectPrompt = "Please select the date range you want to examine."

dateRange = st.sidebar.date_input(label = dateSelectPrompt, value = [date(2012,1,3), date(2021,10,22)],min_value = date(2012,1,3) , max_value = date(2021,10,22))

fileName = "data/1QBit_MSM_"+selectedFut

pdf = pd.read_csv(fileName).drop([0,1]).reset_index(drop=True)

st.subheader("raw data")

st.write(pdf.head())

# Trade Date
dobList = []
for row in range(len(pdf)):
    dobList.append(datetime.datetime.strptime(str(pdf[selectedFut+'_TRADEDATE'][row]),'%Y%m%d').date())
#endFor

# Most Active Futures Price
spxList = []
for row in range(len(pdf)):
    spxList.append(float(pdf[selectedFut+'_PRICE_SETTLE_ACTIVE'][row]))
#endFor

# Market States
productComplacent = []
for row in range(len(pdf)):
    productComplacent.append(int(pdf[selectedFut+'_MIX_COMPLACENT'][row]))
#endFor

productBalanced = []
for row in range(len(pdf)):
    productBalanced.append(int(pdf[selectedFut+'_MIX_BALANCED'][row]))
#endFor

productAnxious = []
for row in range(len(pdf)):
    productAnxious.append(int(pdf[selectedFut+'_MIX_ANXIOUS'][row]))
#endFor

productConflicted = []
for row in range(len(pdf)):
    productConflicted.append(int(pdf[selectedFut+'_MIX_CONFLICTED'][row]))
#endFor


# Plot ES and ES Market States
fig = go.Figure()

# Complacent States Plotting
exes=   dobList
whys=   spxAxisLimitDict[selectedFut][1]*np.array(productComplacent)
fig.add_trace(go.Scatter(x=exes, y=whys, fill='tozeroy',name="Complacent",mode='lines', line=dict(width=0.0, color='rgba(89, 179, 230, 0.4)'))) # fill down to xaxis

# Balanced States Plotting
exes=   dobList
whys=   spxAxisLimitDict[selectedFut][1]*np.array(productBalanced)
fig.add_trace(go.Scatter(x=exes, y=whys, fill='tozeroy',name="Balanced",mode='lines', line=dict(width=0.0, color='rgba(255, 255, 255, 0.4)'))) # fill down to xaxis

# Anxious States Plotting
exes=   dobList
whys=   spxAxisLimitDict[selectedFut][1]*np.array(productAnxious)
fig.add_trace(go.Scatter(x=exes, y=whys, fill='tozeroy',name="Anxious",mode='lines', line=dict(width=0.0, color='rgba(242, 230, 64, 0.4)'))) # fill down to xaxis

# Conflicted States Plotting
exes=   dobList
whys=   spxAxisLimitDict[selectedFut][1]*np.array(productConflicted)
fig.add_trace(go.Scatter(x=exes, y=whys, fill='tozeroy',name="Conflicted",mode='lines', line=dict(width=0.0,color='rgba(204, 102, 0, 0.4)'))) # fill down to xaxis

# Settlement Price Plotting
exes= dobList
whys = np.array(spxList)
fig.add_trace(go.Scatter(x=exes, y=whys,name="Settlement Price",mode='lines',line=dict(color='black', width=2))) # fill down to xaxis

fig.update_layout(yaxis_range=spxAxisLimitDict[selectedFut],xaxis_range=dateRange,title_text=selectedFut+" Settlement Price (Most Active)",title_x=0.5,xaxis_title="Trade Date", yaxis_title="Price (USD)",xaxis_rangeslider_visible=True)


st.plotly_chart(fig)

def msmHist(tradeDate):
    msmInfoOneDate = pdf.loc[pdf[selectedFut+'_TRADEDATE'] == tradeDate]
    stateText = msmInfoOneDate[selectedFut+'_MIX_STATE'].tolist()[0]
    dateIndex = pdf.loc[pdf[selectedFut+'_TRADEDATE'] == tradeDate].index.tolist()[0]
    probDensity = pd.to_numeric(pdf.iloc[dateIndex,91:]).tolist()
    xHistBin = np.arange(-1.00,1.56,0.01)
    figHist = go.Figure()
    figHist.add_trace(go.Scatter(x=xHistBin, y=probDensity, fill='tozeroy',mode='lines', line=dict(width=1.0,color='black')))
    figHist.update_layout(xaxis_range=histxAxisLimitDict[selectedFut],title_text=selectedFut+" Risk-Return Curve"+" ("+stateText+")",title_x=0.5,xaxis_title="Estimated Percent Price Movement Over 12 Months",yaxis_title="Probability Density")
    figHist.update_xaxes(tickformat="%")
    st.plotly_chart(figHist)
#endDef

stateDate = st.date_input(label = "Pick a single date.", value = date(2020,4,8), min_value = date(2012,1,3) , max_value = date(2021,10,22))

stateDate = int(stateDate.strftime('%Y%m%d'))

msmHist(stateDate)
