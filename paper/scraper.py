import requests
from requests.exceptions import HTTPError
import pandas as pd


URL = "https://api-gateway.ss.ge/v1/RealEstate/LegendSearch"
AUTH_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkEzMTIxOUJCRUNCNTkyNkNEOTEzMzJDMkIwNTMzMEJERENFNkRBODJSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6Im94SVp1LXkxa216WkV6TENzRk13dmR6bTJvSSJ9.eyJuYmYiOjE3MTE5NTcxNTgsImV4cCI6MTcxMTk2MDc1OCwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LnNzLmdlIiwiYXVkIjpbImZpbGVzIiwicGFpZF9zZXJ2aWNlcyIsIndlYl9hcGlnYXRld2F5IiwicmVhbF9lc3RhdGUiLCJzdGF0aXN0aWNzIiwidXNlcl9yZWdpc3RyYXRpb24iLCJKb2JhcmlhQVBJIl0sImNsaWVudF9pZCI6InNzd2ViIiwiaWF0IjoxNzExOTU3MTU4LCJzY29wZSI6WyJmaWxlcyIsInBhaWRfc2VydmljZXMiLCJyZWFsX2VzdGF0ZSIsInN0YXRpc3RpY3MiLCJ1c2VyX3JlZ2lzdHJhdGlvbiIsIndlYl9hcGlnYXRld2F5Il19.oudV8borEjPFfvc5x6V5sEXIBVi_stgLuxb_DaTUOMO9fmMQTce0Ier0ZSKXG2Xw2J8vHhQyrRZb7hFlp4mbr44bjLTqQrKxtyFmukMNNmpLfnaxZ6xpIyYSu-oO8hTeqNcQueegPH_QILiOTqLE_uVkT_6i6lSwQzVemc_jgQ1oShCRWpkdLVrUeBEifozACqeAdLd_7YZ4vRYtPkG0TtKqRLKJIHDSv26YqlcEJUBKK_HyOghG2lO6nBtnhCjS3shMfxnW86xkNLBEQeMj1Myl2JtKuBuR03x4VCOuFKUpDjOU900puAPQOV1oDxbSQiZm1_deZmkkFUnWrYbD3Q"
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Origin": "https://home.ss.ge",
    "Referer": "https://home.ss.ge/",
    "User-Agent": "Mozilla/5.0"
}
payload = {
    "currencyId": 1,
    "page": 2,
    "pageSize": 16,
    "realEstateDealType": 4,
    "realEstateType": 5,
}

def scrape_single_page(page: int):
    try:
        response = requests.post(URL, headers=HEADERS, json={**payload, "page": page})
    except HTTPError as ex:
        # add retry logic
        print(ex.args[0])
        raise ex
    
    properties = []
    parsed_response = response.json()
    for prop in parsed_response["realStateItemModel"]:
        title = prop["title"]
        address = prop["address"]
        price = prop["price"]
        total_area = prop["totalArea"]
        building_floors = prop["totalAmountOfFloor"]
        floor = prop["floorNumber"]
        bedrooms = prop["numberOfBedrooms"]

        prop_norm = {
            "title": title,
            "address": address,
            "price": price,
            "total_area": total_area,
            "total_floors": building_floors,
            "floor": floor,
            "bedrooms": bedrooms

        }
        properties.append(prop_norm)
        return properties


def scrape_pagination() -> list[dict]:
    scraping = True
    page = 1
    properites = []
    while scraping:
        page_properties = scrape_single_page(page)
        if len(page_properties) > 0:
            properites.extend(page_properties)
        else:
            scraping = False
            print(f"No more properties on page {page}.")
            print("DONE!")
    return properites
            

if __name__ == "__main__":
    properies = scrape_pagination()
    df = pd.DataFrame(properies)
    df.to_csv("./real_estate.csv", index=False)
