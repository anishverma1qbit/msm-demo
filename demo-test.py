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

appTitle = "1QBit CME Market Sentiment Meter"

st.title(appTitle)

st.write(
        """
        ### Demo Information
        Data-driven thinking is becoming increasingly important, and thus prevalent, in finance.
        Students need to know how to collect, clean, and work with data whether they want to develop
        trading algorithms, analyze client information, and beyond.
        
        One indispensable skill that is generally not covered in courses (yet), is being able to deploy
        one's work on a cloud platform. There are many cloud providers like Streamlit, Azure, AWS, and more
        that allow the deploymeny of apps.
        
        The purpose of this demo is to showcase 1QBit's CME Market Sentiment Meter (MSM) – a curated dataset
        that has many metrics suitable organized as a cleaned time-series, readily portable to your workflow.
        One of the key features is the novel Anxiety metric, which is derived from a mixture distribution that
        allows for multiple schools of thought. The MSM provides data for 8 futures markets (C, CL, EC, ES, GC,
        NG, S, and TYF).
        """
    )

dmCode = ["C","CL","EC","ES","GC","NG","S","TYF"]

futSelectPrompt = "Please select the futures product of interest."

selectedFut = st.sidebar.selectbox(futSelectPrompt,dmCode)

dateSelectPrompt = "Please select the date range you want to examine."

dateRange = st.sidebar.date_input(label = dateSelectPrompt, value = [date(2012,1,3), date(2021,10,22)],min_value = date(2012,1,3) , max_value = date(2021,10,22))

fileName = "data/1QBit_MSM_"+selectedFut

pdf = pd.read_csv(fileName).drop([0,1]).reset_index(drop=True)

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

st.write(
        """
        ### Settlement Price and Anxiety Evolution
        Click the sidebar and choose your product of interest, and a date range. From this, you can begin
        to visually explore relationships between the MSM states and the settlement price for the most
        active futures contract. Complacent corresponds to a narrow risk-return distribution, Balanced to
        a slightly wider, more normal distribtion, Anxious to a wider distribution, and Conflicted to
        a potentially bimodal distribution. Generally, the evolution of the states and the Anxiety can better
        inform a trading strategy.
        """
    )


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


st.write(
        """
        ### Mixture Risk–Return Distribution
        Here, you can select the daily mixture distribution for a finer exploration of the Anxiety.
        """
    )


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

st.write(
        """
        ### The Data Structure
        To see all the possible metrics included in the CME Market Sentiment Meter Curated Data File,
        you can see the below headings of the dataframe.
        """
    )

msmHist(stateDate)


st.subheader("raw data")

st.write(pdf.head())

st.write(
        """
        ### Learn More:
        https://www.cmegroup.com/tools-information/market-sentiment-meter.html
        """
    )
