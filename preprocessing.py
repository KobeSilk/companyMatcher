import pandas as pd
from cleanco import basename
import abydos.distance as abd
import streamlit as st
from urllib.parse import urlparse
import re
#Loading data

#Common words to filter from dataset, feel free to add more
common_words = r'\b(sa|holding|groep|holdings|group|groups|inc\.?|incorporated|llc|limited|corporation|corp|bvba| nv|nv |bv | bv|vzw | vzw|international\.?)\b'

#Function to clean company column for better matching
def cleanCompanies(df, column):
    df[column] = df[column].astype(str)
    #Make lowercase
    df["company_cleaned"] = df[column].str.lower()
    #Remove non-ASCI
    df["company_cleaned"].str.encode('ascii', 'ignore').str.decode('ascii')
    #Remove everything between brackets
    df["company_cleaned"] = df["company_cleaned"].replace(r"\[.*?\]|\(.*?\)", "", regex=True)
    #Apply base name
    df["company_cleaned"] = df["company_cleaned"].apply(basename)
    #Remove comming words
    df["company_cleaned"] = df["company_cleaned"].str.replace(common_words, '', regex=True).str.strip()
    #Replace all non-alphanumeric characters
    df["company_cleaned"] = df["company_cleaned"].replace(r'[^a-zA-Z0-9 ]', '', regex=True)

    return df

#Function to extract domain from URL
def extract_domain(url):
    parsed_url = urlparse(url)
    # Split by '.' and get the second element (the middle part)
    return parsed_url.netloc.split('.')[1] if len(parsed_url.netloc.split('.')) > 2 else parsed_url.netloc.split('.')[0]

#Apply domain extraction to dataframe column
def cleanWebsite(df, column):
    df['website_cleaned'] = df[column].astype(str).apply(extract_domain)
    return df

#Upload file
uploaded_file = st.file_uploader("Upload List a", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)


#Select the different
companyName = st.selectbox("Select Company Name Column: ", df.columns)
df_cleaned = cleanCompanies(df,companyName)
csv = df_cleaned.to_csv(index=False)
st.download_button(label="Download data as CSV", data=csv, mime="text/csv", file_name=uploaded_file.name)