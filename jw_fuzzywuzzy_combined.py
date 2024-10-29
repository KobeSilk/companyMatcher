import jellyfish
import pandas as pd
from fuzzywuzzy import fuzz
import re

droplist = {"contractors","bureau","architecten","architectuur","architecture","studio","construct","bouwonderneming","bouwwerken","bouw","vzw","group","nederland","nv","bvba","groep","technology","the","van", "de", "het","engineering","recruitment","solutions","solution","consultancy","consulting","professionals","brands","media","services","belgium","belgi","benelux","europe","belux"}
def preprocess_name(name):
    # Split name into words and remove common words and places
    name = name.lower()
    re.sub(r'[^A-Za-z0-9 ]+', '', name)
    words = name.split()
    core_words = [word for word in words if word not in droplist]
    name = " ".join(core_words)
    return name

def preprocess_list(input_list):
    processed_dict = {}
    for name in input_list:
        preprocessed_name = preprocess_name(name)
        processed_dict[preprocessed_name] = name
    return processed_dict

def compare_company_names_optimized(list1, list2, threshold=0.8, penalty=0.2,length_threshold=7):
    processed_list1 = preprocess_list(list1)
    processed_list2 = preprocess_list(list2)
    matches = []

    for clean_name1, original_name1 in processed_list1.items():
        for clean_name2, original_name2 in processed_list2.items():
            # Calculate similarity scores
            jw_similarity = jellyfish.jaro_winkler_similarity(clean_name1, clean_name2)
            token_similarity = fuzz.token_set_ratio(clean_name1, clean_name2) / 100
            combined_similarity = 0.6*jw_similarity + 0.4*token_similarity
            
            # Append if similarity is above the threshold
            if jw_similarity >= threshold or token_similarity >= threshold:
                matches.append((original_name1, original_name2, combined_similarity, jw_similarity, token_similarity))
    df = pd.DataFrame(matches, columns=["List1_Name", "List2_Name", "Combined_Similarity", "JW_Similarity", "Token_Similarity"])
    return df

list1 = pd.read_csv("Overzciht/matching lists/basislijst exact.csv").iloc[:,2].tolist()
list2 = pd.read_csv("Overzciht/matching lists/BIM_linkedinsalesnav.csv").iloc[:,6].tolist()

matches = compare_company_names_optimized(list1,list2)
matches.to_csv("overzicht_test.csv", index=False)