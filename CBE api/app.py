import requests
import pandas as pd
import time

#Get Companieslist
companies = pd.read_csv("test Karen.csv")

#Token and headers for CBEAPI

token = "Bearer 45vixGldkLL65CisH5VACBxSLdlAkiFK"
headers = {
    "Authorization":token
}
companies = companies.head(100)
companies
cberesults = pd.DataFrame()
for index,row in companies.iterrows():
    companyName = row["Company_cleaned"]
    r = requests.get(f"https://cbeapi.be/api/v1/company/search?name={companyName}",headers=headers)
    print(r.json())
    if r.status_code == 200:
        flattened = pd.json_normalize(r.json()['data'])
        flattened["Company Name"] = row["Company"]
        cberesults = pd.concat([cberesults,flattened],ignore_index=True)
    time.sleep(0.5)

cberesults

for i,row in cberesults.iterrows():
    address_search = row["address.full_address"]
    print(address_search)
    r = requests.get(f"https://geo.api.vlaanderen.be/geolocation/v4/Location?q={address_search}")
    print(r.json()['LocationResult'])
    if r.json()['LocationResult'] == []:
        cberesults.at[i,"valid address"] = "No"
    else: 
        cberesults.at[i,"valid address"] = "Yes"

cberesults.to_csv("karen_results_1.csv")
