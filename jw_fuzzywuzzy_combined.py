import jellyfish
import pandas as pd
from fuzzywuzzy import fuzz

# List of common Dutch words and place names
suffixes_list = ['belgium', 'belgi', 'benelux','europe','belux', 'nederland',' nv','group','groep', 'international', 'technology', '.be','.com']

def removeprefixes(text_list,prefixes_list):
    for x in prefixes_list:
        text_list = [y.removeprefix(x) for y in text_list]
    return text_list

def removesuffixes(text_list, suffixes_list):
    for x in suffixes_list:
        text_list = [y.removesuffix(x) for y in text_list]
    text_list = [x.strip() for x in text_list]
    return text_list

common_dutch_words = {"group","nederland","nv","bvba","groep","technology","the","van", "de", "het","engineering","recruitment","solutions","solution","consultancy","consulting","professionals","brands","media","services","belgium","belgi","benelux","europe","belux"}

common_places = {"antwerpen","antwerp"}
def remove_non_str_elements(input_list):
    return [element for element in input_list if isinstance(element, str)]
def preprocess_name(name):
    # Split name into words and remove common words and places
    words = name.split()
    core_words = [word for word in words if word not in common_dutch_words and word not in common_places]
    return " ".join(core_words)

def compare_company_names(list1, list2, threshold=0.8, penalty=0.2,length_threshold=7):
    matches = []
    for name1 in list1:
        for name2 in list2:
            # Preprocess names
            clean_name1 = preprocess_name(name1)
            clean_name2 = preprocess_name(name2)
            
            # Use a combination of Jaro-Winkler and Token Set Ratio
            jw_similarity = jellyfish.jaro_winkler_similarity(clean_name1, clean_name2)
            token_similarity = fuzz.token_set_ratio(clean_name1, clean_name2) / 100
            
            # Combine the two scores
            combined_similarity = (jw_similarity + token_similarity) / 2
            
            # Apply penalty if both names are short or common
            #if combined_similarity != 1:
            #    if len(clean_name1.split()) == 1 or len(clean_name2.split()) == 1:
            #        combined_similarity *= (1 - penalty)
            # Append if similarity is above the threshold
            if (jw_similarity >= threshold or token_similarity >= threshold):
                matches.append((name1, name2, combined_similarity, jw_similarity, token_similarity))
    
    df = pd.DataFrame(matches, columns=["List1_Name", "List2_Name", "combined similarity", "jw_similarity", "token_similarity"])
    return df

list1 = pd.read_csv("data/list a.csv",header=None)[0].tolist()
list2 = pd.read_csv("data/list b.csv",header=None)[0].tolist()
# Function to preprocess names by removing common words and places
list1 = remove_non_str_elements(list1)
list2 = remove_non_str_elements(list2)

list1 = removesuffixes(list1,suffixes_list)
list2 = removesuffixes(list2,suffixes_list)

# Function to compare company names
# Example usage
matches = compare_company_names(list1, list2, threshold=0.8)
matches.to_csv("data/company_name_matches_no_penalty.csv", index=False)