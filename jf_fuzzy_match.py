from thefuzz import fuzz
from thefuzz import process
import pandas as pd
import tfidf_matcher as tm
import jellyfish

def remove_non_str_elements(input_list):
    return [element for element in input_list if isinstance(element, str)]

# Example lists of company names
original = pd.read_csv("data/list a.csv",header=None)[0].tolist()
lookupList = pd.read_csv("data/list b.csv",header=None)[0].tolist()

lookupList = remove_non_str_elements(lookupList)
suffixes_list = ['belgium', 'belgi', 'benelux','europe','belux', 'nederland',' nv','group','groep', 'international', 'technology', '.be','.com']
prefixes_list = ['the ','de ']
def removeprefixes(text_list,prefixes_list):
    for x in prefixes_list:
        text_list = [y.removeprefix(x) for y in text_list]
    return text_list

def removesuffixes(text_list, suffixes_list):
    for x in suffixes_list:
        text_list = [y.removesuffix(x) for y in text_list]
    text_list = [x.strip() for x in text_list]
    return text_list

lookup_cleaned = removesuffixes(lookupList,suffixes_list)
original_cleaned = removesuffixes(original,suffixes_list)
lookup_cleaned = removeprefixes(lookup_cleaned,prefixes_list)
original_cleaned = removeprefixes(original_cleaned,prefixes_list)

#tdf-idf
matched = tm.matcher(original_cleaned,lookup_cleaned,2,3)
matched.to_csv("data/tdf_matched.csv")

common_dutch_words = {"van ", "de ", "het "}
def has_common_dutch_words(name):
    # Check if any of the common words are in the name
    return any(word in name.lower().split() for word in common_dutch_words)

#jellyfish
def jf_compare(list1,list2, threshold=0.8, avg_length_threshold=8,penalty=0.2):
    matches = []
    for name1 in list1:
        for name2 in list2:
            avg_length = (len(name1) + len(name2)) / 2
            
            # Calculate Jaro-Winkler similarity between the two names
            similarity = jellyfish.jaro_winkler_similarity(name1, name2)
            if avg_length < avg_length_threshold: 
                weighting_factor = avg_length / avg_length_threshold
                similarity *= weighting_factor
            if (" " not in name1 or " " not in name2) and similarity != 1:
                similarity *= (1 - penalty*(1/len(name1)))
            # Append to matches if similarity is above the threshold
            if similarity >= threshold:
                matches.append((name1, name2, similarity))
    df = pd.DataFrame(matches, columns = ["List1_Name", "List2_Name", "Similarity"])
    return df

matches = jf_compare(lookup_cleaned,original_cleaned, 0.8)
matches.to_csv("data/jf_matched.csv")