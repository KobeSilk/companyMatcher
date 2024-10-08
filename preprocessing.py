import pandas as pd
from cleanco import basename
#import abydos.distance as abd
from thefuzz import fuzz, process
import streamlit as st
from urllib.parse import urlparse
#Loading data

common_words = r'\b(sa|holding|groep|holdings|group|groups|Inc\.?|incorporated|LLC|limited|corporation|corp\.?)\b'

uploaded_file_a = st.file_uploader("Upload List a", type=["csv"])
if uploaded_file_a:
    list_a = pd.read_csv(uploaded_file_a)

def cleanCompanies(df, column):
    df[column] = df[column].astype(str)
    #Make lowercase
    df["company_cleaned"] = df[column].str.lower()
    #Remove non-ASCI
    df["company_cleaned"].str.encode('ascii', 'ignore').str.decode('ascii')
    #Apply base name
    df["company_cleaned"] = df["company_cleaned"].apply(basename)
    #Remove comming words
    df["company_cleaned"] = df["company_cleaned"].str.replace(common_words, '', regex=True).str.strip()
    #Replace all non-alphanumeric characters
    df["company_cleaned"] = df["company_cleaned"].replace(r'[^a-zA-Z0-9 ]', '', regex=True)
    return df

def extract_domain(url):
    parsed_url = urlparse(url)
    # Split by '.' and get the second element (the middle part)
    return parsed_url.netloc.split('.')[1] if len(parsed_url.netloc.split('.')) > 2 else parsed_url.netloc.split('.')[0]

def cleanWebsite(df, column):
    df['website_cleaned'] = df[column].astype(str).apply(extract_domain)
    return df

companyName = st.selectbox("Select Company Name Column: ", list_a.columns)

cleaned_a = cleanCompanies(list_a,companyName)

companyWebsite = st.selectbox("Select Company Website Column: ", list_a.columns)

cleaned_b = cleanWebsite(cleaned_a, companyWebsite)

cleaned_b

st.write("Select columns to keep:")
columns_to_keep = st.multiselect("Select columns", options=cleaned_a.columns.tolist())
if columns_to_keep:
    # Filter the dataframe with the selected columns
    filtered_df = cleaned_a[columns_to_keep]
    
    st.write("Here is the filtered data:")
    st.dataframe(filtered_df)
    
    # Button to export filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download filtered data as CSV", data=csv, mime="text/csv", file_name="filtered_data.csv")