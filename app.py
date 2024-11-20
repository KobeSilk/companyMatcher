import re
import jellyfish
import pandas as pd
from fuzzywuzzy import fuzz

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

preprocess_name("Up Time Group")
naam1 = preprocess_name("MARS BELGIUM")
naam2 = preprocess_name("Mars")
naam1
naam2
jw_similarity = jellyfish.jaro_winkler_similarity(naam1, naam2)
jw_similarity
token_similarity = fuzz.token_set_ratio(naam1,naam2) / 100
token_similarity
