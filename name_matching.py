import pandas as pd
from cleanco import basename
#import abydos.distance as abd
from thefuzz import fuzz, process
import streamlit as st
#Loading data

st.write("Choose first list to match: ")

a = st.file_uploader("list a", type=["csv"])
if a:
    list_a = pd.read_csv(a)

st.write("Choose second list to match: ")

b = st.file_uploader("list b", type=["csv"])
if b:
    list_b = pd.read_csv(b)

st.write("Choose Company name column to match with: ")
a_name_column = st.selectbox("Company Name column from list A", list_a.columns)
b_name_column = st.selectbox("Company Name column from list b", list_b.columns)

list_a = list_a[list_a[a_name_column].notna()]
list_b = list_b[list_b[b_name_column].notna()]

dfs = [list_a,list_b]

def merge_dataframes_on_column(dfs, column_name, how='inner'):
    # Start by merging the first DataFrame with the next, iterating through the list
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=column_name, how=how)
    return merged_df

merged_df = merge_dataframes_on_column(dfs,a_name_column,how='inner')

st.write("Select columns to keep:")
columns_to_keep = st.multiselect("Select columns", options=merged_df.columns.tolist())
if columns_to_keep:
    # Filter the dataframe with the selected columns
    filtered_df = merged_df[columns_to_keep]
    
    st.write("Here is the filtered data:")
    st.dataframe(filtered_df)
    
    # Button to export filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download filtered data as CSV", data=csv, mime="text/csv", file_name="filtered_data.csv")