import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import date
import os
import boto3
import pytz
import altair as alt
#from link_button import link_button

st.set_page_config(page_title="Compound Interest Calculator",page_icon="💹",layout="wide")

with st.form(key='columns_in_form'):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        initialInvestment = st.text_input("Starting capital",value=500)
    with c2:
        monthlyContribution = st.text_input("Monthly contribution (Optional)",value=100)
    with c3:
        annualRate = st.text_input("Annual increase rate in percentage",value="15")
    with c4:
        investingTimeYears = st.text_input("Duration in years:",value=10)

    submitButton = st.form_submit_button(label = 'Calculate')

annualRateCalculated = 1 + int(annualRate.replace("%",""))/100
initialInvestment = int(initialInvestment)
monthlyContribution = int(monthlyContribution)
investingTimeYears = int(investingTimeYears)

def compoundCalculation(annualRateCalculated,initialInvestment,monthlyContribution,investingTimeYears):

    year = 1
    sumInvestment = initialInvestment
    dictInvestment = {}
    dictReturn = {}
    totalContributions = 0

    if monthlyContribution == 0:
        
        totalContributions = initialInvestment

        while year <= investingTimeYears:

            investmentTotal = sumInvestment * annualRateCalculated
            dictInvestment[year] = investmentTotal
            sumInvestment = investmentTotal
            year = year + 1
            
        dictReturn['Total Contributions'] = totalContributions
        dictReturn['Compounded Interest'] = dictInvestment[investingTimeYears] - totalContributions
        dictReturn['Total Value'] = dictInvestment[investingTimeYears]
        dictReturn['Yearly Growth'] = dictInvestment
        
        return dictReturn

    else:
        
        totalContributions = initialInvestment

        while year <= investingTimeYears:

            month = 1
            monthlyRateCalculated = 1 + ((annualRateCalculated - 1)/12)

            while month <= 12:

                investmentTotal = sumInvestment * monthlyRateCalculated + monthlyContribution
                sumInvestment = investmentTotal
                totalContributions = totalContributions + monthlyContribution
                month = month + 1
            
            dictInvestment[year] = investmentTotal
            year = year + 1
            
        dictReturn['Total Contributions'] = totalContributions
        dictReturn['Compounded Interest'] = dictInvestment[investingTimeYears] - totalContributions
        dictReturn['Total Value'] = dictInvestment[investingTimeYears]
        dictReturn['Yearly Growth'] = dictInvestment
            
        return dictReturn

if submitButton:

    output = compoundCalculation(annualRateCalculated,initialInvestment,monthlyContribution,investingTimeYears)

    amountInvested = output['Total Contributions']
    walletValue = output['Total Value']
    walletEvolution = output['Yearly Growth']
    profit = output['Compounded Interest']
    df = pd.DataFrame.from_dict(walletEvolution,orient='index',columns=['PriceUSD'])


    col1, col2, col3, col4 = st.columns(4)

    deltaInvestment = (walletValue - amountInvested) / amountInvested * 100

    col1.metric("Total Contributions", amountInvested, delta=None, delta_color='normal')
    col2.metric("Total Value", round(walletValue,2), delta=f"{round(deltaInvestment,2)}%", delta_color='normal')
    col3.metric("Profit realised", f"{round(profit,2)}", delta=None, delta_color='normal')

    with col4:
        #link_button(f"It's never too late to start investing! Begin your journey right now!", url='https://docs.streamlit.io/en/stable/')

    c = alt.Chart(df.reset_index()).mark_line().encode(x=alt.X('index', title='Year'),y=alt.Y('PriceUSD', title='Total Value'))

    st.altair_chart(c, use_container_width=True)
