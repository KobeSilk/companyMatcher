import pandas as pd
from cleanco import basename
#import abydos.distance as abd
from thefuzz import fuzz, process
import streamlit as st
#Loading data

uploaded_file_a = st.file_uploader("Upload List A", type=["csv"])
if uploaded_file_a:
    list_a = pd.read_csv(uploaded_file_a)
list_a

nameColumnA = st.selectbox("Select Company Name Column:", list_a.columns)

uploaded_file_b = st.file_uploader("Upload List B", type=["csv"])
if uploaded_file_b:
    list_b = pd.read_csv(uploaded_file_b)
list_b

nameColumnB = st.selectbox("Select Company Name Column:", list_b.columns)

common_words = r'\b(sa|holding|groep|holdings|group|groups|Inc\.?|incorporated|LLC|limited|corporation|corp\.?)\b'









