import numpy as np
import pandas as pd
import streamlit as st
import re

st.title("Phone number cleaner")
phonenumber = pd.read_csv(st.file_uploader("upload phone numbers",type="csv"))
column = st.selectbox("Choose column that has phone numbers:",phonenumber.columns)
# Define the string

df = phonenumber
df['mobile_cleaned'] = df[column].apply(lambda x: re.sub(r"[()\[\]{}<>].*?[()\[\]{}<>]|\.|\/| +", '', str(x)).strip())
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('32'),'+'+ df.mobile_cleaned,df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('3'),'+32'+ 
df.mobile_cleaned.str[1:],df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('04'),'+32'+ 
df.mobile_cleaned.str[1:],df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('03'),'+32'+ 
df.mobile_cleaned.str[1:],df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('08'),'+32'+ 
df.mobile_cleaned.str[1:],df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('02'),'+32'+ 
df.mobile_cleaned.str[1:],df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('09'),'+32'+ 
df.mobile_cleaned.str[1:],df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('05'),'+32'+ 
df.mobile_cleaned.str[1:],df.mobile_cleaned)
df.mobile_cleaned=np.where(df.mobile_cleaned.str.startswith('00'),'+'+ 
df.mobile_cleaned.str[2:],df.mobile_cleaned)
df.mobile_cleaned = df.mobile_cleaned.str.replace(' ', '')

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")
#df[column] = df[column].astype(str)
#df["mobile_cleaned"] = df["mobile_cleaned"].astype(str)
csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="phones_cleaned.csv",
    mime="text/csv",
)