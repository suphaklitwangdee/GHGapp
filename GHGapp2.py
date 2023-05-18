import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from io import StringIO
import PIL.Image as pil

st.set_page_config(page_title="UTM ESG ASSESSMENT TOOL",
                   layout="wide",
                   page_icon="💨",
                   )

# ----MainPage---
st.header('GHG Emission')

# ----side bar----
logo = pil.open('logo1.jpeg')
st.sidebar.image(logo)
file1 = st.sidebar.file_uploader("")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Scope 1", "Scope 2", "Scope 3"])


#Conversionfactors

fuelconv = (0.75*41.85)/(0.75*1000000)
lpgco2ef = 63100 #kgCO2/TJ
lpgch4ef = 1 #kgCO2/TJ
lpgn2oef = 0.1 #kgN2O/TJ
gasco2ef = 69300 #kgCO2/TJ
gasch4ef = 3.3 #kgCH4/TJ
gasn2oef = 3.2 #kgN2O/TJ
dislco2ef = 74100 #kgCO2/TJ
dislch4ef = 3.9 #kgCH4/TJ
disln2oef = 3.9 #kgN2O/TJ
efelectricity = 0.78 #kgCO2/kwh
efwaste = 0.5 #KgCO2e/kg
efwater = 10.6 #KgCO2/m3

gwpch4 = 25 #CH4 CO2equivalence
n2ogwp = 298 #N2O CO2equivalence

if file1 is not None:
    df1 = pd.read_excel(file1)
    
    lpg = df1['LPG'] #LPG consumption in TJ
    lpgco2 = lpgco2ef * lpg
    lpgch4 = lpgch4ef * lpg
    lpgn2o = lpgn2oef * lpg
    totallpg = lpgco2+lpgch4+lpgn2o #total emission by lpg
    totallpgco2e = lpgco2+lpgch4*25+lpgn2o*298 #total emission by lpg in co2 equivalence

    sumscope1 = sum(totallpg)
    sumscope1co2e = sum(totallpgco2e)

    elec = df1['Electricity'] #Electricity consumption in Kwh
    elecco2 = elec*efelectricity

    waste = df1['Waste'] #Waste generation in kg
    wasteco2 = waste*efwaste 

    water = df1['Water'] #Water usage in m3
    waterco2 = water*efwater

    scope2 = elecco2+wasteco2
    sumscope2 = sum(scope2)


    car = df1['Car'] #Distance travelled by cars in km (Assuming cars use only gasoline)
    carco2 = car*fuelconv*gasco2ef
    carch4 = car*fuelconv*gasch4ef
    carn2o = car*fuelconv*gasn2oef

    carco2e = carco2+carch4+carn2o

    truck = df1['Truck'] #Distance travelled by Trucks in km (Assuming trucks use only diesel)
    truckco2 = truck*fuelconv*dislco2ef
    truckch4 = truck*fuelconv*dislch4ef
    truckn2o = truck*fuelconv*disln2oef

    truckco2e = truckco2+truckch4+truckn2o

    scope3 = carco2+carch4+carn2o+truckco2+truckch4+truckn2o
    scope3co2e = carco2+carch4*25+carn2o*298+truckco2+truckch4*25+truckn2o*298

    sumscope3 = sum(scope3)
    sumscope3co2e = sum(scope3co2e)

    alltotalco2e = totallpgco2e+scope2+scope3co2e
    averagetotalco2e = sum(alltotalco2e)/12

    avggraph = [averagetotalco2e/1000]*12

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df1['Month'], y=totallpg, name="Scope 1"))
    fig1.add_trace(go.Bar(x=df1['Month'], y=scope2, name="Scope 2"))
    fig1.add_trace(go.Bar(x=df1['Month'], y=scope3, name="Scope 3"))
    fig1.update_xaxes(type='category')
    fig1.update_layout(barmode='stack',
                       title="Total emission")   
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df1['Month'], y=totallpgco2e/1000, name="Scope 1"))
    fig2.add_trace(go.Bar(x=df1['Month'], y=scope2/1000, name="Scope 2"))
    fig2.add_trace(go.Bar(x=df1['Month'], y=scope3co2e/1000, name="Scope 3"))
    fig2.update_xaxes(type='category')
    fig2.update_layout(barmode='stack',
                       title="Total GHG emission",
                       xaxis_title = "2022",
                       yaxis_title = "GHG Emission Tons CO2e")

    fig3 = go.Figure(data=[go.Pie(labels=["Scope 1", "Scope 2", "Scope 3"], 
                                  values=[sumscope1co2e, sumscope2, sumscope3co2e])])
    fig3.update_layout(title="GHG by scope")

    fig4 = go.Figure(data=go.Scatter(x=df1['Month'], y=alltotalco2e/1000, name="GHG emission"))
    fig4.add_trace(go.Scatter(x=df1['Month'], y=avggraph, name="Average GHG emission"))
    fig4.update_layout(title="Total CO2 equivalent GHG emission",
                       yaxis_title="GHG Emission Tons CO2e",
                       xaxis_title="2022")

    fig5 = go.Figure(data=go.Scatter(x=df1['Month'], y=totallpgco2e/1000, name="GHG emission by Scope 1"))
    fig5.update_layout(title="Total GHG emission by Scope 1",
                       yaxis_title="Ton CO2e",
                       xaxis_title="2022"
                       )

    fig6 = go.Figure(data=go.Scatter(x=df1['Month'], y=scope2/1000, name="GHG emission by Scope 2"))
    fig6.update_layout(title="Total GHG emission by Scope 2",
                       yaxis_title="Ton CO2e",
                       xaxis_title="2022"
                       )

    fig7 = go.Figure(data=go.Scatter(x=df1['Month'], y=scope3co2e/1000, name="GHG emission by Scope 3"))
    fig7.update_layout(title="Total GHG emission by Scope 3",
                       yaxis_title="Ton CO2e",
                       xaxis_title="2022"
                       )

    fig8 = go.Figure(data=[go.Pie(labels=["Electricity", "Waste", "Water"], 
                                  values=[sum(elecco2), sum(wasteco2), sum(waterco2)])])
    fig8.update_layout(title="Scope 2 GHG emission sources")

    fig9 = go.Figure(data=[go.Pie(labels=["Car", "Truck"], 
                                  values=[sum(carco2e), sum(truckco2e)])])
    fig9.update_layout(title="Scope 3 GHG emission sources")

    fig10 = go.Figure(data=[go.Pie(labels=["LPG"], 
                                  values=[sumscope1co2e])])
    fig10.update_layout(title="Scope 1 GHG emission sources")
    
    with tab1:
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
    
    with tab2:
        st.plotly_chart(fig5)
        st.plotly_chart(fig10)
        
    with tab3:
        st.plotly_chart(fig6)
        st.plotly_chart(fig8)

    with tab4:
        st.plotly_chart(fig7)
        st.plotly_chart(fig9)


        

