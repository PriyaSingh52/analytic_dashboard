import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

years = list(range(1980,2014))
def clean_dataset(df):
    df.drop(['AREA','REG','DEV','Type','Coverage'], axis = 1,inplace = True)
    df.rename(columns={'OdName':'Country','AreaName':'Continent','RegName':'Region','DevName':'Status'},inplace=True)
    df.set_index('Country',inplace=True)
    df['Total'] = df[years].sum(axis=1)
    return df

st.cache()            # helps to make the app faster
def load_dataset():
    df = pd.read_excel('data/Canada.xlsx', sheet_name='Canada by Citizenship', skiprows=20, skipfooter=2)
    df = clean_dataset(df)
    return df

st.title("Immigration from Countries to Canada")
with st.spinner("loading dataset"):       #show loading message
    df = load_dataset()
    st.balloons()

if st.sidebar.checkbox("Show full dataframe"):        #show raw data if checkbox is checked
    st.write(df)


# 5. give user option to select columns
# 6. give user option display graphs
# 0. Run the app run the command below
# streamlit run home.py
st.sidebar.header("Select a country to visualize")
countries = df.index.tolist()
sel_country = st.sidebar.selectbox("Country", countries)

#graph
st.header(f'Immigration from {sel_country} to Canada')
country = df.loc[sel_country, years] # subset
fig = px.line(country, x=country.index, y=country.values)
st.plotly_chart(fig)

st.sidebar.header("Select multiple countries to visualize")
sel_countries = st.sidebar.multiselect("Countries", countries)
if len(sel_countries)>1:
    st.header(f'Comparing countries{",".join(sel_countries)}')
    df_countries = df.loc[sel_countries , years].T
    fig = px.line(df_countries , x=years , y=sel_countries)
    st.plotly_chart(fig)
else:
    st.warning('Please select at least 2 countries for comparision')