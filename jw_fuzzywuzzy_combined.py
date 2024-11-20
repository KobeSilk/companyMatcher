import jellyfish
import pandas as pd
from fuzzywuzzy import fuzz
import re
import streamlit as st

st.title = "Company Name matching"

#Convert dataframe to csv
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

droplist = {"architectenbureau","algemene bouw","architects","international","industries","manufacturing","global","logistics","bureau","architecten","architectuur","architecture","construct","bouwonderneming","bouwwerken","bouw","vzw","group","nederland","nv","bvba","groep","technology","the","van", "de", "het","engineering","recruitment","solutions","solution","consultancy","consulting","professionals","brands","media","services","belgium","belgi","benelux","europe","belux"}
def preprocess_name(name):
    name = str(name)
    # Split name into words and remove common words and places
    name = name.lower()
    name = re.sub(r'[-/\']', ' ',name)
    name = re.sub(r'[^A-Za-z0-9 ]+', '', name)
    words = name.split()
    core_words = [word for word in words if word not in droplist]
    name = " ".join(core_words)
    return name

#Preprocess list to ensure there are no duplicates
def preprocess_list(input_list):
    processed_dict = {}
    for name in input_list:
        processed_dict[name] = name
    return processed_dict

def compare_company_names_optimized(list1, list2, threshold=0.8, penalty=0.2,length_threshold=7):
    processed_list1 = preprocess_list(list1)
    processed_list2 = preprocess_list(list2)
    matches = []

    for clean_name1, original_name1 in processed_list1.items():
        clean_name1 = preprocess_name(clean_name1)
        for clean_name2, original_name2 in processed_list2.items():
            clean_name2 = preprocess_name(clean_name2)
            # Calculate similarity scores
            jw_similarity = jellyfish.jaro_winkler_similarity(clean_name1, clean_name2)
            token_similarity = fuzz.token_set_ratio(clean_name1, clean_name2) / 100
            combined_similarity = 0.6*jw_similarity + 0.4*token_similarity
            
            # Append if similarity is above the threshold
            if jw_similarity >= threshold or token_similarity >= threshold:
                matches.append((original_name1, original_name2, combined_similarity, jw_similarity, token_similarity))
    df = pd.DataFrame(matches, columns=["List1_Name", "List2_Name", "Combined_Similarity", "JW_Similarity", "Token_Similarity"])
    return df

#Upload file

# Upload file 1
list1 = st.file_uploader(label="Please upload list 1", type="csv", key="list1")
if list1 is not None:
    if "df1" not in st.session_state:
        st.session_state.df1 = pd.read_csv(list1, encoding='utf-8-sig')
    df1 = st.session_state.df1
    columnName = st.selectbox(
        label="Please select column with company names (List 1)",
        options=df1.columns,
        key="column1"
    )

# Upload file 2
list2 = st.file_uploader(label="Please upload list 2", type="csv", key="list2")
if list2 is not None:
    if "df2" not in st.session_state:
        st.session_state.df2 = pd.read_csv(list2, encoding='utf-8-sig')
    df2 = st.session_state.df2
    columnName2 = st.selectbox(
        label="Please select column with company names (List 2)",
        options=df2.columns,
        key="column2"
    )

# Match Names Button
if list1 and list2 and "df1" in st.session_state and "df2" in st.session_state:
    companies1 = st.session_state.df1[st.session_state.column1].tolist()
    companies2 = st.session_state.df2[st.session_state.column2].tolist()

    if st.button(label="Match Names"):
        if "matches" not in st.session_state:
            st.session_state.matches = compare_company_names_optimized(companies1, companies2)
        matches = st.session_state.matches
        st.dataframe(matches)
        csv = convert_df(matches)
        st.download_button("Export table to CSV",data=csv, file_name="Company Name Match.csv", mime="text/csv")
